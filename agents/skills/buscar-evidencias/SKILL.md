---
name: buscar-evidencias
description: "Searches for files created or modified during a reporting period across annual, evidence, and source folders using 3 find commands, reads content via MCP document-loader, classifies by obligation, and organizes into OBLIGACION_N/ folders. Use when user says \"buscar evidencias\", \"search evidence\", \"find period files\", or needs to inventory deliverables before report generation."
argument-hint: "[ENTIDAD] [FECHA_INICIO] [FECHA_FIN]"
metadata:
  author: solercia
  version: "1.0.0"
  category: data-processing
  tags: [evidencias, find, archivos, obligaciones]
  mcp-server: document-loader
---

> **REGLAS OBLIGATORIAS** (R1-R7) — ver `agents/skills/shared/paso0-rutas.md#reglas-compactas`. Aplican sin excepción a este skill.


# Skill: Buscar y Leer Evidencias del Período

## ENTRADA
- **$0**: Entidad (IDARTES, SDMUJER, IDT, UAECD)
- **$1**: Fecha inicio (YYYY-MM-DD)
- **$2**: Fecha fin (YYYY-MM-DD)

## PROCESO

### PASO 0: Resolver rutas

Ejecutar la resolución de rutas estándar según `.claude/skills/shared/paso0-rutas.md`.

**Variables adicionales de este skill:**
- `{dia_siguiente}` = `date -v+1d +%Y-%m-%d` (límite superior para PASO 2C, incluye archivos de hoy)
- Verificar/crear `{carpeta_mes}` y `{carpeta_evidencias}` con `mkdir -p`

### PASO 1: Cargar configuración de la entidad
Del config.json ya leído, obtener:
- `rutas.carpeta_anual` (ya resuelta)
- `rutas.carpeta_evidencias` (ya resuelta) — esta es la carpeta de ANEXOS, mapeo de anexos estándar
- `obligaciones_count`: Número de obligaciones

### PASO 2: Buscar archivos del período

**OBLIGATORIO: Ejecutar los 3 `find` siguientes vía Bash tool.** Cada find DEBE ejecutarse como un comando Bash independiente. NO sustituir con lectura de directorios, conocimiento previo ni archivos ya conocidos de pasos anteriores.

**REGLA CRÍTICA DE FECHAS:** NUNCA modificar, ampliar ni ajustar los parámetros de fecha de los `find`. Usar `$1` y `$2` exactos. Si un find devuelve 0 archivos, reportar 0 y continuar — NO inventar rangos alternativos.

**Ver detalle de los 3 comandos find (2A, 2B, 2C), warm-up OneDrive y consolidación en** `references/paso2-find-commands.md`

### PASO 3: Clasificar archivos por tipo

Agrupa los archivos encontrados:

| Categoría | Extensiones | Herramienta |
|-----------|-------------|-------------|
| Documentos Office | `.docx`, `.xlsx`, `.pptx` | MCP read_document |
| PDF | `.pdf` | MCP read_document |
| Texto plano | `.md`, `.txt`, `.json`, `.sql` | Read nativo |
| Imágenes | `.png`, `.jpg`, `.jpeg` | MCP read_image |
| Video | `.mp4`, `.webm`, `.avi` | Solo listar, no leer |
| Otros | `.zip`, `.rar`, etc. | Solo listar, no leer |

### PASO 4: Leer contenido de cada archivo

Leer cada archivo usando la herramienta apropiada según su tipo (PASO 3). Si `read_document` falla, aplicar cadena de fallback.

**Ver detalle de herramientas MCP, argumentos y cadena de fallback en** `references/paso4-lectura-archivos.md`

### PASO 5: Generar resumen de evidencias

Para cada archivo leído, extraer:
1. **Nombre del archivo**
2. **Fecha de modificación**
3. **Tipo de documento**
4. **Resumen del contenido** (máximo 255 palabras)
5. **Obligaciones relacionadas** (según mapeo de la entidad) — **OBLIGATORIO para cada archivo**

### PASO 5.5: Generar manifest JSON para organización de archivos

**OBLIGATORIO** — Después de clasificar archivos y asignar obligaciones, escribir un archivo JSON manifest para el script de organización.

**Ver estructura del JSON, reglas de acción (copy/move) en** `references/paso5-manifest-json.md`

### PASO 6: Ejecutar script de organización de archivos

**OBLIGATORIO** — Ejecutar el script Python que crea carpetas OBLIGACION_N/ y copia/mueve archivos:

```bash
python3 scripts/organize_evidencias.py "{carpeta_evidencias}/_manifest_evidencias_{entidad_lower}_{mes}.json"
```

El script crea carpetas `OBLIGACION_N/` automáticamente, copia archivos externos y mueve archivos locales.

**Después de ejecutar:**
1. Si el script termina OK → eliminar el manifest JSON:
   ```bash
   rm "{carpeta_evidencias}/_manifest_evidencias_{entidad_lower}_{mes}.json"
   ```
2. Reportar: "PASO 6: Copiados N archivos a M carpetas OBLIGACION_N/"
3. Si el script falla → reportar error pero continuar (el .md ya se generó en PASO 5)

### PASO 7: Guardar inventario de evidencias

Guardar el inventario completo en:
```
{carpeta_evidencias}/evidencias_{entidad_lower}_{mes}.md
```

Ejemplo: `.../ANEXOS/evidencias_idt_enero.md`

**También mostrar el resultado en la conversación** para que el usuario pueda revisarlo.

## REGLAS CRÍTICAS

1. **Solo archivos del `find`**: Únicamente los archivos devueltos por el `find` del PASO 2 A, B y C son evidencias válidas
2. **NUNCA modificar fechas**: Usar `$1` y `$2` exactos. No ampliar, ajustar ni inventar rangos alternativos
3. **Calentar caché OneDrive**: Ejecutar PASO 2 PRE antes de los find. Si el primer find devuelve 0, reintentar UNA vez
4. **Lee TODOS los archivos** identificados por el find, sin excepción
5. **Ejecuta las lecturas en paralelo** cuando sea posible
6. Si un archivo falla al leer, **reporta el error pero continúa** con los demás
7. **No inventes contenido** — solo reporta lo que existe en los archivos
8. **Log de comandos**: Para cada find, registrar el comando exacto ejecutado (con fechas sustituidas) junto al resultado
9. **Ortografía:** Aplicar TODAS las reglas de ortografía español de CLAUDE.md

## MAPEO DE ARCHIVOS A OBLIGACIONES

**Ver tabla de palabras clave y mapeo en** `references/mapeo-archivos.md`

## Ejemplos

### Ejemplo 1: Búsqueda con resultados
User says: `/buscar-evidencias IDT 2026-02-01 2026-02-28`
Actions:
1. Ejecuta 3 find: carpeta_anual (15 archivos), carpeta_evidencias (3), carpeta_fuentes (8)
2. Lee cada archivo con MCP read_document/Read
3. Clasifica: 5 documentos Office, 3 PDF, 2 imágenes, 1 video (solo listar)
4. Crea OBLIGACION_1/ a OBLIGACION_6/ con archivos copiados
Result: `evidencias_idt_febrero.md` con inventario de 26 archivos únicos

### Ejemplo 2: Sin archivos en el período
User says: `/buscar-evidencias UAECD 2026-12-01 2026-12-31`
Actions:
1. Ejecuta 3 find: 0 + 0 + 0 archivos
2. TOTAL == 0 → se detiene y pregunta al usuario
Result: No genera archivo, solicita confirmación antes de continuar

## SALIDA ESPERADA

**Ver formato y estructura de carpetas en** `examples/salida_esperada.md`

## ARCHIVO GENERADO

| Campo | Valor |
|-------|-------|
| Nombre | `evidencias_{entidad_lower}_{mes}.md` |
| Ubicación | `{carpeta_evidencias}/` |
| Ejemplo | `.../01. ENERO/ANEXOS/evidencias_idt_enero.md` |
