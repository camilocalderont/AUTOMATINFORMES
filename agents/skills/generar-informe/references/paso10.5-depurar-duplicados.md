# PASO 10.5: Depurar duplicados de formato en OBLIGACIÓN_N/

Para cada carpeta `OBLIGACION_N/`, detectar archivos con el mismo nombre base pero diferente extensión:

```bash
for dir in "{carpeta_evidencias}"/OBLIGACION_*/; do
  ls "$dir" 2>/dev/null
done
```

## Regla de prelación

PDF > Word (.docx) > Markdown (.md)

Si coexisten:
- `archivo.pdf` + `archivo.docx` → eliminar `.docx`
- `archivo.pdf` + `archivo.md` → eliminar `.md`
- `archivo.docx` + `archivo.md` → eliminar `.md`

**Registrar en log:** Archivos eliminados por duplicado de formato.

**NOTA:** Solo aplica a archivos con el MISMO nombre base. Archivos con nombres distintos aunque tengan el mismo contenido NO se eliminan automáticamente.
