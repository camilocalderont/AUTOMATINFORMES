---
name: resumen-reuniones
description: "Processes meeting transcriptions and calendar data to generate a structured summary with key points, agreements, attendance table, and Word document deliverable. Combines local transcription files with calendar API data for comprehensive coverage. Use when user says \"resumen reuniones\", \"meeting summary\", \"summarize meetings\", \"resumir reuniones\", or needs meeting evidence for any entity."
argument-hint: "[ENTIDAD] [FECHA_INICIO] [FECHA_FIN]"
metadata:
  author: solercia
  version: "1.0.0"
  category: documentation
  tags: [reuniones, transcripciones, resumen, actas]
---

> **REGLAS OBLIGATORIAS** (R1-R7) — ver `agents/skills/shared/paso0-rutas.md#reglas-compactas`. Aplican sin excepción a este skill.


# Skill: Resumen de Reuniones

## ENTRADA
- **$0**: Entidad (IDARTES, SDMUJER, IDT, UAECD)
- **$1**: Fecha inicio (YYYY-MM-DD)
- **$2**: Fecha fin (YYYY-MM-DD)

## PROCESO

### PASO 0: Resolver rutas

Ejecutar la resolucion de rutas estandar segun `.claude/skills/shared/paso0-rutas.md`.

**Variables adicionales de este skill:**
- `{dia_actual}` = `date +%Y-%m-%d`
- `{carpeta_reuniones}`: Si `rutas.carpeta_reuniones` en config → resolver con `{carpeta_fuentes}`; si no → `{carpeta_fuentes}/TRANSCRIPCIONES`
  - Verificar existencia; si no existe → buscar `TRANSCRIPCIONES` desde `{carpeta_mes}` (maxdepth 4); si no → preguntar al usuario

### PASO 0.5: Cargar datos del calendario (si existen)

Verificar si existe el archivo de reuniones del calendario generado por `/extraer-reuniones-calendario`:

```bash
ls "{carpeta_evidencias}/reuniones_calendario_{entidad_lower}_{mes}.md" 2>/dev/null
```

- **Si existe** → Leerlo y almacenar la lista de reuniones del calendario como referencia. Este archivo contiene todas las reuniones del periodo con fecha, hora, titulo, organizador, participantes y tipo.
- **Si no existe** → Continuar sin datos del calendario. El skill funcionara solo con transcripciones locales.

### PASO 1: Buscar archivos de transcripcion

Buscar archivos en `{carpeta_reuniones}` con fecha entre `$1` y `{dia_actual}` (las transcripciones se generan despues del periodo):

```bash
find "{carpeta_reuniones}" -type f \
  -newermt "$1" -not -newermt "{dia_actual}" \
  \( -name "*transcript*.md" -o -name "*transcripcion*.md" -o -name "*reunion*.md" -o -name "*acta*.docx" -o -name "*acta*.md" -o -name "*meeting*.md" \) \
  2>/dev/null | sort
```

Si `{carpeta_reuniones}` no existe o no hay resultados, buscar tambien en `{carpeta_fuentes}`:
```bash
find "{carpeta_fuentes}" -type f \
  -newermt "$1" -not -newermt "{dia_actual}" \
  \( -name "*transcript*.md" -o -name "*transcripcion*.md" -o -name "*reunion*.md" -o -name "*acta*.docx" -o -name "*acta*.md" -o -name "*meeting*.md" \) \
  2>/dev/null | sort
```

Si no se encuentran archivos en ninguna ubicacion, informar al usuario y terminar indicando que no hay transcripciones para el periodo.

### PASO 2: Leer archivos encontrados

Para cada archivo encontrado:
- **Archivos `.md`**: Usar la herramienta Read directamente
- **Archivos `.docx`**: Usar MCP `read_document`:
```json
{
  "file_path": "{ruta_archivo}",
  "file_type": "docx"
}
```

**Fallback si `read_document` falla:** Si el MCP no responde para un `.docx`, intentar leerlo con la herramienta `Read` nativa. Si tampoco funciona, registrar el archivo como "no leido" y alertar en la salida indicando cuales transcripciones no pudieron procesarse.

### PASO 3: Redactar resumen por reunion

Para cada reunion encontrada, extraer y redactar:

**Ver template por reunion en** `examples/salida_esperada.md`

**Reglas de redaccion:**
- Primera persona + pasado: "Participe en", "Presente", "Discutimos"
- Claro y sin calificativos
- Sin calificativos ("productiva", "exitosa")
- Solo incluir informacion que aparezca en la transcripcion

### PASO 4: Generar tabla resumen y asignar obligacion

#### A) Tabla resumen de reuniones

**Ver formato de tabla en** `examples/salida_esperada.md`

#### B) Reuniones sin transcripcion (solo si hay datos del calendario)

Si en PASO 0.5 se cargaron datos del calendario, agregar seccion con reuniones sin transcripcion. **Ver formato en** `examples/salida_esperada.md`

**Nota:** Solo incluir reuniones que no coincidan (por titulo y fecha) con las transcripciones ya procesadas en PASO 3.

#### C) Asignar obligacion relacionada

Consultar `anexos.reuniones` del config.json para determinar el nombre del anexo:
- **IDT** → "Anexo 2A. Resumen de reuniones" (Obligacion 6)
- **IDARTES** → "Anexo 9A. Resumen de Reuniones" (Obligacion 9)
- **SDMUJER** → "Resumen de reuniones" (Obligacion 10)
- **UAECD** → "Resumen de reuniones" (Obligacion 7)

Agregar footer al final del documento — **ver formato en** `examples/salida_esperada.md`

### PASO 5: Guardar output

Guardar el contenido generado en:
```
{carpeta_evidencias}/reuniones_{entidad_lower}_{mes}.md
```

Ejemplo: `.../ANEXOS/reuniones_idt_enero.md`

**Tambien mostrar el resultado en la conversacion** para que el usuario pueda revisarlo.

### PASO 6: Generar DOCX de reuniones

1. Resolver `{carpeta_fuentes}` desde `config.json rutas.carpeta_fuentes`:
   - Reemplazar `{carpeta_evidencias}` en el valor de `rutas.carpeta_fuentes`
   - Si `rutas.carpeta_fuentes` no existe en config → usar `{carpeta_evidencias}/FUENTES/`
   - Ejecutar: `mkdir -p "{carpeta_fuentes}"`

2. Generar JSON intermedio — **estructura en** `references/json_structure.md`
   - Archivo: `{carpeta_fuentes}/_reuniones_data_{entidad_lower}_{mes}.json`

3. Ejecutar el script de generacion:
```bash
python3 scripts/reuniones_to_docx.py "{carpeta_fuentes}/_reuniones_data_{entidad_lower}_{mes}.json" "{carpeta_fuentes}/reuniones_{entidad_lower}_{mes}.docx"
```

4. Si el script termina correctamente:
   - Eliminar el JSON intermedio: `rm "{carpeta_fuentes}/_reuniones_data_{entidad_lower}_{mes}.json"`
   - Informar: "DOCX generado: `{carpeta_fuentes}/reuniones_{entidad_lower}_{mes}.docx`"

5. Si el script falla:
   - Informar el error pero NO detener la ejecucion (el .md ya se genero en PASO 5)

## DIRECTRICES DE REDACCION

1. **Primera persona + pasado**: "Participe en la reunion", "Presente el avance", "Acordamos los compromisos"
2. **Claro y verificable**: Solo informacion de las transcripciones, no inventar
3. **Sin calificativos**: Evitar "reunion productiva", "amplia participacion"
4. **Objetivo**: Documentar reuniones como evidencia de coordinacion y seguimiento
5. **Evidencia**: Referenciar el anexo correspondiente de config.json (`anexos.reuniones`)
6. **No inventar**: Solo incluir informacion presente en las transcripciones
7. **Ortografia:** Aplicar TODAS las reglas de "REGLAS DE ORTOGRAFIA ESPAÑOL" de CLAUDE.md

## Ejemplos

### Ejemplo 1: Con transcripciones y calendario
User says: `/resumen-reuniones IDARTES 2026-02-01 2026-02-28`
Actions:
1. PASO 0.5: Lee reuniones_calendario_idartes_febrero.md (12 reuniones)
2. PASO 1: Encuentra 5 transcripciones en TRANSCRIPCIONES/
3. PASO 3: Redacta resumen detallado de 5 reuniones con transcripcion
4. PASO 4: Tabla con 12 reuniones (5 con transcripcion, 7 solo calendario)
5. Genera .md y .docx
Result: `reuniones_idartes_febrero.md` + `reuniones_idartes_febrero.docx`

### Ejemplo 2: Sin transcripciones disponibles
User says: `/resumen-reuniones UAECD 2026-03-01 2026-03-31`
Actions:
1. PASO 0.5: No existe archivo de calendario
2. PASO 1: No hay transcripciones en ninguna ubicacion
Result: Informa "No hay transcripciones para UAECD en el periodo" y termina

## ARCHIVOS GENERADOS

| Campo | Valor |
|-------|-------|
| Nombre MD | `reuniones_{entidad_lower}_{mes}.md` |
| Ubicacion MD | `{carpeta_evidencias}/` |
| Nombre DOCX | `reuniones_{entidad_lower}_{mes}.docx` |
| Ubicacion DOCX | `{carpeta_fuentes}/` |
| Ejemplo MD | `.../ANEXOS/reuniones_idt_enero.md` |
| Ejemplo DOCX | `.../FUENTES/reuniones_idt_enero.docx` |
