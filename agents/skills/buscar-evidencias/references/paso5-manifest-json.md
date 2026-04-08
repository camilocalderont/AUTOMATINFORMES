# PASO 5.5: Estructura del manifest JSON

Escribir un archivo JSON en:
```
{carpeta_evidencias}/_manifest_evidencias_{entidad_lower}_{mes}.json
```

## Estructura

```json
{
  "carpeta_evidencias": "{carpeta_evidencias}",
  "archivos": [
    {
      "ruta": "/ruta/completa/archivo.docx",
      "obligaciones": [1, 3],
      "accion": "copy"
    }
  ]
}
```

## Reglas para determinar `accion`

- Archivos **dentro** de `{carpeta_evidencias}/` → `"move"` (se reubican a OBLIGACION_N/)
- Archivos **fuera** de `{carpeta_evidencias}/` (carpeta_anual, carpeta_fuentes) → `"copy"` (se copian, original intacto)
- Solo incluir archivos que tengan al menos una obligación asignada
- Archivos sin obligaciones asignadas → NO incluir en el manifest
