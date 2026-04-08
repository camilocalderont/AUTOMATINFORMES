---
name: generar-plan-accion
description: "Generates the Plan de Accion progress report for SDMUJER based on evidence from the reporting period. Maps document activity to the security policy implementation indicator, writes a qualitative narrative, and produces a Word deliverable via md-to-docx. Use when user says 'generar plan de accion', 'plan de accion', 'reporte plan de accion', 'seguimiento plan de accion', or needs the Anexo 1A for SDMUJER."
argument-hint: "[ENTIDAD] [FECHA_INICIO] [FECHA_FIN]"
metadata:
  author: solercia
  version: "1.0.0"
  category: documentation
  tags: [plan-acción, sdmujer, seguridad-digital]
  model: sonnet
---

> **REGLAS OBLIGATORIAS** (R1-R7) — ver `agents/skills/shared/paso0-rutas.md#reglas-compactas`. Aplican sin excepción a este skill.


# Skill: Generar Plan de Accion

Genera el reporte de seguimiento del Plan de Accion institucional basado en las evidencias del periodo.
Actualmente aplica a SDMUJER (indicador de Politica de Seguridad Digital). El skill puede ejecutarse standalone o como sub-skill de `/generar-informe`.

## ENTRADA
- **$0**: Entidad (actualmente solo SDMUJER)
- **$1**: Fecha inicio (YYYY-MM-DD)
- **$2**: Fecha fin (YYYY-MM-DD)

## PROCESO

### PASO 0: Resolver rutas

Ejecutar la resolucion de rutas estandar segun `.claude/skills/shared/paso0-rutas.md`.

**Variables adicionales de este skill:**
- `{carpeta_planes}`: Resolver `rutas.carpeta_planes` del config.json reemplazando `{carpeta_anual}` y `{month_name}`. Si no existe en config → `{carpeta_anual}/PLANES/{month_name}`
- `{mes_upper}`: Nombre del mes en MAYUSCULAS (ENERO, FEBRERO, etc.)
- Verificar/crear: `mkdir -p "{carpeta_planes}"`

---

### PASO 1: Verificar insumos previos

Determinar modo de ejecucion:

**A) Modo sub-skill** (dentro de generar-informe):
```bash
ls "{carpeta_evidencias}/evidencias_{entidad_lower}_{mes}.md" 2>/dev/null
```
- **Si existe** → El AI ya tiene el contexto de buscar-evidencias. Leer el archivo como referencia de inventario.
- Este es el modo preferido: ya se leyeron todos los archivos en pasos anteriores.

**B) Modo standalone** (ejecucion directa):
- **Si NO existe** → Ejecutar PASO 2 (busqueda y lectura propia).

---

### PASO 2: Buscar y leer archivos (solo modo standalone)

**SALTAR este paso si PASO 1A fue exitoso.**

Buscar archivos del periodo en `{carpeta_anual}`:

```bash
find "{carpeta_anual}" -type f \
  -newermt "{$1}" ! -newermt "{dia_siguiente_fin}" \
  ! -name ".DS_Store" \
  ! -path "*/node_modules/*" \
  ! -path "*/.git/*" \
  ! -path "*/INFORMES/*" \
  2>/dev/null | sort
```

Donde `{dia_siguiente_fin}` = dia siguiente a `{$2}` (para incluir archivos del ultimo dia).

Para cada archivo encontrado:
- **`.md`, `.txt`, `.json`** → Leer con herramienta Read
- **`.pdf`, `.docx`, `.xlsx`, `.pptx`** → Intentar con MCP `read_document`; si falla → Read nativo o `openpyxl` para Excel
- **Imagenes (`.png`, `.jpg`)** → Listar, no leer
- **Videos (`.mp4`)** → Listar, no leer

---

### PASO 3: Generar INSUMOS_CONSOLIDADOS (opcional)

**Solo en modo standalone.** Si se ejecuta como sub-skill de generar-informe, SALTAR.

Generar archivo `INSUMOS_CONSOLIDADOS_{mes_upper}_{year}.txt` en `{carpeta_planes}/`:

**Ver estructura en** `references/formato_reporte.md#insumos-consolidados`

---

### PASO 4: Redactar reporte cualitativo

Consultar el indicador y objetivo estrategico en `references/formato_reporte.md`.

Con toda la evidencia disponible (del contexto o de PASO 2), redactar:

#### a) Descripcion cualitativa del avance en el mes

**Estructura:** Agrupar actividades por tematica. Cada tematica es un parrafo con:
- Titulo de la tematica (en negrita como inicio del parrafo)
- Descripcion de actividades con referencias a archivos especificos (nombre, fecha)
- Controles ISO 27001:2022 relevantes (si aplica)

**Reglas de redaccion:**
- Tercera persona + pasado impersonal: "Se actualizo", "Se realizo", "Se gestion" (NOTA: el Plan de Accion usa tercera persona, NO primera persona como el informe de obligaciones)
- Cada afirmacion respaldada por archivo leido
- Incluir nombre de archivo y fecha entre parentesis
- Referenciar controles ISO cuando sea pertinente
- Sin calificativos subjetivos
- Ortografia: Aplicar TODAS las reglas de CLAUDE.md

#### b) Retrasos y factores limitantes

- Solo si hay evidencia de retrasos o actividades pendientes
- Si no hay retrasos → dejar en blanco

#### c) Soluciones propuestas

- Solo si hay retrasos identificados
- Propuestas concretas con acciones y fechas si es posible
- Si no hay retrasos → dejar en blanco

---

### PASO 5: Guardar .md

Guardar el reporte en:
```
{carpeta_planes}/{mes_upper}_{year}.md
```

Ejemplo: `.../PLANES/02. FEBRERO/FEBRERO_2026.md`

**Tambien mostrar el resultado en la conversacion.**

---

### PASO 6: Generar .docx

Convertir el .md a .docx usando `/md-to-docx`:

```
/md-to-docx {carpeta_planes}/{mes_upper}_{year}.md
```

Resultado: `{carpeta_planes}/{mes_upper}_{year}.docx`

---

### PASO 7: Copiar a evidencias

1. Copiar .docx a `{carpeta_fuentes}` con nombre estandar para PASO 10 de generar-informe:
```bash
cp "{carpeta_planes}/{mes_upper}_{year}.docx" "{carpeta_fuentes}/plan_accion_{entidad_lower}_{mes}.docx"
```

2. Si hay carpetas OBLIGACION_N/ ya creadas, copiar directamente:
```bash
for N in $(echo "{obligaciones}" | tr ',' ' '); do
  mkdir -p "{carpeta_evidencias}/OBLIGACION_${N}/"
  cp "{carpeta_fuentes}/plan_accion_{entidad_lower}_{mes}.docx" \
     "{carpeta_evidencias}/OBLIGACION_${N}/{nombre_anexo}{extension}"
done
```

Donde `{obligaciones}`, `{nombre_anexo}` y `{extension}` vienen de `config.json["anexos"]["plan_accion"]`.

---

## DIRECTRICES DE REDACCION

1. **Tercera persona + pasado impersonal**: "Se realizo la actualizacion", "Se gestiono el incidente" (diferente del informe de obligaciones que usa primera persona)
2. **Basado en evidencia**: Cada actividad mencionada DEBE corresponder a un archivo leido
3. **Sin calificativos**: No usar "significativo avance", "labor destacada"
4. **Referencias a archivos**: Incluir nombre del archivo y fecha entre parentesis
5. **Controles ISO**: Referenciar controles ISO 27001:2022 / ISO 27002:2022 cuando aplique
6. **Ortografia:** Aplicar TODAS las reglas de "REGLAS DE ORTOGRAFIA ESPAÑOL" de CLAUDE.md

---

## Ejemplos

**Ver ejemplos completos en** `examples/salida_esperada.md`

- **Sub-skill:** Lee evidencias existentes → redacta → .md + .docx en PLANES/ → copia a FUENTE/
- **Standalone:** find archivos → INSUMOS_CONSOLIDADOS → redacta → .md + .docx → copia

## ARCHIVOS GENERADOS

| Archivo | Ubicación |
|---------|-----------|
| `{mes_upper}_{year}.md` / `.docx` | `{carpeta_planes}/` |
| `plan_accion_{entidad_lower}_{mes}.docx` | `{carpeta_fuentes}/` (copia) |
| `INSUMOS_CONSOLIDADOS_{mes_upper}_{year}.txt` | `{carpeta_planes}/` (solo standalone) |
