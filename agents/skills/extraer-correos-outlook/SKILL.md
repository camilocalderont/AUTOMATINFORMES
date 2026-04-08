---
name: extraer-correos-outlook
description: Extracts sent emails from Outlook/Microsoft 365 for a specific entity and date range using the MS-365 MCP server, including full email bodies and thread history. Generates Markdown report and Word document deliverable. Use when user says "extraer correos outlook", "outlook emails", "extract outlook", "correos enviados outlook", or needs sent email evidence for SDMUJER or UAECD.
argument-hint: "[ENTIDAD] [FECHA_INICIO] [FECHA_FIN]"
metadata:
  author: solercia
  version: "1.0.0"
  category: data-processing
  tags: [outlook, correos, api, extracción]
  mcp-server: outlook-sdmujer
  model: sonnet
---

> **REGLAS OBLIGATORIAS** (R1-R7) — ver `agents/skills/shared/paso0-rutas.md#reglas-compactas`. Aplican sin excepción a este skill.


# Skill: Extraer Correos de Outlook (Microsoft 365)

Extrae correos enviados desde la cuenta Outlook/M365 de la entidad en el periodo indicado, usando el MCP server correspondiente (`@softeria/ms-365-mcp-server`).

## ENTRADA
- **$0**: Entidad (SDMUJER o UAECD)
- **$1**: Fecha inicio (YYYY-MM-DD)
- **$2**: Fecha fin (YYYY-MM-DD)

## PROCESO

### PASO 0: Resolver rutas

Ejecutar la resolucion de rutas estandar segun `.claude/skills/shared/paso0-rutas.md`.

Verificar `{carpeta_evidencias}` existe; si no, buscar desde `{carpeta_mes}` o preguntar al usuario.

### PASO 1: Validar entidad y determinar MCP server

Mapeo de entidad a MCP server Outlook:

| Entidad | MCP Server | Cuenta |
|---------|-----------|--------|
| SDMUJER | `outlook-sdmujer` | (ver config.json api.outlook.cuenta) |
| UAECD | `outlook-uaecd` | (ver config.json api.outlook.cuenta) |

Si la entidad no tiene `api.outlook` en su config.json, informar al usuario y terminar.

### PASO 2: Obtener correos de Sent Items

Usar la herramienta `list-mail-folder-messages` del MCP server correspondiente para obtener correos de la carpeta "Sent Items" (Elementos enviados):

```
folder: "SentItems"
filter: "sentDateTime ge {$1}T00:00:00Z and sentDateTime le {$2}T23:59:59Z"
top: 100
```

**Nota:** Si `list-mail-folder-messages` no esta disponible, intentar con `list-mail-messages`, `search-mail` u otra herramienta equivalente del MCP. Listar las herramientas disponibles si es necesario.

### PASO 3: Leer contenido COMPLETO de cada correo

Para cada correo, extraer:
- **Fecha**: sentDateTime
- **Asunto**: subject
- **De**: from (remitente completo)
- **Para**: toRecipients
- **CC**: ccRecipients (si existe)
- **Cuerpo COMPLETO**: body.content (texto integro, NO bodyPreview)

**IMPORTANTE - Hilo de correo:** Si el correo es una respuesta (asunto con "RE:" o "FW:"), usar `get-mail-message` con el conversationId para obtener los mensajes anteriores del hilo. Para cada mensaje del hilo:
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

Ejemplo: `.../ANEXOS/correos_api_uaecd_febrero.md`

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

- Si el MCP server no responde o falla la autenticacion:
  1. Verificar que `.env` tenga las variables `{ENTIDAD}_TENANT_ID`, `{ENTIDAD}_CLIENT_ID`, `{ENTIDAD}_CLIENT_SECRET`
  2. Verificar que el admin de IT haya registrado la app en Azure AD con permisos `Mail.Read`
  3. Verificar que se haya otorgado admin consent
- Si Azure AD no es viable (IT no coopera):
  - Informar al usuario que debe mantener el flujo manual de exportar PDF desde Outlook
  - El fallback en `generar-soportes-correo` se encargara de buscar el PDF

## PREREQUISITOS

**Requieren accion del admin de IT** — ver detalle en `references/prerequisitos.md`

## EJEMPLO DE USO

```
/extraer-correos-outlook UAECD 2026-02-01 2026-02-28
/extraer-correos-outlook SDMUJER 2026-02-01 2026-02-28
```

## Ejemplos

### Ejemplo 1: Extraccion exitosa
User says: `/extraer-correos-outlook UAECD 2026-02-01 2026-02-28`
Actions:
1. Conecta a outlook-uaecd MCP
2. Lista correos de SentItems filtrados por fecha
3. Lee 15 correos completos con hilos
4. Clasifica y genera .md + .docx
Result: `correos_api_uaecd_febrero.md` + `correos_soporte_uaecd_febrero.docx`

### Ejemplo 2: Credenciales no configuradas
User says: `/extraer-correos-outlook SDMUJER 2026-02-01 2026-02-28`
Actions:
1. MCP server outlook-sdmujer no responde
2. Indica: verificar SDMUJER_TENANT_ID, CLIENT_ID, CLIENT_SECRET en .env
3. Sugiere: solicitar registro de app en Azure AD al admin de IT
Result: No genera archivos, muestra pasos de solucion

## ARCHIVOS GENERADOS

| Campo | Valor |
|-------|-------|
| Nombre MD | `correos_api_{entidad_lower}_{mes}.md` |
| Ubicacion MD | `{carpeta_evidencias}/` |
| Nombre DOCX | `correos_soporte_{entidad_lower}_{mes}.docx` |
| Ubicacion DOCX | `{carpeta_fuentes}/` |
| Ejemplo MD | `.../ANEXOS/correos_api_uaecd_febrero.md` |
| Ejemplo DOCX | `.../FUENTES/correos_soporte_uaecd_febrero.docx` |
