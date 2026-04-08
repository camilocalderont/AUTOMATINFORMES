# PASO 10: Organizar anexos en carpetas OBLIGACIÓN_N

**Nota:** Las carpetas OBLIGACION_N/ pueden ya contener archivos copiados por buscar-evidencias PASO 6 (evidencias documentales del período). PASO 10 agrega los entregables estándar de config.json["anexos"] sin sobreescribir archivos existentes (usa `cp -n`).

## Procedimiento

Para cada anexo en `config.json["anexos"]`:

1. **Leer obligaciones:** Obtener el array `obligaciones` del anexo (ej: `[1, 3, 6]`)
2. **Localizar archivo fuente** según `fuente_key`:

| fuente_key | Archivo en `{carpeta_fuentes}` |
|-----------|-------------------------------|
| `jira` | `jira_{entidad_lower}_{mes}.xlsx` |
| `commits` | `commits_{entidad_lower}_{mes}.docx` |
| `glpi` | `glpi_{entidad_lower}_{mes}.xlsx` |
| `correos` | `correos_soporte_{entidad_lower}_{mes}.docx` |
| `correos_general` | `correos_soporte_{entidad_lower}_{mes}.docx` |
| `reuniones` | `reuniones_{entidad_lower}_{mes}.docx` |
| `plan_accion` | `plan_accion_{entidad_lower}_{mes}.docx` |

3. **Para cada obligación N** del array:
   - Crear carpeta: `mkdir -p "{carpeta_evidencias}/OBLIGACION_{N}/"`
   - Determinar nombre destino: si el anexo tiene `nombre_corto` → usar `nombre_corto`; si no → usar `nombre`
   - Copiar: `cp -n "{fuente}" "{carpeta_evidencias}/OBLIGACION_{N}/{nombre_destino}{extension}"`
4. **Si `manual == true`:** Buscar archivo existente por nombre parcial en carpeta_evidencias, carpeta_fuentes o carpeta_anual
5. **Si no se encuentra la fuente:** Registrar como "no generado" en log (no es error crítico)

**Nota:** Un mismo archivo se copia a múltiples carpetas OBLIGACION_N/ si aplica a varias obligaciones.

## Mapeo de renombrado

Si algún anexo usa `nombre_corto`, registrar en log una tabla de mapeo:

| Nombre Original | Archivo Destino | Ruta |
|----------------|-----------------|------|
