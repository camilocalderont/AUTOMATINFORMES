---
name: buscar-evidencias
description: "Searches for files created or modified during a reporting period across annual, evidence, and source folders using 3 find commands, reads content via MCP document-loader, classifies by obligation, and organizes into OBLIGACION_N/ folders. Use when user says \"buscar evidencias\", \"search evidence\", \"find period files\", or needs to inventory deliverables before report generation."
argument-hint: "[ENTIDAD] [FECHA_INICIO] [FECHA_FIN]"
---

# Skill: Buscar y Leer Evidencias del Periodo

## ENTRADA
- **$0**: Entidad (IDARTES, SDMUJER, IDT, UAECD)
- **$1**: Fecha inicio (YYYY-MM-DD)
- **$2**: Fecha fin (YYYY-MM-DD)

## PROCESO

### PASO 0: Resolver rutas

Ejecutar la resolucion de rutas estandar segun `.claude/skills/shared/paso0-rutas.md`.

**Variables adicionales de este skill:**
- `{dia_siguiente}` = `date -v+1d +%Y-%m-%d` (limite superior para PASO 2C, incluye archivos de hoy)
- Verificar/crear `{carpeta_mes}` y `{carpeta_evidencias}` con `mkdir -p`


### PASO 1: Cargar configuracion de la entidad
Del config.json ya leido, obtener:
- `rutas.carpeta_anual` (ya resuelta)
- `rutas.carpeta_evidencias` (ya resuelta) Esta es la carpeta de ANEXOS, mapeo de anexos estandar
- `obligaciones_count`: Numero de obligaciones

### PASO 2: Buscar archivos del periodo

**OBLIGATORIO: Ejecutar los 3 `find` siguientes via Bash tool.** Cada find DEBE ejecutarse como un comando Bash independiente. NO sustituir con lectura de directorios, conocimiento previo ni archivos ya conocidos de pasos anteriores.

**REGLA CRITICA DE FECHAS:** NUNCA modificar, ampliar ni ajustar los parametros de fecha de los `find`. Usar `$1` y `$2` exactos tal como los proporciona el usuario. Si un find devuelve 0 archivos, reportar 0 y continuar — NO inventar rangos alternativos. Los timestamps de OneDrive pueden no coincidir con las fechas reales de creacion; eso es un hecho documentado que el usuario conoce, y prefiere precision de fechas sobre completitud.

#### PASO 2 PRE: Calentar cache OneDrive

OneDrive Files On-Demand no enumera archivos hasta que se accede al directorio. Ejecutar ANTES de los find:

```bash
for dir in "{carpeta_anual}"/*/; do ls "$dir" >/dev/null 2>&1; done
```

Esto fuerza la enumeracion de archivos en cada subcarpeta de primer nivel.

#### PASO 2A: Carpeta ANUAL — archivos del periodo en toda la carpeta anual

```bash
find "{carpeta_anual}" \
  -type f \
  -newermt "$1" ! -newermt "$2" \
  ! -name ".DS_Store" \
  ! -name "*.tmp" \
  ! -name "~*" \
  ! -path "*/node_modules/*" \
  ! -path "*/.git/*" \
  ! -path "*/INFORMES/*" \
  2>/dev/null | sort
```

**Si devuelve 0:** Reintentar UNA vez (a veces OneDrive necesita un segundo acceso). Si sigue en 0, reportar 0 y continuar.

**Despues del find, reportar:** "PASO 2A: {N} archivos en carpeta_anual"
**Comando ejecutado:** Pegar el comando find exacto con las fechas sustituidas (para el log).

#### PASO 2B: Carpeta EVIDENCIAS — anexos dejados manualmente en el periodo

```bash
find "{carpeta_evidencias}" \
  -type f \
  -newermt "$1" ! -newermt "$2" \
  ! -name ".DS_Store" \
  ! -name "*.tmp" \
  ! -name "~*" \
  ! -path "*/node_modules/*" \
  ! -path "*/.git/*" \
  2>/dev/null | sort
```
**Despues del find, reportar:** "PASO 2B: {N} archivos en carpeta_evidencias"
**Comando ejecutado:** Pegar el comando find exacto con las fechas sustituidas.

#### PASO 2C: Carpeta FUENTES — insumos generados (transcripciones, correos, GLPI, Jira)

La carpeta `{carpeta_fuentes}` contiene fuentes base para el informe. Estos archivos se generan **despues** del periodo reportado, por lo que el rango va desde `$1` hasta `{dia_siguiente}` (incluye archivos creados hoy):

```bash
find "{carpeta_fuentes}" \
  -type f \
  -newermt "$1" ! -newermt "{dia_siguiente}" \
  ! -name ".DS_Store" \
  ! -name "*.tmp" \
  ! -name "~*" \
  2>/dev/null | sort
```
**Despues del find, reportar:** "PASO 2C: {N} archivos en carpeta_fuentes"
**Comando ejecutado:** Pegar el comando find exacto con las fechas sustituidas.

**Nota:** Si la carpeta FUENTES no existe, reportar "PASO 2C: 0 archivos (carpeta no existe)" y continuar sin error.

#### Consolidacion PASO 2

Mostrar resumen obligatorio:
```
PASO 2A: X archivos en carpeta_anual
PASO 2B: X archivos en carpeta_evidencias
PASO 2C: X archivos en carpeta_fuentes
TOTAL:   X archivos unicos
```

**Si TOTAL == 0, DETENERSE y preguntar al usuario** antes de continuar.

### PASO 3: Clasificar archivos por tipo

Agrupa los archivos encontrados:

| Categoria | Extensiones | Herramienta |
|-----------|-------------|-------------|
| Documentos Office | `.docx`, `.xlsx`, `.pptx` | MCP read_document |
| PDF | `.pdf` | MCP read_document |
| Texto plano | `.md`, `.txt`, `.json`, `.sql` | Read nativo |
| Imagenes | `.png`, `.jpg`, `.jpeg` | MCP read_image |
| Video | `.mp4`, `.webm`, `.avi` | Solo listar, no leer |
| Otros | `.zip`, `.rar`, etc. | Solo listar, no leer |

### PASO 4: Leer contenido de cada archivo

#### Para documentos Office y PDF:
Usa el MCP `awslabs.document-loader-mcp-server`:

```
Herramienta: read_document
Servidor: user-awslabs.document-loader-mcp-server
Argumentos:
  - file_path: [ruta completa del archivo]
  - file_type: [docx|xlsx|pdf|pptx]
```

**Fallback si `read_document` falla:** Si el MCP no responde o devuelve error para un archivo:
1. Registrar el archivo en una lista de **"archivos no leidos por MCP"**
2. Intentar leer con la herramienta `Read` nativa de Claude Code (funciona para .docx y .xlsx como texto parcial)
3. Si `Read` tampoco puede extraer contenido util, convertir los archivos a markdown con pandoc o similares y leer el archivo en texto.
4. Si hay problemas convirtiendo a markdown, entonces registrar el archivo como **"no leido"** y continuar con el siguiente
5. Al final del PASO 4, **alertar en la salida** listando todos los archivos que no se pudieron leer:
```
**Alerta:** Los siguientes archivos no pudieron ser leidos por read_document:
- [nombre_archivo.xlsx] — [motivo del error]
- [nombre_archivo.pdf] — [motivo del error]
Se recomienda verificar que el MCP document-loader este activo.
```

#### Para archivos de texto:
Usa la herramienta `Read` nativa de Claude Code.

#### Para imagenes:
Usa el MCP con `read_image`:

```
Herramienta: read_image
Servidor: user-awslabs.document-loader-mcp-server
Argumentos:
  - file_path: [ruta completa del archivo]
```

### PASO 5: Generar resumen de evidencias

Para cada archivo leido, extraer:
1. **Nombre del archivo**
2. **Fecha de modificacion**
3. **Tipo de documento**
4. **Resumen del contenido** (maximo 255 palabras)
5. **Obligaciones relacionadas** (segun mapeo de la entidad) — **OBLIGATORIO para cada archivo**

### PASO 5.5: Generar manifest JSON para organizacion de archivos

**OBLIGATORIO** — Despues de clasificar archivos y asignar obligaciones, escribir un archivo JSON:

```
{carpeta_evidencias}/_manifest_evidencias_{entidad_lower}_{mes}.json
```

**Estructura del JSON:**
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

**Reglas para determinar `accion`:**
- Archivos **dentro** de `{carpeta_evidencias}/` → `"move"` (se reubican a OBLIGACION_N/)
- Archivos **fuera** de `{carpeta_evidencias}/` (carpeta_anual, carpeta_fuentes) → `"copy"` (se copian, original intacto)
- Solo incluir archivos que tengan al menos una obligacion asignada
- Archivos sin obligaciones asignadas → NO incluir en el manifest

### PASO 6: Ejecutar script de organizacion de archivos

**OBLIGATORIO** — Ejecutar el script Python que crea carpetas OBLIGACION_N/ y copia/mueve archivos:

```bash
python3 scripts/organize_evidencias.py "{carpeta_evidencias}/_manifest_evidencias_{entidad_lower}_{mes}.json"
```

El script:
- Crea carpetas `OBLIGACION_N/` automaticamente
- Copia archivos externos, mueve archivos locales de carpeta_evidencias
- Imprime resumen JSON a stdout con resultados

**Despues de ejecutar:**
1. Si el script termina OK → eliminar el manifest JSON:
   ```bash
   rm "{carpeta_evidencias}/_manifest_evidencias_{entidad_lower}_{mes}.json"
   ```
2. Reportar: "PASO 6: Copiados N archivos a M carpetas OBLIGACION_N/"
3. Si el script falla → reportar error pero continuar (el .md ya se genero en PASO 5)

### PASO 7: Guardar inventario de evidencias

Guardar el inventario completo en:
```
{carpeta_evidencias}/evidencias_{entidad_lower}_{mes}.md
```

Ejemplo: `.../ANEXOS/evidencias_idt_enero.md`

**Tambien mostrar el resultado en la conversacion** para que el usuario pueda revisarlo.

## REGLAS CRITICAS

1. **Solo archivos del `find`**: Unicamente los archivos devueltos por el `find` del PASO 2 A, B y C son evidencias validas. NO listar archivos pre-existentes en `{carpeta_evidencias}`.
2. **NUNCA modificar fechas**: Usar `$1` y `$2` exactos. No ampliar, ajustar ni inventar rangos alternativos. Si devuelve 0, reportar 0.
3. **Calentar cache OneDrive**: Ejecutar PASO 2 PRE antes de los find. Si el primer find devuelve 0, reintentar UNA vez.
4. **Lee TODOS los archivos identificados por el find**, sin excepcion
5. **Ejecuta las lecturas en paralelo** cuando sea posible
6. Si un archivo falla al leer, **reporta el error pero continua** con los demas
7. **No inventes contenido** - solo reporta lo que existe en los archivos
8. **Log de comandos**: Para cada find, registrar el comando exacto ejecutado (con fechas sustituidas) junto al resultado.
9. **Ortografia:** Aplicar TODAS las reglas de "REGLAS DE ORTOGRAFIA ESPAÑOL" de CLAUDE.md


## Ejemplos

### Ejemplo 1: Busqueda con resultados
User says: `/buscar-evidencias IDT 2026-02-01 2026-02-28`
Actions:
1. Ejecuta 3 find: carpeta_anual (15 archivos), carpeta_evidencias (3), carpeta_fuentes (8)
2. Lee cada archivo con MCP read_document/Read
3. Clasifica: 5 documentos Office, 3 PDF, 2 imagenes, 1 video (solo listar)
4. Crea OBLIGACION_1/ a OBLIGACION_6/ con archivos copiados
Result: `evidencias_idt_febrero.md` con inventario de 26 archivos unicos

### Ejemplo 2: Sin archivos en el periodo
User says: `/buscar-evidencias UAECD 2026-12-01 2026-12-31`
Actions:
1. Ejecuta 3 find: 0 + 0 + 0 archivos
2. TOTAL == 0 → se detiene y pregunta al usuario
Result: No genera archivo, solicita confirmacion antes de continuar

## MAPEO DE ARCHIVOS A OBLIGACIONES

Usa las palabras clave del nombre y contenido para mapear:

| Palabra clave | Posible obligacion |
|---------------|-------------------|
| historia, HU, requisito | Desarrollo, Documentacion |
| prueba, test, caso | Calidad, Pruebas |
| soporte, ticket, GLPI | Soporte tecnico |
| arquitectura, diseno | Arquitectura, Documentacion |
| manual, guia, capacitacion | Transferencia conocimiento |
| seguridad, vulnerabilidad | Seguridad |
| reunion, acta, transcripcion | Reuniones |

## SALIDA ESPERADA

**Ver formato y estructura de carpetas en** `examples/salida_esperada.md`

## ARCHIVO GENERADO

| Campo | Valor |
|-------|-------|
| Nombre | `evidencias_{entidad_lower}_{mes}.md` |
| Ubicacion | `{carpeta_evidencias}/` |
| Ejemplo | `.../01. ENERO/ANEXOS/evidencias_idt_enero.md` |
