---
name: extraer-issues-jira
description: "Extracts completed Jira issues (statusCategory=Done) for a specific entity and period using jira_extract.py with Jira Cloud REST API. Generates Markdown report and Excel deliverable with issue details. Use when user says \"extraer jira\", \"jira issues\", \"extract jira tickets\", \"issues finalizados\", or needs Jira evidence. Currently only IDARTES."
argument-hint: "[ENTIDAD] [FECHA_INICIO] [FECHA_FIN]"
metadata:
  author: solercia
  version: "1.0.0"
  category: data-processing
  tags: [jira, issues, api, extracción]
---

# Skill: Extraer Issues Finalizados de Jira

Extrae issues **finalizados** (statusCategory = Done) de Jira Cloud asignadas al usuario y resueltos en el periodo indicado, usando el script `jira_extract.py`.

## ENTRADA
- **$0**: Entidad (actualmente solo IDARTES)
- **$1**: Fecha inicio (YYYY-MM-DD)
- **$2**: Fecha fin (YYYY-MM-DD)

## PROCESO

### PASO 0: Resolver rutas

Ejecutar la resolucion de rutas estandar segun `.claude/skills/shared/paso0-rutas.md`.

Verificar `{carpeta_evidencias}` existe; si no, buscar desde `{carpeta_mes}` o preguntar al usuario.

### PASO 1: Validar entidad y configuracion API

1. Solo IDARTES tiene Jira configurado. Si la entidad no tiene `api.jira` en su config.json, informar al usuario y terminar.
2. Verificar que `scripts/jira_extract.py` exista.

### PASO 2: Ejecutar script de extraccion

El script `scripts/jira_extract.py` usa la REST API directa de Jira Cloud (endpoint `/rest/api/3/search/jql`). No depende del MCP server ya que `mcp-atlassian` usa el endpoint deprecado `/rest/api/3/search`.

**IMPORTANTE:** El script solo extrae issues con `statusCategory = Done` (finalizados/cerrados) cuya fecha de resolucion (`resolved`) este dentro del rango indicado. Issues pendientes, en progreso o por hacer NO se incluyen.

1. Definir la ruta de salida del .md:
```
{output_md} = {carpeta_evidencias}/jira_issues_{entidad_lower}_{mes}.md
```

2. Resolver `{carpeta_fuentes}` desde `config.json rutas.carpeta_fuentes`:
   - Reemplazar `{carpeta_evidencias}` en el valor de `rutas.carpeta_fuentes`
   - Si `rutas.carpeta_fuentes` no existe en config → usar `{carpeta_evidencias}/FUENTES/`
   - Ejecutar: `mkdir -p "{carpeta_fuentes}"`

3. Definir la ruta de salida del .xlsx:
```
{xlsx_path} = {carpeta_fuentes}/jira_{entidad_lower}_{mes}.xlsx
```

4. Ejecutar con ambas salidas:
```bash
python3 scripts/jira_extract.py $0 $1 $2 "{output_md}" --output-xlsx "{xlsx_path}"
```

**Configuracion del JQL** se lee automaticamente desde `config.json api.jira`:
- `proyecto`: Clave del proyecto Jira (ej: "CP")
- `account_id`: ID de cuenta Atlassian del usuario
- `jql_base`: Template JQL con placeholders `{proyecto}`, `{account_id}`, `{fecha_inicio}`, `{fecha_fin}`

**Prerequisitos en `.env`:**
```
JIRA_{ENTIDAD}_EMAIL=usuario@entidad.gov.co
JIRA_{ENTIDAD}_API_TOKEN=<token clasico de id.atlassian.com>
```

**IMPORTANTE:** El API token debe ser **clasico** (no granular/scoped). Los tokens granulares (ATATT3...) pueden fallar con "scope does not match" si no tienen los permisos correctos.

### PASO 3: Verificar resultado

- Si el script termina con exit code 0:
  - Leer el archivo .md generado en `{output_md}`
  - Mostrar el contenido en la conversacion
  - Informar si el Excel fue generado: `{xlsx_path}`
- Si falla:
  - Mostrar el error al usuario
  - Indicar posibles causas:
    1. Variables de entorno no configuradas (`.env`)
    2. API Token invalido o expirado
    3. Token granular en vez de clasico
    4. `account_id` o `proyecto` incorrectos en config.json

## MANEJO DE ERRORES

- Si el script falla o la API no responde:
  1. Registrar el error en el log/conversacion
  2. **Fallback a archivo local:** Buscar un archivo CSV o XLSX de Jira en `{carpeta_fuentes}`:
     ```bash
     find "{carpeta_fuentes}" -type f \( -name "*jira*.csv" -o -name "*jira*.xlsx" -o -name "*issues*.csv" -o -name "*issues*.xlsx" \) 2>/dev/null
     ```
  3. Si se encuentra archivo local: leerlo con `read_document` (xlsx) o `Read` (csv) y generar el .md con la informacion disponible
  4. Si NO se encuentra archivo local: registrar en log "Jira API no disponible y no se encontro archivo local" y terminar sin generar archivos
  5. Informar al usuario las posibles causas del fallo API:
     - Variables de entorno no configuradas (`JIRA_IDARTES_EMAIL`, `JIRA_IDARTES_API_TOKEN` en `.env`)
     - API Token expirado — renovar en https://id.atlassian.com/manage-profile/security/api-tokens
     - Token granular en vez de clasico
     - Reiniciar Claude Code para recargar configuracion

## MAPEO A OBLIGACIONES (IDARTES)

**Solo issues finalizados se incluyen en la redaccion del informe.** Issues pendientes o en progreso no se mencionan.

| Tipo de Issue | Obligacion |
|---------------|------------|
| Stories (funcionalidades nuevas) | 1 |
| Bugs (correcciones) | 1, 6 |
| Tasks de seguridad | 3 |
| Tasks de refactorizacion/calidad | 6 |

## Ejemplos

### Ejemplo 1: Extraccion exitosa
User says: `/extraer-issues-jira IDARTES 2026-02-01 2026-02-28`
Actions:
1. Lee config IDARTES, verifica api.jira configurado
2. Ejecuta jira_extract.py con JQL filtrado por statusCategory=Done
3. Encuentra 8 issues finalizados (3 stories, 4 bugs, 1 task)
4. Genera .md con tabla detallada y .xlsx
Result: `jira_issues_idartes_febrero.md` + `jira_idartes_febrero.xlsx`

### Ejemplo 2: API token expirado
User says: `/extraer-issues-jira IDARTES 2026-03-01 2026-03-31`
Actions:
1. Ejecuta jira_extract.py → falla con error 401
2. Muestra error e indica: verificar API token en .env, renovar en id.atlassian.com
Result: No genera archivos, sugiere pasos de solucion

## ARCHIVOS GENERADOS

| Campo | Valor |
|-------|-------|
| Nombre MD | `jira_issues_{entidad_lower}_{mes}.md` |
| Ubicacion MD | `{carpeta_evidencias}/` |
| Nombre Excel | `jira_{entidad_lower}_{mes}.xlsx` |
| Ubicacion Excel | `{carpeta_fuentes}/` |
| Ejemplo MD | `.../ANEXOS/jira_issues_idartes_febrero.md` |
| Ejemplo Excel | `.../FUENTE/jira_idartes_febrero.xlsx` |
