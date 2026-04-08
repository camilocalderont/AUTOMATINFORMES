# Mapeo a obligaciones y referencia de uso

## Mapeo a obligaciones

| Entidad | Obligación | Texto |
|---------|------------|-------|
| IDARTES | 2 | Realizar el soporte técnico de acuerdo con la asignación realizada por la mesa de servicios... |
| SDMUJER | 4 | Atender de forma correcta y oportuna los requerimientos internos... |

## Ejemplo de uso

```
# Con auto-localización de archivo
/generar-soportes-glpi IDARTES 2026-01-01 2026-01-31

# Con ruta específica
/generar-soportes-glpi IDARTES 2026-01-01 2026-01-31 /path/to/glpi_enero.xlsx
```

## Archivo generado

| Campo | Valor |
|-------|-------|
| Nombre | `soportes_glpi_{entidad_lower}_{mes}.md` |
| Ubicación | `{carpeta_evidencias}/` |
| Ejemplo | `.../01. ENERO/ANEXOS/soportes_glpi_idartes_enero.md` |
