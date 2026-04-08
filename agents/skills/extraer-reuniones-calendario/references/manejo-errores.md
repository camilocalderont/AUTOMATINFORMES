# Manejo de errores — Extraer Reuniones Calendario

Si el MCP server no responde o falla la autenticación:

1. Registrar el error en el log/conversación
2. **Fallback manual:** Informar al usuario que puede proveer un archivo de reuniones manualmente (`.md`, `.csv` o `.xlsx`) en `{carpeta_fuentes}` con la lista de reuniones del período. Si el usuario provee el archivo, leerlo y generar el output normalmente.
3. Si no hay fallback disponible: terminar sin generar archivo, registrar en log "Calendar API no disponible, sin archivo manual"
4. Indicar pasos de solución según el tipo de calendario:

## Google Calendar
1. Verificar que el archivo de credenciales OAuth existe en `~/.google-calendar-mcp/`
2. Verificar que se habilitó "Google Calendar API" en Google Cloud Console
3. Re-autenticar: `GOOGLE_OAUTH_CREDENTIALS=~/.google-calendar-mcp/oauth-credentials.json npx @cocal/google-calendar-mcp auth`

## Outlook Calendar
1. Verificar que las variables de entorno del tenant están configuradas en `.env`
2. El MCP de Outlook debe tener permisos de Calendar (scope `Calendars.Read`)
