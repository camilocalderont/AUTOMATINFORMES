# Generación de Excel GLPI (PASO 4B)

## Verificación previa

Verificar si ya existe un Excel generado por la API:

```bash
ls "{carpeta_fuentes}/glpi_{entidad_lower}_{mes}.xlsx" 2>/dev/null
```

- **Si ya existe:** Saltar este paso (la API ya lo generó).
- **Si NO existe** y se procesaron tickets (desde CSV/Excel local en PASO 3): continuar.

## Procedimiento

1. Resolver `{carpeta_fuentes}` desde `rutas.carpeta_fuentes` en config.json (fallback: `{carpeta_evidencias}/FUENTES/`)
2. Construir JSON intermedio con los datos parseados del archivo local:

```json
{
    "entidad": "{$0}",
    "periodo_inicio": "{$1}",
    "periodo_fin": "{$2}",
    "total": N,
    "tickets": [
        {
            "id": "12345",
            "titulo": "Título del ticket",
            "tipo": "Incidencia",
            "estado": "Cerrado",
            "fecha_apertura": "YYYY-MM-DD",
            "fecha_cierre": "YYYY-MM-DD",
            "prioridad": "Media",
            "categoria": "Software",
            "solicitante": "usuario@entidad.gov.co",
            "solucion": "Descripción de la solución..."
        }
    ]
}
```

3. Escribir JSON intermedio en: `{carpeta_fuentes}/_glpi_data_{entidad_lower}_{mes}.json`
4. Ejecutar:

```bash
python3 scripts/glpi_to_excel.py "{carpeta_fuentes}/_glpi_data_{entidad_lower}_{mes}.json" "{carpeta_fuentes}/glpi_{entidad_lower}_{mes}.xlsx"
```

5. Si exitoso: eliminar JSON intermedio
6. Informar: "Excel generado: `{carpeta_fuentes}/glpi_{entidad_lower}_{mes}.xlsx`"
