# Estructura JSON — correos_to_docx.py (Outlook)

Archivo intermedio: `{carpeta_fuentes}/_correos_data_{entidad_lower}_{mes}.json`

```json
{
    "entidad": "{$0}",
    "periodo_inicio": "{$1}",
    "periodo_fin": "{$2}",
    "cuenta": "{cuenta del config.json api.outlook.cuenta}",
    "total": N,
    "correos": [
        {
            "num": 1,
            "fecha": "2026-02-05",
            "asunto": "RE: Error modulo X",
            "de": "usuario@entidad.gov.co",
            "para": "usuario@entidad.gov.co",
            "cc": "otro@entidad.gov.co",
            "cuerpo": "Texto COMPLETO del correo incluyendo todo el contenido...",
            "hilo": [
                {
                    "de": "usuario@entidad.gov.co",
                    "para": "usuario@entidad.gov.co",
                    "fecha": "2026-02-04",
                    "cuerpo": "Texto completo del mensaje anterior en el hilo..."
                }
            ]
        }
    ]
}
```

## Reglas del JSON

- **IMPORTANTE:** El campo `cuerpo` debe contener el texto COMPLETO del correo, no un resumen
- El campo `hilo` es una lista de mensajes anteriores (solo si el correo es respuesta/reenvio)
- Si no hay hilo, usar lista vacia `[]`
- Escribir el JSON usando la herramienta Write
