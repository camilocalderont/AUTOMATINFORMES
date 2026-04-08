---
name: verificar-informe
description: "Validates coherence between obligation text and evidence files in OBLIGACION_N/ folders. Reads each file, verifies it belongs to the reporting period, detects duplicates (PDF>Word>MD), and confirms every mentioned annex exists. Use when user says 'verificar informe', 'validate report', 'check evidence', 'revisar anexos'."
argument-hint: "[ENTIDAD] [FECHA_INICIO] [FECHA_FIN]"
metadata:
  author: solercia
  version: "1.0.0"
  category: validation
  tags: [verificación, coherencia, evidencias, obligaciones]
  model: opus
---

> **REGLAS OBLIGATORIAS** (R1-R7) — ver `agents/skills/shared/paso0-rutas.md#reglas-compactas`. Aplican sin excepción a este skill.


# Skill: Verificar Informe

Valida la coherencia entre el texto del informe de obligaciones y los archivos en las carpetas OBLIGACION_N/. Este skill se ejecuta como PASO FINAL del orquestador `/generar-informe` o de forma standalone.

## ENTRADA
- **$0**: Entidad (IDARTES, SDMUJER, IDT, UAECD)
- **$1**: Fecha inicio (YYYY-MM-DD)
- **$2**: Fecha fin (YYYY-MM-DD)

## PROCESO

### PASO 0: Resolver rutas

Ejecutar la resolución de rutas estándar según `.claude/skills/shared/paso0-rutas.md`.

Archivos requeridos:
- `{carpeta_mes}/Informe_Obligaciones_{$0}_{mes}_{year}.md` — el informe a verificar
- `{carpeta_evidencias}/OBLIGACION_N/` — las carpetas de evidencia

### PASO 1: Cargar informe y extraer referencias

Leer el informe `.md` y para cada obligación extraer:
1. **Texto de la justificación** (lo que se afirma haber hecho)
2. **Anexos mencionados** en `(Evidencia: ...)` — lista de nombres
3. **Número de obligación**

### PASO 2: Inventariar archivos por carpeta OBLIGACION_N/

Para cada carpeta `OBLIGACION_N/`:
```bash
ls -la "{carpeta_evidencias}/OBLIGACION_{N}/" 2>/dev/null
```

Registrar: nombre, extensión, tamaño de cada archivo.

### PASO 3: Verificación cruzada — texto vs archivos

Para cada obligación, ejecutar 4 validaciones:

#### 3A: Anexo mencionado → archivo existe
- Para cada anexo mencionado en `(Evidencia: ...)`, verificar que existe un archivo con ese nombre (o nombre similar) en `OBLIGACION_N/`
- **FAIL** si un anexo mencionado no tiene archivo correspondiente
- **PASS** si todos los anexos mencionados tienen archivo

#### 3B: Archivo existe → está mencionado
- Para cada archivo en `OBLIGACION_N/`, verificar que está referenciado (directa o indirectamente) en el texto de la obligación
- **WARNING** si hay archivos no referenciados en el texto (posible evidencia sin justificación)

#### 3C: Contenido del archivo → corresponde al período
- **Leer cada archivo** (MCP read_document para .docx/.xlsx/.pdf, Read para .md/.txt)
- Buscar indicadores de fecha dentro del contenido: "período", "fecha", "marzo", meses, años
- **WARNING** si el contenido menciona un período diferente al reportado
- **INFO** si no se puede determinar el período del contenido

#### 3D: Duplicados de formato
- Detectar archivos con el mismo nombre base pero diferente extensión (ej: `informe.pdf` + `informe.docx` + `informe.md`)
- **Prelación:** PDF > Word > Markdown
- **WARNING** con recomendación: "Eliminar {archivo_menor} — ya existe {archivo_mayor}"

### PASO 4: Validación de coherencia narrativa

Para cada obligación, verificar que las afirmaciones del texto tienen respaldo:
- Si el texto dice "Participé en N reuniones" → verificar que el Resumen de Reuniones tiene al menos N reuniones del período
- Si el texto dice "Realicé N commits" → verificar que el Informe de commits tiene N commits
- Si el texto dice "Atendí N tickets" → verificar que los Soportes GLPI tienen N tickets
- Si el texto menciona un documento específico (ej: "GT-MA-3 V5") → verificar que existe en la carpeta
- **FAIL** si una afirmación numérica no coincide con la evidencia
- **WARNING** si se menciona un documento que no está en la carpeta

### PASO 5: Revisión de pares con Codex

Enviar el reporte preliminar de verificación al MCP `codex` para una segunda opinión:

```
Prompt para codex: "Revisa este reporte de verificación de coherencia entre un informe de obligaciones contractuales y sus evidencias. Identifica: 1) Inconsistencias que se me hayan escapado, 2) Evidencias que podrían estar mal clasificadas entre obligaciones, 3) Riesgos de que la supervisora rechace alguna obligación por falta de evidencia clara."
```

Incorporar las observaciones de codex en el reporte final.

### PASO 6: Generar reporte de verificación

Guardar el reporte en:
```
{carpeta_mes}/verificacion_{entidad_lower}_{mes}_{year}.md
```

## ESTRUCTURA DEL REPORTE

```markdown
# Verificación de Informe — {ENTIDAD}
## Período: {$1} a {$2}
## Fecha de verificación: {fecha_actual}

---

## Resumen ejecutivo

| Métrica | Valor |
|---------|-------|
| Obligaciones verificadas | N |
| PASS | N |
| FAIL | N |
| WARNING | N |

---

## Detalle por obligación

### Obligación 1 — {PASS/FAIL/WARNING}

**Texto dice:** "[resumen de lo que afirma el texto]"

| Validación | Estado | Detalle |
|-----------|--------|---------|
| Anexos mencionados existen | PASS/FAIL | [detalle] |
| Archivos tienen referencia | PASS/WARNING | [detalle] |
| Contenido corresponde al período | PASS/WARNING | [detalle] |
| Sin duplicados de formato | PASS/WARNING | [detalle] |
| Coherencia narrativa | PASS/FAIL | [detalle] |

**Archivos en OBLIGACION_1/:**
- archivo1.docx — [status: verificado, período OK]
- archivo2.pdf — [status: verificado, período OK]

[... repetir para cada obligación ...]

---

## Acciones requeridas

### FAIL (bloqueantes)
1. [Acción requerida]

### WARNING (recomendadas)
1. [Acción recomendada]

### Observaciones Codex
1. [Observación de la revisión de pares]
```

## REGLAS CRÍTICAS

1. **LEER cada archivo** — NO inferir contenido por el nombre. Abrir y verificar
2. **NO modificar archivos** — Este skill solo REPORTA, no corrige
3. **Prelación de formatos:** PDF > Word (.docx) > Markdown (.md). Si coexisten, recomendar eliminar los de menor prelación
4. **NUNCA inventar contenido** — Si no se puede leer un archivo, reportar como INFO
5. **Período estricto** — Un archivo cuyo contenido es de otro período es WARNING aunque su fecha de modificación sea del período

## Ejemplos

### Ejemplo 1: Verificación exitosa
User says: `/verificar-informe SDMUJER 2026-03-01 2026-03-31`
Actions:
1. Lee informe: 9 obligaciones, 15 anexos mencionados
2. Inventaría: 38 archivos en 9 carpetas
3. Verifica: todos los anexos existen, contenido del período, sin duplicados
Result: 9 PASS, 0 FAIL, 2 WARNING (archivos sin referenciar)

### Ejemplo 2: Inconsistencias detectadas
User says: `/verificar-informe IDT 2026-02-01 2026-02-28`
Actions:
1. Lee informe: menciona "Anexo 4B. Soportes GLPI" pero no existe en OBLIGACION_4/
2. Detecta commits_idt_febrero.md + commits_idt_febrero.docx (duplicado de formato)
3. Lee reuniones_idt_febrero.docx: contenido menciona "enero 2026" (período incorrecto)
Result: 1 FAIL, 2 WARNING, reporte con acciones requeridas

## ARCHIVOS GENERADOS

| Campo | Valor |
|-------|-------|
| Nombre | `verificacion_{entidad_lower}_{mes}_{year}.md` |
| Ubicación | `{carpeta_mes}/` |
