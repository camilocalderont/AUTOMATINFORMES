# PASO 4: Lectura de archivos — detalle

## Para documentos Office y PDF

Usa el MCP `awslabs.document-loader-mcp-server`:

```
Herramienta: read_document
Servidor: user-awslabs.document-loader-mcp-server
Argumentos:
  - file_path: [ruta completa del archivo]
  - file_type: [docx|xlsx|pdf|pptx]
```

**Fallback si `read_document` falla:** Si el MCP no responde o devuelve error para un archivo:
1. Registrar el archivo en una lista de **"archivos no leídos por MCP"**
2. Intentar leer con la herramienta `Read` nativa de Claude Code (funciona para .docx y .xlsx como texto parcial)
3. Si `Read` tampoco puede extraer contenido útil, convertir los archivos a markdown con pandoc o similares y leer el archivo en texto.
4. Si hay problemas convirtiendo a markdown, entonces registrar el archivo como **"no leído"** y continuar con el siguiente
5. Al final del PASO 4, **alertar en la salida** listando todos los archivos que no se pudieron leer:
```
**Alerta:** Los siguientes archivos no pudieron ser leídos por read_document:
- [nombre_archivo.xlsx] — [motivo del error]
- [nombre_archivo.pdf] — [motivo del error]
Se recomienda verificar que el MCP document-loader esté activo.
```

## Para archivos de texto

Usa la herramienta `Read` nativa de Claude Code.

## Para imágenes

Usa el MCP con `read_image`:

```
Herramienta: read_image
Servidor: user-awslabs.document-loader-mcp-server
Argumentos:
  - file_path: [ruta completa del archivo]
```
