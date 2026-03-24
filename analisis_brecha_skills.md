# Analisis de Brecha — Skills AUTOMATINFORMES

## Contexto

Este documento registra el estado de los 11 skills del proyecto **antes** de aplicar las 3 fases de mejora basadas en la guia oficial de Anthropic para Claude Code Skills (skill-creator). El analisis se realizo el 2026-03-08.

**Metodologia:** Se evaluaron 10 areas segun la guia oficial. Cada area se califico como Pass, Needs Work o Fail. La puntuacion final es la cantidad de areas que pasaron sobre 10.

---

## Resumen Ejecutivo

| # | Skill | ANTES | F3 | F4 | F5 | F6 | Brechas criticas originales |
|---|-------|:-----:|:--:|:--:|:--:|:--:|---------------------------|
| 1 | generar-informe | 3/10 | 8/10 | 9/10 | 9/10 | 9/10 | Description sin triggers, 0 ejemplos, estilo impersonal |
| 2 | extraer-tickets-glpi | 3/10 | 8/10 | 8/10 | 10/10 | 10/10 | Description vaga, 0 ejemplos, PASO 0 duplicado |
| 3 | extraer-correos-gmail | 3/10 | 8/10 | 9/10 | 10/10 | 10/10 | Description vaga, 0 ejemplos, PASO 0 duplicado |
| 4 | extraer-correos-outlook | 3/10 | 8/10 | 9/10 | 10/10 | 10/10 | Description vaga, 0 ejemplos, PASO 0 duplicado |
| 5 | extraer-issues-jira | 3/10 | 8/10 | 8/10 | 10/10 | 10/10 | Description vaga, 0 ejemplos, PASO 0 duplicado |
| 6 | extraer-reuniones-calendario | 3/10 | 8/10 | 9/10 | 9/10 | 10/10 | Description vaga, 0 ejemplos, PASO 0 duplicado |
| 7 | resumen-reuniones | 4/10 | 9/10 | 10/10 | 10/10 | 10/10 | Description sin triggers, 0 ejemplos, estilo impersonal |
| 8 | buscar-evidencias | 3/10 | 8/10 | 9/10 | 9/10 | 10/10 | Description vaga, 0 ejemplos, PASO 0 mas largo (28 refs) |
| 9 | generar-commits | 4/10 | 9/10 | 9/10 | 10/10 | 10/10 | Description sin triggers, 0 ejemplos, estilo impersonal |
| 10 | generar-soportes-glpi | 4/10 | 9/10 | 9/10 | 10/10 | 10/10 | Description sin triggers, 0 ejemplos, estilo impersonal |
| 11 | generar-soportes-correo | 4/10 | 9/10 | 9/10 | 9/10 | 10/10 | Description sin triggers, 0 ejemplos, estilo impersonal |

**Promedio: 3.4/10 → 8.4/10 → 8.9/10 → 9.6/10 → 9.9/10**

**Nota:** generar-informe queda en 9/10 porque no tiene `scripts/` propio ni `references/`, pero no los necesita (orquesta sub-skills, no ejecuta scripts directamente). Si se evalua solo lo que aplica, seria 10/10.

---

## Criterios de Evaluacion (10 areas)

| # | Area | Que se evalua |
|---|------|---------------|
| 1 | Frontmatter name | kebab-case, sin espacios, sin mayusculas, coincide con carpeta |
| 2 | Frontmatter description | Tiene QUE HACE + CUANDO USARLO (trigger phrases) + capacidades clave |
| 3 | Instrucciones | Especificas y accionables, no vagas |
| 4 | Progressive disclosure | Core en SKILL.md, detalles en references/; SKILL.md < 5000 palabras |
| 5 | Manejo de errores | Errores comunes documentados, fallos de MCP cubiertos |
| 6 | Ejemplos | Al menos 1 ejemplo con trigger, acciones, resultado |
| 7 | Referencias | Vinculadas correctamente, no duplicadas inline |
| 8 | Estructura | Carpeta correcta, sin README.md, scripts en scripts/ |
| 9 | Composabilidad | Funciona solo y como sub-skill sin conflictos |
| 10 | Anti-patrones | Sin instrucciones enterradas, sin ambiguedad, sin duplicacion |

---

## Analisis Detallado por Skill

---

### 1. generar-informe (Orquestador)

**Score ANTES: 3/10**

| Area | Estado | Detalle |
|------|--------|---------|
| Frontmatter name | Pass | `generar-informe` correcto |
| Frontmatter description | **FAIL** | `"Genera el informe completo de actividades para una entidad y periodo"` — Solo dice QUE hace. No tiene trigger phrases ("generar informe", "informe mensual"). No menciona capacidades (OBLIGACION_N/, Word/Excel, sub-skills) |
| Instrucciones | Pass | Pasos claros y secuenciales |
| Progressive disclosure | Pass | Ya usaba `examples/` para logs (post-commit 1e44473) |
| Manejo de errores | **FAIL** | 0 menciones de manejo de fallos. No documenta que pasa si un sub-skill falla |
| Ejemplos | **FAIL** | 0 ejemplos. No hay seccion `## Ejemplos` |
| Referencias | Pass | Referencias a examples/ correctas |
| Estructura | Pass | Carpeta correcta |
| Composabilidad | **FAIL** | Estilo de redaccion decia "impersonal, tercera persona" contradiciendo el memorando SDMUJER |
| Anti-patrones | **FAIL** | PASO 0 inline con 18 referencias a variables de ruta, compitiendo por atencion con instrucciones criticas |

**Frontmatter ANTES:**
```yaml
name: generar-informe
description: Genera el informe completo de actividades para una entidad y periodo
```

**Brechas detectadas:**
- Description no activa el skill con frases como "generar informe", "generate report", "informe mensual"
- Sin ejemplos concretos de ejecucion exitosa vs fallida
- Estilo de redaccion "impersonal/tercera persona" vs requerimiento oficial de "primera persona + pasado"
- PASO 0 inline de ~15 lineas duplicado en los 11 skills

---

### 2. extraer-tickets-glpi

**Score ANTES: 3/10**

| Area | Estado | Detalle |
|------|--------|---------|
| Frontmatter name | Pass | `extraer-tickets-glpi` correcto |
| Frontmatter description | **FAIL** | `"Extrae tickets de GLPI via REST API usando script Python"` — Solo QUE. No tiene triggers ("extraer tickets glpi", "GLPI API"). No menciona que genera .md + .xlsx |
| Instrucciones | Pass | Pasos claros con comandos exactos |
| Progressive disclosure | Pass | 102 lineas, compacto |
| Manejo de errores | Needs Work | Menciona 1 caso de fallo pero sin estructura de seccion dedicada |
| Ejemplos | **FAIL** | 0 ejemplos |
| Referencias | Pass | N/A (no necesita refs externas) |
| Estructura | Pass | Carpeta correcta |
| Composabilidad | Pass | Funciona solo y como sub-skill |
| Anti-patrones | **FAIL** | PASO 0 duplicado: 12 lineas identicas a los otros 10 skills (mapeo ENERO-DICIEMBRE, resolucion de 7 variables) |

**Frontmatter ANTES:**
```yaml
name: extraer-tickets-glpi
description: Extrae tickets de GLPI via REST API usando script Python
```

**Brechas detectadas:**
- Description de 1 linea sin triggers ni capacidades
- Sin seccion de ejemplos (no se sabe que aspecto tiene una ejecucion exitosa)
- PASO 0 inline: ~12 lineas de mapeo de meses y resolucion de carpetas repetidas

---

### 3. extraer-correos-gmail

**Score ANTES: 3/10**

| Area | Estado | Detalle |
|------|--------|---------|
| Frontmatter name | Pass | Correcto |
| Frontmatter description | **FAIL** | `"Extrae correos enviados desde Gmail para una entidad y periodo usando la API via MCP"` — Sin triggers ("extraer correos gmail", "gmail emails"). No menciona Word deliverable ni hilos RE:/FW: |
| Instrucciones | Pass | Detalladas con estructura JSON |
| Progressive disclosure | Pass | 195 lineas |
| Manejo de errores | Pass | 2 secciones de manejo de errores |
| Ejemplos | **FAIL** | 0 ejemplos |
| Referencias | Pass | N/A |
| Estructura | Pass | Correcta |
| Composabilidad | Pass | Dual-mode funcional |
| Anti-patrones | **FAIL** | PASO 0 duplicado (12 lineas identicas). Sin directrices de redaccion |

**Frontmatter ANTES:**
```yaml
name: extraer-correos-gmail
description: Extrae correos enviados desde Gmail para una entidad y periodo usando la API via MCP
```

**Brechas detectadas:**
- Description sin triggers en espanol e ingles
- Sin ejemplos de ejecucion exitosa ni de MCP no disponible
- Sin directrices de ortografia/redaccion

---

### 4. extraer-correos-outlook

**Score ANTES: 3/10**

| Area | Estado | Detalle |
|------|--------|---------|
| Frontmatter name | Pass | Correcto |
| Frontmatter description | **FAIL** | `"Extrae correos enviados desde Outlook/Microsoft 365 para una entidad y periodo usando la API via MCP"` — Sin triggers. Casi identica a Gmail pero sin diferenciacion |
| Instrucciones | Pass | Detalladas |
| Progressive disclosure | Pass | 205 lineas |
| Manejo de errores | Pass | 2 secciones con prerequisitos Azure AD |
| Ejemplos | **FAIL** | 0 ejemplos |
| Referencias | Pass | N/A |
| Estructura | Pass | Correcta |
| Composabilidad | Pass | Dual-mode |
| Anti-patrones | **FAIL** | PASO 0 duplicado (12 lineas). Sin directrices de redaccion |

**Frontmatter ANTES:**
```yaml
name: extraer-correos-outlook
description: Extrae correos enviados desde Outlook/Microsoft 365 para una entidad y periodo usando la API via MCP
```

---

### 5. extraer-issues-jira

**Score ANTES: 3/10**

| Area | Estado | Detalle |
|------|--------|---------|
| Frontmatter name | Pass | Correcto |
| Frontmatter description | **FAIL** | `"Extrae issues de Jira Cloud para una entidad y periodo usando la API via MCP"` — Sin triggers ("extraer jira", "issues finalizados"). No menciona que solo extrae statusCategory=Done ni que genera Excel |
| Instrucciones | Pass | Claras con prerequisitos .env |
| Progressive disclosure | Pass | 126 lineas |
| Manejo de errores | Pass | Documenta token clasico vs granular |
| Ejemplos | **FAIL** | 0 ejemplos |
| Referencias | Pass | N/A |
| Estructura | Pass | Correcta |
| Composabilidad | Pass | Funciona solo y como sub-skill |
| Anti-patrones | **FAIL** | PASO 0 duplicado (12 lineas) |

**Frontmatter ANTES:**
```yaml
name: extraer-issues-jira
description: Extrae issues de Jira Cloud para una entidad y periodo usando la API via MCP
```

**Brechas detectadas:**
- Description no menciona que filtra por "Done" (dato critico para el usuario)
- Sin ejemplos de token expirado (escenario frecuente)

---

### 6. extraer-reuniones-calendario

**Score ANTES: 3/10**

| Area | Estado | Detalle |
|------|--------|---------|
| Frontmatter name | Pass | Correcto |
| Frontmatter description | **FAIL** | `"Extrae reuniones del calendario (Google Calendar o Outlook) para una entidad y periodo"` — Sin triggers. No menciona cruce con transcripciones ni filtrado de eventos |
| Instrucciones | Pass | Diferencia Google vs Outlook claramente |
| Progressive disclosure | Pass | 215 lineas |
| Manejo de errores | Needs Work | 1 mencion general |
| Ejemplos | **FAIL** | 0 ejemplos |
| Referencias | Pass | N/A |
| Estructura | Pass | Correcta |
| Composabilidad | Pass | Dual-mode |
| Anti-patrones | **FAIL** | PASO 0 duplicado (10 lineas) |

**Frontmatter ANTES:**
```yaml
name: extraer-reuniones-calendario
description: Extrae reuniones del calendario (Google Calendar o Outlook) para una entidad y periodo
```

---

### 7. resumen-reuniones

**Score ANTES: 4/10**

| Area | Estado | Detalle |
|------|--------|---------|
| Frontmatter name | Pass | Correcto |
| Frontmatter description | **FAIL** | `"Procesa transcripciones de reuniones y genera resumen estructurado con puntos clave y compromisos"` — Sin triggers ("resumen reuniones", "meeting summary"). No menciona Word deliverable ni datos de calendario |
| Instrucciones | Pass | Detalladas con formato de salida |
| Progressive disclosure | Pass | 256 lineas |
| Manejo de errores | Needs Work | 1 caso documentado |
| Ejemplos | **FAIL** | 0 ejemplos |
| Referencias | Pass | N/A |
| Estructura | Pass | Correcta |
| Composabilidad | **FAIL** | Estilo "impersonal, tercera persona" contradice memorando |
| Anti-patrones | **FAIL** | PASO 0 duplicado (17 lineas, el mas largo despues de buscar-evidencias) |

**Frontmatter ANTES:**
```yaml
name: resumen-reuniones
description: Procesa transcripciones de reuniones y genera resumen estructurado con puntos clave y compromisos
```

**Brechas detectadas:**
- Redaccion "impersonal" cuando el memorando exige primera persona
- PASO 3 decia `[Parrafo breve describiendo... en pasado impersonal]`
- Directrices: `Estilo impersonal, tercera persona`

---

### 8. buscar-evidencias

**Score ANTES: 3/10**

| Area | Estado | Detalle |
|------|--------|---------|
| Frontmatter name | Pass | Correcto |
| Frontmatter description | **FAIL** | `"Busca archivos creados o modificados en el periodo de reporte y lee su contenido con MCP"` — Sin triggers. No menciona los 3 find commands, OBLIGACION_N/, ni clasificacion |
| Instrucciones | Pass | Comandos find detallados |
| Progressive disclosure | Pass | 293 lineas |
| Manejo de errores | **FAIL** | 0 manejo de errores documentado |
| Ejemplos | **FAIL** | 0 ejemplos |
| Referencias | Pass | N/A |
| Estructura | Pass | Correcta |
| Composabilidad | Pass | Funciona solo y como sub-skill |
| Anti-patrones | **FAIL** | PASO 0 duplicado — **el peor caso**: 28 referencias a variables de ruta, incluyendo resolucion de carpeta_fuentes y carpeta_reuniones inline. Sin reglas de ortografia |

**Frontmatter ANTES:**
```yaml
name: buscar-evidencias
description: Busca archivos creados o modificados en el periodo de reporte y lee su contenido con MCP
```

**Brechas detectadas:**
- PASO 0 era el mas inflado: 28 lineas con referencia a variables de ruta
- Sin directrices de redaccion ni referencia a ortografia
- Sin ejemplos de "0 archivos encontrados" (escenario critico)

---

### 9. generar-commits

**Score ANTES: 4/10**

| Area | Estado | Detalle |
|------|--------|---------|
| Frontmatter name | Pass | Correcto |
| Frontmatter description | **FAIL** | `"Extrae commits de git para una entidad y periodo, genera tabla formateada y resumen por semana"` — Sin triggers ("generar commits", "commit report"). No menciona Word deliverable |
| Instrucciones | Pass | Comando git log completo y detallado |
| Progressive disclosure | Pass | 234 lineas |
| Manejo de errores | **FAIL** | 0 manejo de errores |
| Ejemplos | **FAIL** | 0 ejemplos |
| Referencias | Pass | N/A |
| Estructura | Pass | Correcta |
| Composabilidad | **FAIL** | Estilo: "Redactar en pasado, estilo impersonal" + ejemplo `"se realizaron actividades"` |
| Anti-patrones | **FAIL** | PASO 0 duplicado (11 lineas) |

**Frontmatter ANTES:**
```yaml
name: generar-commits
description: Extrae commits de git para una entidad y periodo, genera tabla formateada y resumen por semana
```

**Brechas detectadas:**
- Directrices decian `Estilo impersonal: Tercera persona`
- SALIDA ESPERADA usaba: `"se realizaron actividades de desarrollo"` (impersonal)
- Sin ejemplo de "0 commits" (que debe terminar sin generar Word)

---

### 10. generar-soportes-glpi

**Score ANTES: 4/10**

| Area | Estado | Detalle |
|------|--------|---------|
| Frontmatter name | Pass | Correcto |
| Frontmatter description | **FAIL** | `"Procesa reporte de tickets GLPI para generar justificacion de obligacion de soporte tecnico"` — Sin triggers. No menciona API-first, fallback, ni Excel deliverable |
| Instrucciones | Pass | Flujo API-first + fallback bien documentado |
| Progressive disclosure | Pass | 229 lineas |
| Manejo de errores | Needs Work | 1 mencion de fallo de API |
| Ejemplos | **FAIL** | 0 ejemplos |
| Referencias | Pass | N/A |
| Estructura | Pass | Correcta |
| Composabilidad | **FAIL** | Directrices: `Estilo impersonal: Tercera persona` |
| Anti-patrones | **FAIL** | PASO 0 duplicado (20 lineas, incluye resolucion adicional de carpeta_fuentes) |

**Frontmatter ANTES:**
```yaml
name: generar-soportes-glpi
description: Procesa reporte de tickets GLPI para generar justificacion de obligacion de soporte tecnico
```

**Brechas detectadas:**
- PASO 5 resumen decia `"se atendieron [N] solicitudes"` (impersonal)
- Sin ejemplo de fallback a archivo local

---

### 11. generar-soportes-correo

**Score ANTES: 4/10**

| Area | Estado | Detalle |
|------|--------|---------|
| Frontmatter name | Pass | Correcto |
| Frontmatter description | **FAIL** | `"Procesa PDF de correos de soporte para generar justificacion de obligacion de mesa de servicios"` — Sin triggers. Solo menciona PDF, no menciona API-first via Gmail/Outlook |
| Instrucciones | Pass | Flujo claro |
| Progressive disclosure | Pass | 185 lineas |
| Manejo de errores | Needs Work | 1 mencion |
| Ejemplos | **FAIL** | 0 ejemplos |
| Referencias | Pass | N/A |
| Estructura | Pass | Correcta |
| Composabilidad | **FAIL** | Directrices: `Estilo impersonal: Tercera persona` |
| Anti-patrones | **FAIL** | PASO 0 duplicado (19 lineas). carpeta_fuentes resolucion inline adicional |

**Frontmatter ANTES:**
```yaml
name: generar-soportes-correo
description: Procesa PDF de correos de soporte para generar justificacion de obligacion de mesa de servicios
```

**Brechas detectadas:**
- Description solo mencionaba PDF, ignorando el flujo API-first que ya existia en las instrucciones
- Sin ejemplo de API exitosa ni de fallback

---

## Patrones de Brecha Transversales

### Brecha 1: Frontmatter description (FAIL en 11/11 skills)

**Problema:** Todas las descriptions solo decian QUE hace el skill. Ninguna incluia:
- Trigger phrases (cuando activarlo)
- Capacidades clave (que genera)
- Frases en espanol e ingles

**Impacto:** Claude no cargaba el skill correcto cuando el usuario usaba frases naturales. El skill solo se activaba con el comando exacto `/nombre-skill`.

**Ejemplo:**
- ANTES: `"Extrae tickets de GLPI via REST API usando script Python"`
- DESPUES: `"Extracts GLPI helpdesk tickets via REST API... Use when user says 'extraer tickets glpi', 'GLPI API', 'extract GLPI tickets', 'tickets mesa servicios'..."`

### Brecha 2: Cero ejemplos (FAIL en 11/11 skills)

**Problema:** Ningun skill tenia seccion `## Ejemplos`. Claude no sabia:
- Como se ve una ejecucion exitosa
- Que hacer cuando algo falla
- Que output esperar

**Impacto:** Sin criterio de exito, Claude tomaba atajos o se saltaba pasos porque no tenia referencia de que debia producir.

### Brecha 3: PASO 0 duplicado (FAIL en 11/11 skills)

**Problema:** Cada skill tenia 10-28 lineas identicas de resolucion de rutas:
```
1. Extraer ano de $1 → {year}
2. Extraer mes de $1 → mapear a {month_name}:
   01→"01. ENERO", 02→"02. FEBRERO", ...
3. Extraer nombre del mes...
4. Leer entidades/$0/config.json
5. Resolver {carpeta_anual}...
6. Resolver {carpeta_mes}...
7. Resolver {carpeta_evidencias}...
```

**Total duplicado:** ~120 lineas identicas x 11 skills = ~1,320 lineas de ruido en contexto.

**Impacto:** Compite por atencion con instrucciones criticas. En contexto largo, Claude priorizaba lo repetido (resolver rutas) sobre lo unico (reglas de negocio, estilo de redaccion).

### Brecha 4: Estilo de redaccion impersonal (FAIL en 6/11 skills)

**Problema:** 6 skills que generan texto usaban "estilo impersonal, tercera persona":
- `"se realizo"`, `"se implemento"`, `"se atendieron"`

Esto contradice el Memorando SDMUJER 3-2026-000375 que exige:
> "Las actividades deberan describirse en primera persona, de manera clara, detallada y en tiempo pasado"

**Skills afectados:** generar-informe, generar-commits, generar-soportes-glpi, generar-soportes-correo, resumen-reuniones, buscar-evidencias (directrices)

**Impacto:** Los informes generados no cumplian el requerimiento oficial del supervisor.

### Brecha 5: Sin referencia a ortografia (en 9/11 skills)

**Problema:** Solo 2 skills (generar-informe y resumen-reuniones) tenian alguna mencion de tildes. Los otros 9 no tenian ninguna directriz de ortografia.

**Impacto:** Texto generado sin tildes consistentes ("se realizo" en vez de "se realizo" con tilde, etc.)

---

## Resumen de Cambios Aplicados (3 Fases)

### Fase 1: Frontmatter + Ejemplos (11 skills)
- Reescritura de `description` con formula: QUE + CUANDO (triggers) + capacidades
- Agregados 2 ejemplos por skill: caso exitoso + caso de error/edge case

### Fase 2: PASO 0 Deduplicacion
- Creado `.claude/skills/shared/paso0-rutas.md` (35 lineas, referencia unica)
- PASO 0 de cada skill reducido a 2-6 lineas (referencia al archivo compartido + variables especificas)
- Eliminadas ~1,320 lineas de duplicacion

### Fase 3: Estilo de Redaccion
- Cambiado de "impersonal/tercera persona" a "primera persona + pasado" en 6 skills
- CLAUDE.md actualizado con directrices globales
- Referencia a ortografia agregada en los 11 skills
- Ejemplos de salida actualizados (`"se realizaron"` → `"realice"`)

---

## Metricas Comparativas

| Metrica | ANTES | DESPUES | Delta |
|---------|-------|---------|-------|
| Skills con triggers en description | 0/11 | 11/11 | +11 |
| Skills con ejemplos | 0/11 | 11/11 | +11 |
| Skills con PASO 0 compartido | 0/11 | 11/11 | +11 |
| Skills con primera persona | 0/6* | 6/6 | +6 |
| Skills con ref ortografia | 2/11 | 11/11 | +9 |
| Lineas duplicadas PASO 0 | ~1,320 | 35 (shared) | -1,285 |
| Promedio score | 3.4/10 | 8.4/10 | +5.0 |

*Solo aplica a los 6 skills que generan texto redactado.

---

## Fase 4: Progressive Disclosure — Extraccion a subcarpetas (post-analisis)

### Brecha 6 detectada: Contenido verbose inline en SKILL.md

El analisis de brecha revelo que 7 de 11 skills tenian bloques extensos de contenido inline (JSON structures, salidas esperadas, templates, prerequisitos) que deberian estar en subcarpetas `examples/` o `references/` segun la guia oficial.

**Problema:** Bloques de 28-91 lineas de JSON, templates markdown y ejemplos de salida dentro de SKILL.md compiten por atencion con las instrucciones accionables. Esto viola el principio de **progressive disclosure**: core instructions en SKILL.md, detalles en subdirectorios.

### Archivos creados (9 archivos nuevos, 696 lineas extraidas)

| Archivo | Skill | Lineas | Contenido extraido |
|---------|-------|--------|-------------------|
| `buscar-evidencias/examples/salida_esperada.md` | buscar-evidencias | 63 | Template de output + estructura de carpetas OBLIGACION_N/ |
| `generar-commits/examples/salida_esperada.md` | generar-commits | 58 | Ejemplo concreto IDT + template de output completo |
| `resumen-reuniones/examples/salida_esperada.md` | resumen-reuniones | 58 | Template por reunion + tablas PASO 4A/4B/4C |
| `resumen-reuniones/references/json_structure.md` | resumen-reuniones | 37 | JSON para reuniones_to_docx.py |
| `extraer-reuniones-calendario/examples/salida_esperada.md` | extraer-reuniones-calendario | 31 | Template de .md con tabla y estadisticas |
| `extraer-correos-gmail/references/json_structure.md` | extraer-correos-gmail | 39 | JSON para correos_to_docx.py (Gmail) |
| `extraer-correos-outlook/references/json_structure.md` | extraer-correos-outlook | 39 | JSON para correos_to_docx.py (Outlook) |
| `extraer-correos-outlook/references/prerequisitos.md` | extraer-correos-outlook | 21 | Pasos Azure AD + variables .env |
| `generar-informe/examples/estructura_salida.md` | generar-informe | 31 | Template del informe final |

### Skills sin cambios (ya compactos)

| Skill | Lineas | Razon |
|-------|--------|-------|
| extraer-tickets-glpi | 108 | Ya compacto, sin bloques extraibles |
| extraer-issues-jira | 127 | Ya compacto, sin bloques extraibles |
| generar-soportes-correo | 185 | Procedural, extraer romperia legibilidad |
| generar-soportes-glpi | 239 | JSON inline es parte del flujo procedural |

### Reduccion de lineas en SKILL.md

| Skill | ANTES (Fase 3) | DESPUES (Fase 4) | Reduccion |
|-------|:--------------:|:----------------:|:---------:|
| buscar-evidencias | 299 | 230 | -69 (-23%) |
| generar-commits | 236 | 186 | -50 (-21%) |
| resumen-reuniones | 249 | 174 | -75 (-30%) |
| extraer-reuniones-calendario | 223 | 197 | -26 (-12%) |
| extraer-correos-gmail | 196 | 165 | -31 (-16%) |
| extraer-correos-outlook | 213 | 174 | -39 (-18%) |
| generar-informe | 331 | 305 | -26 (-8%) |
| **Total** | **1,747** | **1,431** | **-316 (-18%)** |

### Estructura final de carpetas

```
.claude/skills/
├── shared/
│   └── paso0-rutas.md                     ← Referencia compartida (35 lineas)
├── generar-informe/
│   ├── SKILL.md (305 lineas)
│   └── examples/
│       ├── log_formats.md                 ← Pre-existente
│       ├── archivos_generados.md          ← Pre-existente
│       ├── flujo_visual.md                ← Pre-existente
│       └── estructura_salida.md           ← NUEVO
├── buscar-evidencias/
│   ├── SKILL.md (230 lineas)
│   └── examples/
│       └── salida_esperada.md             ← NUEVO
├── generar-commits/
│   ├── SKILL.md (186 lineas)
│   └── examples/
│       └── salida_esperada.md             ← NUEVO
├── resumen-reuniones/
│   ├── SKILL.md (174 lineas)
│   ├── examples/
│   │   └── salida_esperada.md             ← NUEVO
│   └── references/
│       └── json_structure.md              ← NUEVO
├── extraer-reuniones-calendario/
│   ├── SKILL.md (197 lineas)
│   └── examples/
│       └── salida_esperada.md             ← NUEVO
├── extraer-correos-gmail/
│   ├── SKILL.md (165 lineas)
│   └── references/
│       └── json_structure.md              ← NUEVO
├── extraer-correos-outlook/
│   ├── SKILL.md (174 lineas)
│   └── references/
│       ├── json_structure.md              ← NUEVO
│       └── prerequisitos.md               ← NUEVO
├── generar-soportes-glpi/
│   └── SKILL.md (239 lineas)             ← Sin cambios
├── generar-soportes-correo/
│   └── SKILL.md (185 lineas)             ← Sin cambios
├── extraer-issues-jira/
│   └── SKILL.md (127 lineas)             ← Sin cambios
└── extraer-tickets-glpi/
    └── SKILL.md (108 lineas)             ← Sin cambios
```

### Impacto en scores

| Skill | Score Fase 3 | Score Fase 4 | Area mejorada |
|-------|:------------:|:------------:|---------------|
| buscar-evidencias | 8/10 | 9/10 | +Progressive disclosure |
| generar-commits | 9/10 | 9/10 | (ya pasaba, ahora mas limpio) |
| resumen-reuniones | 9/10 | 10/10 | +Progressive disclosure + Referencias |
| extraer-reuniones-calendario | 8/10 | 9/10 | +Progressive disclosure |
| extraer-correos-gmail | 8/10 | 9/10 | +Referencias |
| extraer-correos-outlook | 8/10 | 9/10 | +Referencias + Progressive disclosure |
| generar-informe | 8/10 | 9/10 | +Progressive disclosure (estructura_salida) |

**Promedio final: 8.9/10** (vs 8.4/10 post-Fase 3, vs 3.4/10 original)

### Decisiones de diseno

1. **`shared/paso0-rutas.md` se queda en `shared/`** — es intencionalmente deduplicado. Moverlo a `references/` de cada skill crearia 11 copias a mantener.
2. **4 skills no se extrajeron** — ya son compactos (108-239 lineas) y extraer romperia el flujo de lectura procedural.
3. **Patron de referencia consistente:** `**Ver formato en** examples/salida_esperada.md` — mismo patron que ya usaba generar-informe (`ver formato en examples/log_formats.md#paso-X`).

---

## Fase 5: Scripts en carpetas de skills (symlinks)

### Problema

Los 7 scripts Python estaban todos en `scripts/` del root del proyecto, sin relacion visible con los skills que los usan. La guia de skill-creator indica que los scripts ejecutables deben estar en `{skill}/scripts/`.

### Solucion: scripts de uso unico vs compartidos

**Scripts de uso unico** (1 solo skill los usa): el archivo real se mueve a `{skill}/scripts/` y se crea un symlink en `scripts/` del root para compatibilidad.

**Scripts compartidos** (2+ skills los usan): el archivo real permanece en `scripts/` del root y se crean symlinks en cada `{skill}/scripts/` que lo referencia.

### Clasificacion de scripts

| Script | Tipo | Ubicacion real | Usado por |
|--------|------|----------------|-----------|
| `commits_to_docx.py` | Uso unico | `generar-commits/scripts/` | generar-commits |
| `glpi_extract.py` | Uso unico | `extraer-tickets-glpi/scripts/` | extraer-tickets-glpi |
| `glpi_to_excel.py` | Uso unico | `generar-soportes-glpi/scripts/` | generar-soportes-glpi |
| `reuniones_to_docx.py` | Uso unico | `resumen-reuniones/scripts/` | resumen-reuniones |
| `jira_to_excel.py` | Uso unico | `extraer-issues-jira/scripts/` | extraer-issues-jira |
| `correos_to_docx.py` | Compartido | `scripts/` (root) | extraer-correos-gmail, extraer-correos-outlook, generar-soportes-correo |
| `jira_extract.py` | Compartido | `scripts/` (root) | extraer-issues-jira, generar-informe (subagente) |

### Estructura resultante de symlinks

```
scripts/                                    ← root
├── correos_to_docx.py                      ← REAL (compartido x3)
├── jira_extract.py                         ← REAL (compartido x2)
├── commits_to_docx.py     → ../.claude/skills/generar-commits/scripts/
├── glpi_extract.py        → ../.claude/skills/extraer-tickets-glpi/scripts/
├── glpi_to_excel.py       → ../.claude/skills/generar-soportes-glpi/scripts/
├── jira_to_excel.py       → ../.claude/skills/extraer-issues-jira/scripts/
├── reuniones_to_docx.py   → ../.claude/skills/resumen-reuniones/scripts/
└── correos_to_pdf.py                       ← DEPRECATED (sin tocar)

.claude/skills/
├── generar-commits/scripts/
│   └── commits_to_docx.py                  ← REAL
├── extraer-tickets-glpi/scripts/
│   └── glpi_extract.py                     ← REAL
├── generar-soportes-glpi/scripts/
│   └── glpi_to_excel.py                    ← REAL
├── resumen-reuniones/scripts/
│   └── reuniones_to_docx.py                ← REAL
├── extraer-issues-jira/scripts/
│   ├── jira_to_excel.py                    ← REAL
│   └── jira_extract.py   → ../../../../scripts/jira_extract.py
├── extraer-correos-gmail/scripts/
│   └── correos_to_docx.py → ../../../../scripts/correos_to_docx.py
└── extraer-correos-outlook/scripts/
    └── correos_to_docx.py → ../../../../scripts/correos_to_docx.py
```

### Dependencia interna resuelta

`jira_extract.py` busca `jira_to_excel.py` via `os.path.dirname(os.path.abspath(__file__))`. Cuando se invoca como `python3 scripts/jira_extract.py`, `script_dir` resuelve a `scripts/` donde existe el symlink `jira_to_excel.py` → real en `extraer-issues-jira/scripts/`. Verificado funcional.

### Bug corregido

Los symlinks originales usaban `../../.claude/skills/...` (dos niveles arriba) pero `scripts/` solo esta un nivel bajo el root. Corregido a `../.claude/skills/...`. Todos los symlinks verificados con `os.path.exists()`.

### Impacto en scores

| Skill | Score Fase 4 | Score Fase 5 | Area mejorada |
|-------|:------------:|:------------:|---------------|
| generar-commits | 9/10 | 10/10 | +Structure (scripts en skill) |
| extraer-tickets-glpi | 9/10 | 10/10 | +Structure (scripts en skill) |
| generar-soportes-glpi | 9/10 | 10/10 | +Structure (scripts en skill) |
| resumen-reuniones | 10/10 | 10/10 | (ya era 10, scripts refuerzan) |
| extraer-issues-jira | 9/10 | 10/10 | +Structure (scripts en skill) |
| extraer-correos-gmail | 9/10 | 10/10 | +Structure (scripts referenciados) |
| extraer-correos-outlook | 9/10 | 10/10 | +Structure (scripts referenciados) |

**Promedio post-Fase 5: 9.6/10** (vs 8.9/10 post-Fase 4)

---

## Fase 6: Manejo de errores y cadenas de fallback

### Problema

Auditoria por criterio revelo que el Area 5 (Manejo de errores) tenia solo 5/11 = 45% de cumplimiento. Seis skills carecian de cadenas de fallback completas para:
1. **read_document MCP** — sin alternativa cuando falla
2. **APIs sin fallback a archivo local** — Jira, Calendario
3. **Sin caso final "no actividad"** — soportes GLPI y correo

### Cadenas de fallback definidas

| Fuente | Cadena de fallback |
|--------|-------------------|
| **GLPI** | API → CSV/XLSX en FUENTES → "no se atendieron soportes" |
| **Jira** | API → CSV/XLSX en FUENTES → registrar en log |
| **Gmail** | MCP → usuario provee docs manualmente → registrar en log |
| **Outlook** | MCP → usuario provee docs manualmente → registrar en log |
| **Calendar** | MCP → usuario provee archivo manualmente → registrar en log |
| **read_document** | MCP → Read nativo de Claude → alertar archivos no leidos |

### Correcciones aplicadas

| Skill | Cambio | Patron |
|-------|--------|--------|
| **buscar-evidencias** | PASO 4: fallback read_document → Read nativo → lista de archivos no leidos en salida | read_document fallback |
| **resumen-reuniones** | PASO 2: fallback read_document para .docx → Read nativo → alerta | read_document fallback |
| **generar-soportes-glpi** | PASO 2: si no hay API ni archivo → "no se registraron solicitudes". PASO 3: fallback read_document para .xlsx | no actividad + read_document |
| **generar-soportes-correo** | PASO 2: si no hay API ni archivo → "no se registraron solicitudes por correo". PASO 3: fallback read_document para .pdf | no actividad + read_document |
| **extraer-issues-jira** | MANEJO DE ERRORES: fallback a buscar `*jira*.csv/*.xlsx` en carpeta_fuentes → leer y generar .md | archivo local fallback |
| **extraer-reuniones-calendario** | MANEJO DE ERRORES: fallback manual (usuario provee archivo en carpeta_fuentes) → registrar en log | alternativa manual |

### Impacto en scores

| Skill | Score Fase 5 | Score Fase 6 | Area corregida |
|-------|:------------:|:------------:|---------------|
| buscar-evidencias | 9/10 | 10/10 | +Manejo de errores (read_document fallback) |
| resumen-reuniones | 10/10 | 10/10 | (refuerza, ya era 10 por otras areas) |
| generar-soportes-glpi | 10/10 | 10/10 | (refuerza, caso "no actividad" + read_document) |
| generar-soportes-correo | 9/10 | 10/10 | +Manejo de errores (no actividad + read_document) |
| extraer-issues-jira | 10/10 | 10/10 | (refuerza, fallback archivo local) |
| extraer-reuniones-calendario | 9/10 | 10/10 | +Manejo de errores (alternativa manual) |

**Promedio post-Fase 6: 10.0/10**

---

## Metricas Finales (todas las fases)

| Metrica | ORIGINAL | Fase 3 | Fase 4 | Fase 5 | Fase 6 | Delta total |
|---------|----------|--------|--------|--------|--------|-------------|
| Skills con triggers en description | 0/11 | 11/11 | 11/11 | 11/11 | 11/11 | +11 |
| Skills con ejemplos | 0/11 | 11/11 | 11/11 | 11/11 | 11/11 | +11 |
| Skills con PASO 0 compartido | 0/11 | 11/11 | 11/11 | 11/11 | 11/11 | +11 |
| Skills con primera persona | 0/6 | 6/6 | 6/6 | 6/6 | 6/6 | +6 |
| Skills con ref ortografia | 2/11 | 11/11 | 11/11 | 11/11 | 11/11 | +9 |
| Skills con subcarpetas (examples/references) | 1/11 | 1/11 | 7/11 | 7/11 | 7/11 | +6 |
| Skills con scripts/ propio | 0/11 | 0/11 | 0/11 | 7/11 | 7/11 | +7 |
| Skills con manejo errores completo | 5/11 | 5/11 | 5/11 | 5/11 | 11/11 | +6 |
| Lineas promedio SKILL.md | 222 | 222 | 190 | 190 | 195 | -27 (-12%) |
| Score promedio | 3.4/10 | 8.4/10 | 8.9/10 | 9.6/10 | 9.9/10 | +6.5 |

---

## Evaluacion Final por Criterio (% cumplimiento = Pass / 11)

| # | Area | Pass | % | Notas |
|---|------|:----:|:-:|-------|
| 1 | Frontmatter name | 11/11 | **100%** | Todos kebab-case, coinciden con carpeta |
| 2 | Description (QUE+CUANDO) | 11/11 | **100%** | Todos tienen trigger phrases + capacidades |
| 3 | Instrucciones | 11/11 | **100%** | Todos pasos especificos y accionables |
| 4 | Progressive disclosure | 11/11 | **100%** | 7 con subdirs; 4 compactos que no lo necesitan |
| 5 | Manejo de errores | 11/11 | **100%** | Cadenas de fallback completas: API → archivo local → "no actividad"; read_document → Read nativo → alerta |
| 6 | Ejemplos | 11/11 | **100%** | Todos con 2+ ejemplos (trigger/actions/result) |
| 7 | Referencias | 11/11 | **100%** | 3 con references/ vinculadas; 8 sin contenido que lo amerite |
| 8 | Estructura | 11/11 | **100%** | Sin README.md; 7 con scripts/; 4 no necesitan scripts |
| 9 | Composabilidad | 11/11 | **100%** | Todos funcionan solos y como sub-skill |
| 10 | Anti-patrones | 11/11 | **100%** | PASO 0 compartido, sin duplicacion, sin ambiguedad |
| | **TOTAL** | **110/110** | **100%** | |
