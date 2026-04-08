---
name: generar-soportes-glpi
description: "Processes GLPI support tickets (API-first with fallback to local Excel/CSV) to generate a justified support obligation report with statistics, ticket categorization, and detail table. Generates Excel deliverable. Use when user says \"generar soportes glpi\", \"GLPI report\", \"support tickets report\", or needs helpdesk evidence for IDARTES or SDMUJER."
argument-hint: "[ENTIDAD] [FECHA_INICIO] [FECHA_FIN]"
metadata:
  author: solercia
  version: "1.0.0"
  category: documentation
  tags: [glpi, soporte, mesa-servicios, tickets]
  model: sonnet
---

> **REGLAS OBLIGATORIAS** (R1-R7) — ver `agents/skills/shared/paso0-rutas.md#reglas-compactas`. Aplican sin excepción a este skill.


# Skill: Generar Reporte de Soportes GLPI

## ENTRADA
- **$0**: Entidad (IDARTES, SDMUJER)
- **$1**: Fecha inicio (YYYY-MM-DD)
- **$2**: Fecha fin (YYYY-MM-DD)
- **$3** *(opcional)*: Ruta al archivo GLPI (.xlsx o .csv). Si no se proporciona, se auto-localiza.

## PROCESO

### PASO 0: Resolver rutas

Ejecutar la resolución de rutas estándar según `.claude/skills/shared/paso0-rutas.md`.

**Variables adicionales de este skill:**
- `{dia_actual}` = `date +%Y-%m-%d`
- Verificar `{carpeta_evidencias}` existe; si no, buscar desde `{carpeta_mes}` o preguntar al usuario.

### PASO 1: Validar entidad
Solo IDARTES y SDMUJER usan GLPI. Si la entidad es IDT o UAECD, indicar que deben usar `/generar-soportes-correo`.

### PASO 1.5: Intentar extracción vía API (si disponible)

**Nota:** Si se proporcionó $3 (ruta a archivo), saltar este paso completo y usar el archivo directamente.

**PASO 1.5A: Verificar extracción previa**

Antes de llamar la API, verificar si ya existe el archivo de extracción API en `{carpeta_evidencias}`:
```bash
ls "{carpeta_evidencias}/tickets_glpi_api_{entidad_lower}_{mes}.md" 2>/dev/null
```

- **Si existe** → Leer ese archivo y usarlo como base para generar el reporte de soportes. **Saltar a PASO 4** (no re-extraer).
- **Si NO existe** → Continuar a PASO 1.5B.

**PASO 1.5B: Extraer via API**

Verificar si la entidad tiene `api.glpi` configurada en `config.json`:

1. **Si tiene `api.glpi`:**
   - Ejecutar `/extraer-tickets-glpi $0 $1 $2`
   - Si la extraccion es exitosa:
     - El output se guarda en `{carpeta_evidencias}/tickets_glpi_api_{entidad_lower}_{mes}.md`
     - Leer ese archivo y usarlo como base para generar el reporte de soportes
     - **Saltar a PASO 4** (ya se tiene el contenido de los tickets)
   - Si falla (variables de entorno no configuradas, API no habilitada, etc.):
     - Registrar el error en la conversacion
     - Continuar a PASO 2 (fallback a archivo Excel local)

2. **Si NO tiene `api.glpi` configurada:**
   - Continuar a PASO 2 (flujo actual sin cambios)

### PASO 2: Localizar archivo GLPI

**Si $3 fue proporcionado:** Usar esa ruta directamente.

**Si $3 NO fue proporcionado:** Auto-localizar en 3 niveles (FUENTES → carpeta_evidencias → carpeta_anual). Usar el primer nivel con resultados; si hay varios archivos, usar el más reciente.

**Ver detalle en** `references/busqueda-archivo.md`

**Si no se encuentra ningún archivo Y la API tampoco generó datos (PASO 1.5):**
- NO solicitar ruta manualmente
- Redactar el reporte indicando: "Durante el periodo reportado no se registraron solicitudes de soporte a traves de la mesa de servicios GLPI."
- Saltar a PASO 6 (guardar output con el mensaje de no actividad)

### PASO 3: Leer archivo GLPI
Usar MCP `read_document` para archivos Excel:
```json
{
  "file_path": "{ruta_archivo}",
  "file_type": "xlsx"
}
```

**Fallback si `read_document` falla:** Si el MCP no responde, intentar leer el archivo con la herramienta `Read` nativa. Si es `.xlsx` y no se puede parsear, alertar al usuario indicando el archivo que no pudo leerse y sugerir exportar a `.csv`.

Para CSV, usar la herramienta `Read` nativa.

### PASO 4: Extraer informacion relevante
De cada ticket extraer:
- Numero de ticket
- Fecha de apertura
- Fecha de cierre
- Estado
- Titulo/Descripcion
- Tiempo de resolucion

### PASO 4B: Generar Excel (si no existe)

Si ya existe `{carpeta_fuentes}/glpi_{entidad_lower}_{mes}.xlsx` (generado por API), saltar. Si no existe y se procesaron tickets desde CSV/Excel local: construir JSON intermedio → ejecutar `glpi_to_excel.py` → eliminar JSON.

**Ver detalle en** `references/generacion-excel.md`

### PASO 5: Generar contenido

#### A) Resumen General
```
Durante el periodo reportado atendí [N] solicitudes a traves
de la mesa de servicios GLPI, correspondientes a [categorias].
Se logro un cumplimiento del [X]% en los ANS establecidos.
```

#### B) Estadisticas
- Total de tickets atendidos
- Tickets por categoria
- Tiempo promedio de resolucion
- Porcentaje de cumplimiento ANS

#### C) Tabla de Tickets
| Ticket | Fecha Apertura | Fecha Cierre | Estado | Descripcion |
|--------|----------------|--------------|--------|-------------|

### PASO 6: Guardar output

Guardar el contenido generado en:
```
{carpeta_evidencias}/soportes_glpi_{entidad_lower}_{mes}.md
```

Ejemplo: `.../ANEXOS/soportes_glpi_idartes_enero.md`

**Tambien mostrar el resultado en la conversacion** para que el usuario pueda revisarlo.

## DIRECTRICES DE REDACCION

1. **Primera persona + pasado**: "Atendí N solicitudes", "Resolví el incidente", "Gestioné los requerimientos"
2. **Claro y verificable**: Cantidades exactas de tickets, categorias
3. **Sin calificativos**: Evitar "rapida atencion", "excelente servicio"
4. **Objetivo**: Justificar la obligacion de soporte tecnico
5. **Evidencia**: Referenciar el anexo correspondiente de config.json (`anexos.soportes`)
6. **Ortografia:** Aplicar TODAS las reglas de "REGLAS DE ORTOGRAFIA ESPAÑOL" de CLAUDE.md

## Ejemplos

### Ejemplo 1: Extraccion via API
User says: `/generar-soportes-glpi IDARTES 2026-02-01 2026-02-28`
Actions:
1. PASO 1.5A: No existe archivo previo
2. PASO 1.5B: Ejecuta /extraer-tickets-glpi → genera .md y .xlsx
3. PASO 4: Lee el .md generado por API
4. PASO 5: Genera contenido con resumen, estadisticas y tabla
Result: `soportes_glpi_idartes_febrero.md` + `glpi_idartes_febrero.xlsx`

### Ejemplo 2: Fallback a archivo local
User says: `/generar-soportes-glpi SDMUJER 2026-02-01 2026-02-28 /ruta/glpi_febrero.xlsx`
Actions:
1. Salta PASO 1.5 (se proporciono $3)
2. Lee archivo con MCP read_document
3. Extrae tickets, genera reporte
4. Genera Excel via glpi_to_excel.py
Result: `soportes_glpi_sdmujer_febrero.md` + `glpi_sdmujer_febrero.xlsx`

## MAPEO, USO Y ARCHIVO GENERADO

**Ver detalle en** `references/referencia-obligaciones.md`

- **Obligaciones:** IDARTES→2, SDMUJER→4
- **Archivo:** `{carpeta_evidencias}/soportes_glpi_{entidad_lower}_{mes}.md`
