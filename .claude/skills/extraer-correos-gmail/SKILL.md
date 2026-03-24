---
name: extraer-correos-gmail
description: "Extracts sent emails from Gmail for a specific entity and date range using the Gmail MCP server, including full email bodies and thread history (RE:/FW:). Generates Markdown report and Word document deliverable. Use when user says \"extraer correos gmail\", \"gmail emails\", \"extract gmail\", \"correos enviados gmail\", or needs sent email evidence for IDT or IDARTES."
argument-hint: "[ENTIDAD] [FECHA_INICIO] [FECHA_FIN]"
---

# Skill: Extraer Correos de Gmail

Extrae correos enviados desde la cuenta Gmail de la entidad en el periodo indicado, usando el MCP server correspondiente.

## ENTRADA
- **$0**: Entidad (IDT o IDARTES)
- **$1**: Fecha inicio (YYYY-MM-DD)
- **$2**: Fecha fin (YYYY-MM-DD)

## PROCESO

### PASO 0: Resolver rutas

Ejecutar la resolucion de rutas estandar segun `.claude/skills/shared/paso0-rutas.md`.

Verificar `{carpeta_evidencias}` existe; si no, buscar desde `{carpeta_mes}` o preguntar al usuario.

### PASO 1: Validar entidad y determinar MCP server

Mapeo de entidad a MCP server Gmail:

| Entidad | MCP Server | Cuenta |
|---------|-----------|--------|
| IDT | `gmail-idt` | (ver config.json api.gmail.cuenta) |
| IDARTES | `gmail-idartes` | (ver config.json api.gmail.cuenta) |

Si la entidad no tiene `api.gmail` en su config.json, informar al usuario y terminar.

### PASO 2: Buscar correos enviados en el periodo

Convertir fechas al formato Gmail:
- `$1` (YYYY-MM-DD) → `YYYY/MM/DD`
- `$2` (YYYY-MM-DD) → `YYYY/MM/DD`

Usar la herramienta `search_emails` del MCP server correspondiente:

```
query: "from:me after:{$1_gmail_format} before:{$2_gmail_format}"
```

**Nota:** El query `from:me` filtra solo correos enviados por el usuario autenticado.

Si `search_emails` no esta disponible, intentar con `gmail_search` u otra herramienta equivalente del MCP. Listar las herramientas disponibles si es necesario.

### PASO 3: Leer contenido COMPLETO de cada correo

Para cada correo encontrado, usar `read_email` (o `gmail_read_message`) para obtener:
- **Fecha**: Fecha de envio
- **Asunto**: Subject del correo
- **De**: Remitente completo
- **Para**: Destinatarios (To)
- **CC**: Copia (si existe)
- **Cuerpo COMPLETO**: Contenido integro del correo (NO resumen, NO truncado)

**IMPORTANTE - Hilo de correo:** Si el correo es una respuesta (asunto con "RE:" o "FW:"), usar `gmail_read_thread` (o `read_thread`) para obtener los mensajes anteriores del hilo. Para cada mensaje del hilo:
- De, Para, Fecha, Cuerpo completo

**Limite:** Si hay mas de 50 correos, procesar los 50 mas recientes e indicar que hay mas.

### PASO 4: Clasificar correos

Clasificar cada correo por tipo:
- **Soporte tecnico**: Resolucion de incidencias, bugs, errores
- **Soporte funcional**: Consultas de uso del sistema
- **Coordinacion**: Correos de gestion, seguimiento, reuniones
- **Reporte**: Envio de informes, avances, documentacion
- **Otro**: Correos que no encajan en las categorias anteriores

### PASO 5: Generar contenido

#### A) Resumen General
```
Durante el periodo reportado se enviaron [N] correos electronicos
desde la cuenta institucional, correspondientes a [N] soportes tecnicos,
[N] coordinaciones y [N] reportes.
```

#### B) Estadisticas
- Total correos enviados
- Correos por tipo/categoria
- Destinatarios frecuentes (dominios)

#### C) Tabla de Correos
| # | Fecha | Asunto | Destinatarios | Tipo | Resumen |
|---|-------|--------|---------------|------|---------|
| 1 | 2026-02-05 | RE: Error modulo X | usuario@entidad.gov.co | Soporte | Se indico solucion... |

### PASO 6: Guardar output

Guardar el contenido generado en:
```
{carpeta_evidencias}/correos_api_{entidad_lower}_{mes}.md
```

Ejemplo: `.../ANEXOS/correos_api_idt_febrero.md`

**Tambien mostrar el resultado en la conversacion** para que el usuario pueda revisarlo.

### PASO 7: Generar documento Word de correos

1. Resolver `{carpeta_fuentes}` desde `config.json rutas.carpeta_fuentes`:
   - Reemplazar `{carpeta_evidencias}` en el valor de `rutas.carpeta_fuentes`
   - Si `rutas.carpeta_fuentes` no existe en config → usar `{carpeta_evidencias}/FUENTES/`
   - Ejecutar: `mkdir -p "{carpeta_fuentes}"`

2. Generar JSON intermedio con los datos extraidos:
   - Archivo: `{carpeta_fuentes}/_correos_data_{entidad_lower}_{mes}.json`
   - **Estructura JSON:** ver `references/json_structure.md`
   - **IMPORTANTE:** El campo `cuerpo` debe contener el texto COMPLETO del correo, no un resumen

3. Ejecutar el script de generacion:
```bash
python3 scripts/correos_to_docx.py "{carpeta_fuentes}/_correos_data_{entidad_lower}_{mes}.json" "{carpeta_fuentes}/correos_soporte_{entidad_lower}_{mes}.docx"
```

4. Si el script termina correctamente:
   - Eliminar el JSON intermedio: `rm "{carpeta_fuentes}/_correos_data_{entidad_lower}_{mes}.json"`
   - Informar: "Word generado: `{carpeta_fuentes}/correos_soporte_{entidad_lower}_{mes}.docx`"

5. Si el script falla:
   - Informar el error pero NO detener la ejecucion (el .md ya se genero en PASO 6)

## MANEJO DE ERRORES

- Si el MCP server no responde o falla la autenticacion OAuth:
  1. Verificar que las credenciales OAuth existan en `~/.gmail-mcp/`
  2. Si es primera ejecucion, indicar que debe abrir el browser para autorizar
  3. Si el token expiro, eliminar el archivo de credentials y re-autorizar
- Si Google Workspace bloquea OAuth de terceros, informar al usuario que necesita solicitar autorizacion al admin de IT

## Ejemplos

### Ejemplo 1: Extraccion estandar
User says: `/extraer-correos-gmail IDT 2026-02-01 2026-02-28`
Actions:
1. Conecta a gmail-idt MCP, busca "from:me after:2026/02/01 before:2026/02/28"
2. Encuentra 22 correos, lee contenido completo de cada uno
3. Clasifica: 10 soporte, 7 coordinacion, 5 reporte
4. Genera .md con tabla y .docx via correos_to_docx.py
Result: `correos_api_idt_febrero.md` + `correos_soporte_idt_febrero.docx`

### Ejemplo 2: MCP no disponible
User says: `/extraer-correos-gmail IDARTES 2026-02-01 2026-02-28`
Actions:
1. ToolSearch no encuentra herramientas Gmail
2. Informa: "Gmail MCP server not connected"
3. Sugiere: usar /generar-soportes-correo con PDF exportado
Result: No genera archivos, usuario dirigido a flujo alternativo

## ARCHIVOS GENERADOS

| Campo | Valor |
|-------|-------|
| Nombre MD | `correos_api_{entidad_lower}_{mes}.md` |
| Ubicacion MD | `{carpeta_evidencias}/` |
| Nombre DOCX | `correos_soporte_{entidad_lower}_{mes}.docx` |
| Ubicacion DOCX | `{carpeta_fuentes}/` |
| Ejemplo MD | `.../ANEXOS/correos_api_idt_febrero.md` |
| Ejemplo DOCX | `.../FUENTES/correos_soporte_idt_febrero.docx` |
