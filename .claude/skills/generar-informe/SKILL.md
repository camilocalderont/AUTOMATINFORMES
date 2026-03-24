---
name: generar-informe
description: "Orchestrates complete monthly activity report generation for a government entity by running sub-skills sequentially: API extractions, evidence search, commits, support reports, meeting summaries. Use when user says \"generar informe\", \"generate report\", \"informe mensual\", or provides entity with date range. Produces OBLIGACION_N/ folders, Word/Excel deliverables, and final Markdown report."
argument-hint: "[ENTIDAD] [FECHA_INICIO] [FECHA_FIN]"
---

# Skill: Generar Informe Completo (Orquestador)

Este skill orquesta la ejecucion secuencial de los sub-skills para generar el informe completo de una entidad.

## ENTRADA
- **$0**: Entidad (IDARTES, SDMUJER, IDT, UAECD)
- **$1**: Fecha inicio (YYYY-MM-DD)
- **$2**: Fecha fin (YYYY-MM-DD)

## PROCESO

### PASO 0: Resolver rutas e inicializar log

Ejecutar la resolucion de rutas estandar segun `.claude/skills/shared/paso0-rutas.md`.

**Variables adicionales de este skill:**
- `{dia_actual}` = `date +%Y-%m-%d`
- `{log_file}` = `{carpeta_mes}/log_{entidad_lower}_{mes}_{year}.md`
- **Inicializar archivo de log** con encabezado: titulo, periodo, fecha de ejecucion

### PASO 0B: Verificar/crear estructura de carpetas

- Verificar existencia de `{carpeta_mes}` y `{carpeta_evidencias}`. Si no existen → `mkdir -p`
- Crear subcarpetas definidas en `rutas.subcarpetas` del config.json

**Registrar en log** — ver formato en `examples/log_formats.md#paso-0b`

---

### PASO 1: Cargar configuracion completa

Leer ambos archivos:
```
entidades/$0/README.md   → Obligaciones contractuales y mapeo
entidades/$0/config.json → Rutas, correos, ramas git (ya leido en PASO 0)
```

Extraer:
- Lista de obligaciones contractuales (texto completo de cada una)
- Mapeo de evidencias a obligaciones
- Configuracion de `mesa_servicios.tipo` (glpi o correo)
- Estructura de `anexos` (objeto con metadata: nombre, extension, obligaciones, fuente_key, manual)

---

### PASO 2: Extraer insumos via API

Ejecutar las extracciones API como insumos previos. **Los pasos 2B, 2C y 2D se pueden lanzar como agentes paralelos.**

#### PASO 2A: Mesa de servicios (GLPI o Correo)

Consultar `mesa_servicios.tipo` del config.json:

**Si tipo == "glpi"** (IDARTES, SDMUJER) y tiene `api.glpi` con tokens no vacios:
```
/extraer-tickets-glpi $0 $1 $2
```

**Si tipo == "correo"** y tiene `api.gmail` (IDT) — **usar Agent tool** (subagent_type: "general-purpose") con prompt que incluya:
1. ToolSearch para cargar herramientas del MCP server `{api.gmail.mcp_server}`
2. Buscar correos: `from:me after:{YYYY/MM/DD} before:{YYYY/MM/DD}`
3. Leer contenido COMPLETO de cada correo (incluyendo hilos RE:/FW:)
4. Clasificar correos por tipo
5. Escribir JSON intermedio en `{carpeta_fuentes}/_correos_data_{entidad_lower}_{mes}.json`
6. Ejecutar `python3 scripts/correos_to_docx.py` para generar .docx
7. Eliminar JSON si exitoso
8. Escribir .md en `{carpeta_evidencias}/correos_api_{entidad_lower}_{mes}.md`

**Si tipo == "correo"** y tiene `api.outlook` (UAECD):
```
/extraer-correos-outlook $0 $1 $2
```

**Si no tiene API o falla:** Registrar en log, continuar (PASO 5 usara fallback).

#### PASO 2B: Gestion de proyectos (Jira) — Subagente

**Si tiene `api.jira`** (IDARTES): Lanzar Agent (subagent_type: "general-purpose", **run_in_background: true**) que ejecute:
```bash
python3 scripts/jira_extract.py $0 $1 $2 "{carpeta_evidencias}/jira_issues_{entidad_lower}_{mes}.md" --output-xlsx "{carpeta_fuentes}/jira_{entidad_lower}_{mes}.xlsx"
```

**Si no tiene `api.jira`:** Saltar.

#### PASO 2C: Correo suplementario (solo entidades con GLPI + Gmail) — Subagente

Si `mesa_servicios.tipo == "glpi"` Y tiene `api.gmail` (ej: IDARTES): Lanzar Agent (run_in_background: true) con la misma plantilla del PASO 2A (version Gmail).

#### PASO 2D: Calendario

Si tiene `api.calendar`:
```
/extraer-reuniones-calendario $0 $1 $2
```

#### PASO 2E: Resumen de reuniones

```
/resumen-reuniones $0 $1 $2
```
→ Genera .md y .docx **antes** de buscar-evidencias para que los entregables sean encontrados.

#### Paralelizacion del PASO 2

2B y 2C se lanzan en **background**. 2D se ejecuta normal. 2E espera (depende de 2D). Finalmente esperar resultados de 2B y 2C con TaskOutput.

**Registrar en log** — ver formato en `examples/log_formats.md#paso-2`

---

### PASO 3: Ejecutar `/buscar-evidencias`

```
/buscar-evidencias $0 $1 $2
```

**Esperar** a que termine. Luego leer: `{carpeta_evidencias}/evidencias_{entidad_lower}_{mes}.md`

**IMPORTANTE:** Verificar que buscar-evidencias ejecuto los 3 `find` (2A carpeta_anual, 2B carpeta_evidencias, 2C carpeta_fuentes). El log debe mostrar cuantos archivos encontro cada uno con el resumen consolidado. Si solo muestra archivos de FUENTES, algo fallo — repetir buscar-evidencias.

**Nota:** buscar-evidencias PASO 6 copia archivos de evidencia de carpeta_anual a OBLIGACION_N/ via script Python (`organize_evidencias.py`). generar-informe PASO 10 agrega los entregables estandar (Word/Excel de FUENTE/) encima. Ambos pasos son complementarios.

**Registrar en log** — ver formato en `examples/log_formats.md#paso-3`

---

### PASO 4: Ejecutar `/generar-commits`

```
/generar-commits $0 $1 $2
```

**Esperar** a que termine. Luego leer: `{carpeta_evidencias}/commits_{entidad_lower}_{mes}.md`

**Registrar en log** — ver formato en `examples/log_formats.md#paso-4`

---

### PASO 5: Ejecutar skill de soportes (segun tipo de mesa de servicios)

**Si tipo == "correo"** (IDT, UAECD):
```
/generar-soportes-correo $0 $1 $2
```

**Si tipo == "glpi"** (IDARTES, SDMUJER):
```
/generar-soportes-glpi $0 $1 $2
```

**Nota:** Estos skills tienen PASO 1.5A que detecta si la extraccion API del PASO 2 ya genero el archivo.

**Registrar en log** — ver formato en `examples/log_formats.md#paso-5`

---

### PASO 6: Ejecutar `/generar-plan-accion` (condicional)

**Solo si** `config.json["anexos"]` tiene una entrada con `"fuente_key": "plan_accion"` (actualmente solo SDMUJER):

```
/generar-plan-accion $0 $1 $2
```

Este skill:
1. Consume `evidencias_{entidad_lower}_{mes}.md` del PASO 3 (no re-escanea archivos)
2. Redacta reporte cualitativo del indicador de seguridad
3. Genera .md y .docx (via `/md-to-docx`) en `{carpeta_planes}/`
4. Copia .docx a `{carpeta_fuentes}/plan_accion_{entidad_lower}_{mes}.docx`

**Si no aplica:** Saltar. Registrar "Saltado (entidad sin plan_accion)" en log.

**Registrar en log:** Resultado (ejecutado/saltado), archivos generados.

---

### PASO 7: Consolidar inventario de evidencias

Con los outputs de los sub-skills, construir inventario unificado:

1. **Evidencias documentales** (de buscar-evidencias): archivos encontrados con su resumen y obligaciones
2. **Commits** (de generar-commits): resumen general, reporte por semana, tabla de commits
3. **Soportes** (de generar-soportes-*): resumen de tickets/correos atendidos
4. **Issues Jira** (de extraer-issues-jira, solo IDARTES): historias de usuario, bugs, tareas
5. **Reuniones** (de resumen-reuniones): resumen de reuniones del periodo
6. **Anexos estandar** (de config.json): archivos pre-existentes en carpeta_evidencias

---

### PASO 8: Mapear evidencias a obligaciones

Para cada obligacion del README.md:
1. Revisar el mapeo definido (columna "Tipo de Evidencia")
2. Buscar en el inventario consolidado
3. Asignar las evidencias que correspondan
4. Si no hay evidencias, marcar como "sin actividad en el periodo"

---

### PASO 9: Redactar justificacion por obligacion

**Estilo de redaccion:**
- **Conciso y directo**: Maximo 2-3 oraciones por obligacion
- **Sin relleno**: No parafrasear la obligacion ni repetir el titulo
- **Datos concretos**: Cantidades exactas (N commits, N tickets, nombres de documentos)
- **Ortografia:** Aplicar TODAS las reglas de "REGLAS DE ORTOGRAFIA ESPAÑOL" de CLAUDE.md
- **Primera persona + pasado**: "Realice la implementacion", "Atendi N solicitudes", "Desarrolle el modulo"
- **Sin calificativos**: No usar "gran esfuerzo", "significativo avance"
- **No inventar**: Solo actividades con evidencia documentada

**Con evidencias — Referenciar anexos por nombre del config.json:**
```
### Obligacion [N]
**[Texto completo de la obligacion]**

[1-3 oraciones directas.]

(Evidencia: [Nombre del anexo])
```

**Sin evidencias:**
```
### Obligacion [N]
**[Texto completo de la obligacion]**

Durante el periodo reportado no se adelantaron actividades relacionadas con esta obligacion.
```

---

### PASO 10: Organizar anexos en carpetas OBLIGACION_N

**Nota:** Las carpetas OBLIGACION_N/ pueden ya contener archivos copiados por buscar-evidencias PASO 6 (evidencias documentales del periodo). PASO 10 agrega los entregables estandar de config.json["anexos"] sin sobreescribir archivos existentes (usa `cp -n`).

Para cada anexo en `config.json["anexos"]`:

1. **Leer obligaciones:** Obtener el array `obligaciones` del anexo (ej: `[1, 3, 6]`)
2. **Localizar archivo fuente** segun `fuente_key`:

| fuente_key | Archivo en `{carpeta_fuentes}` |
|-----------|-------------------------------|
| `jira` | `jira_{entidad_lower}_{mes}.xlsx` |
| `commits` | `commits_{entidad_lower}_{mes}.docx` |
| `glpi` | `glpi_{entidad_lower}_{mes}.xlsx` |
| `correos` | `correos_soporte_{entidad_lower}_{mes}.docx` |
| `correos_general` | `correos_soporte_{entidad_lower}_{mes}.docx` |
| `reuniones` | `reuniones_{entidad_lower}_{mes}.docx` |
| `plan_accion` | `plan_accion_{entidad_lower}_{mes}.docx` |

3. **Para cada obligacion N** del array:
   - Crear carpeta: `mkdir -p "{carpeta_evidencias}/OBLIGACION_{N}/"`
   - Determinar nombre destino: si el anexo tiene `nombre_corto` → usar `nombre_corto`; si no → usar `nombre`
   - Copiar: `cp -n "{fuente}" "{carpeta_evidencias}/OBLIGACION_{N}/{nombre_destino}{extension}"`
4. **Si `manual == true`:** Buscar archivo existente por nombre parcial en carpeta_evidencias, carpeta_fuentes o carpeta_anual
5. **Si no se encuentra la fuente:** Registrar como "no generado" en log (no es error critico)

**Nota:** Un mismo archivo se copia a multiples carpetas OBLIGACION_N/ si aplica a varias obligaciones.

**Mapeo de renombrado:** Si algun anexo usa `nombre_corto`, registrar en log una tabla de mapeo:
| Nombre Original | Archivo Destino | Ruta |

**Registrar en log** — ver formato en `examples/log_formats.md#paso-10`

---

### PASO 11: Guardar informe final y log

Guardar informe con la estructura de ESTRUCTURA DE SALIDA en:
```
{carpeta_evidencias}/../Informe_Obligaciones_{$0}_{mes}_{year}.md
```

**NO guardar copia en `output/`.**

**Finalizar log** — ver formato en `examples/log_formats.md#paso-11`

---

## Ejemplos

### Ejemplo 1: Ejecucion estandar
User says: `/generar-informe IDARTES 2026-02-01 2026-02-28`
Actions:
1. Resuelve rutas, crea estructura de carpetas
2. Extrae tickets GLPI, Jira (background), Gmail (background), calendario
3. Resume reuniones, busca evidencias, genera commits y soportes
4. Consolida, mapea a obligaciones, redacta justificacion
5. Organiza anexos en OBLIGACION_N/, guarda informe final
Result: `Informe_Obligaciones_IDARTES_febrero_2026.md` + 9 carpetas OBLIGACION_N/ + log

### Ejemplo 2: Entidad sin API configurada
User says: `/generar-informe UAECD 2026-03-01 2026-03-31`
Actions:
1. PASO 2A: Outlook MCP no configurado → registra en log, continua
2. PASO 2D: Calendar Outlook no configurado → registra en log
3. Busca evidencias locales, genera commits, busca correos PDF (fallback)
Result: Informe generado con datos disponibles, log indica APIs no disponibles

---

## ESTRUCTURA DE SALIDA

**Ver formato completo en** `examples/estructura_salida.md`

---

## NOTAS ESPECIALES POR ENTIDAD

| Entidad | Consideraciones |
|---------|-----------------|
| IDARTES | Jira + Gmail como subagentes paralelos. Obligacion 8 = este informe + SECOP (manual). PASO 2C extrae correos Gmail suplementarios |
| SDMUJER | Incluir Plan de Accion TI (manual). Rol dual OSI + Desarrollo |
| IDT | PASO 2A usa subagente Gmail. Obligacion 5 = este informe. Obligacion 4 = soporte correo |
| UAECD | Enfasis en arquitectura (Oblig 1, 2, 4). Sin Jira ni GLPI. Outlook para correos |

---

## ARCHIVOS GENERADOS

Ver detalle completo en `examples/archivos_generados.md`

## FLUJO VISUAL

Ver diagrama completo en `examples/flujo_visual.md`
