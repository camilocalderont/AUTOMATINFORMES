---
name: generar-informe
description: "Orchestrates complete monthly activity report generation for a government entity by running sub-skills sequentially: API extractions, evidence search, commits, support reports, meeting summaries. Use when user says \"generar informe\", \"generate report\", \"informe mensual\", or provides entity with date range. Produces OBLIGACION_N/ folders, Word/Excel deliverables, and final Markdown report."
argument-hint: "[ENTIDAD] [FECHA_INICIO] [FECHA_FIN]"
metadata:
  author: solercia
  version: "1.0.0"
  category: project-management
  tags: [informe, obligaciones, orquestador, entidades]
---

> **REGLAS OBLIGATORIAS** (R1-R7) — ver `agents/skills/shared/paso0-rutas.md#reglas-compactas`. Aplican sin excepción a este skill.

# Skill: Generar Informe Completo (Orquestador)

Orquesta la ejecución secuencial de sub-skills para generar el informe completo de una entidad.

## ENTRADA
- **$0**: Entidad (IDARTES, SDMUJER, IDT, UAECD)
- **$1**: Fecha inicio (YYYY-MM-DD)
- **$2**: Fecha fin (YYYY-MM-DD)

## PROCESO

### PASO 0: Resolver rutas e inicializar log

Ejecutar resolución estándar según `.claude/skills/shared/paso0-rutas.md`.
- `{dia_actual}` = `date +%Y-%m-%d`
- `{log_file}` = `{carpeta_mes}/log_{entidad_lower}_{mes}_{year}.md`
- Inicializar log con encabezado: título, período, fecha de ejecución

### PASO 0B: Verificar/crear estructura de carpetas

Verificar `{carpeta_mes}` y `{carpeta_evidencias}`. Si no existen → `mkdir -p`. Crear subcarpetas de `rutas.subcarpetas`.

**Registrar en log** — ver `examples/log_formats.md#paso-0b`

---

### PASO 1: Cargar configuración completa

Leer `entidades/$0/README.md` (obligaciones) y `entidades/$0/config.json` (rutas, correos, ramas). Extraer: lista de obligaciones, mapeo evidencias, `mesa_servicios.tipo`, estructura de `anexos`.

---

### PASO 2: Extraer insumos vía API

**Ver detalle completo en** `references/paso2-extracción-api.md`

| Sub-paso | Condición | Acción |
|----------|-----------|--------|
| 2A | glpi → `/extraer-tickets-glpi`; gmail → Agent subagente; outlook → `/extraer-correos-outlook` | Mesa de servicios |
| 2B | Si tiene `api.jira` | Agent background: `jira_extract.py` |
| 2C | Si glpi + gmail | Agent background: correo suplementario |
| 2D | Si tiene `api.calendar` | `/extraer-reuniones-calendario` |
| 2E | Siempre | `/resumen-reuniones` (espera a 2D) |

2B y 2C en **background**. 2D normal. 2E espera 2D. Si API falla → registrar en log, continuar.

**Registrar en log** — ver `examples/log_formats.md#paso-2`

---

### PASO 3: Ejecutar `/buscar-evidencias`

```
/buscar-evidencias $0 $1 $2
```

Esperar. Leer `{carpeta_evidencias}/evidencias_{entidad_lower}_{mes}.md`. Verificar que ejecutó los 3 `find` (2A, 2B, 2C). Si solo muestra FUENTES → repetir.

**Registrar en log** — ver `examples/log_formats.md#paso-3`

---

### PASO 4: Ejecutar `/generar-commits`

```
/generar-commits $0 $1 $2
```

Esperar. Leer `{carpeta_evidencias}/commits_{entidad_lower}_{mes}.md`.

**Registrar en log** — ver `examples/log_formats.md#paso-4`

---

### PASO 5: Ejecutar skill de soportes

- **correo** (IDT, UAECD): `/generar-soportes-correo $0 $1 $2`
- **glpi** (IDARTES, SDMUJER): `/generar-soportes-glpi $0 $1 $2`

**Registrar en log** — ver `examples/log_formats.md#paso-5`

---

### PASO 6: Ejecutar `/generar-plan-accion` (condicional)

**Solo si** `config.json["anexos"]` tiene `"fuente_key": "plan_accion"` (SDMUJER). Si no aplica → saltar.

```
/generar-plan-accion $0 $1 $2
```

---

### PASO 7: Consolidar inventario de evidencias

Unificar outputs: evidencias documentales + commits + soportes + issues Jira + reuniones + anexos estándar.

---

### PASO 8: Mapear evidencias a obligaciones

Para cada obligación del README.md: revisar mapeo → buscar en inventario → asignar. Sin evidencias → "sin actividad en el período".

---

### PASO 9: Redactar justificación por obligación

**Ver directrices y formato en** `references/paso9-redacción.md`

Resumen: primera persona + pasado, conciso (2-3 oraciones), datos concretos, sin calificativos, citar evidencia al final.

---

### PASO 9.5: Validar correos y evidencias complementarias

**Ver detalle en** `references/paso9.5-validación.md`

Validar PDFs de correo (pandoc → legibilidad). Verificar evidencias complementarias por obligación. NUNCA fabricar contenido (R7).

---

### PASO 10: Organizar anexos en carpetas OBLIGACION_N

**Ver tabla fuente_key y procedimiento en** `references/paso10-organizar-anexos.md`

Copiar entregables de `config.json["anexos"]` a OBLIGACION_N/ con `cp -n` (sin sobreescribir). Usar `nombre_corto` si existe.

**Registrar en log** — ver `examples/log_formats.md#paso-10`

---

### PASO 10.5: Depurar duplicados de formato

**Ver detalle en** `references/paso10.5-depurar-duplicados.md`

Prelación: PDF > Word > Markdown. Eliminar formatos menores si coexisten con mismo nombre base.

---

### PASO 11: Guardar informe final y log

Guardar en `{carpeta_evidencias}/../Informe_Obligaciones_{$0}_{mes}_{year}.md`. **Ver estructura en** `examples/estructura_salida.md`.

**Finalizar log** — ver `examples/log_formats.md#paso-11`

---

### PASO 12: Verificar coherencia informe vs evidencias

**Ver detalle en** `references/paso12-verificación.md`

```
/verificar-informe $0 $1 $2
```

Si FAIL → corregir. Si WARNING → reportar al usuario. Registrar resultado en log.

---

## Ejemplos

- **Estándar:** `/generar-informe IDARTES 2026-02-01 2026-02-28` → extrae GLPI+Jira+Gmail, busca evidencias, genera commits, soportes, consolida, organiza → Informe + 9 OBLIGACION_N/ + log
- **Sin API:** `/generar-informe UAECD 2026-03-01 2026-03-31` → APIs no disponibles, fallback a PDFs locales → Informe con datos disponibles

---

## NOTAS POR ENTIDAD

| Entidad | Consideraciones |
|---------|-----------------|
| IDARTES | Jira + Gmail como subagentes. Oblg 8 = informe + SECOP. PASO 2C correo suplementario |
| SDMUJER | Plan de Acción TI. Rol dual OSI + Desarrollo |
| IDT | PASO 2A usa subagente Gmail. Oblg 5 = este informe |
| UAECD | Énfasis arquitectura (Oblg 1,2,4). Sin Jira/GLPI. Outlook |

## ARCHIVOS GENERADOS

Ver `examples/archivos_generados.md`

## FLUJO VISUAL

Ver `examples/flujo_visual.md`
