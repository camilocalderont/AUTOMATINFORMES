# AUTOMATINFORMES - Sistema de Generación Automatizada de Informes

## CONTEXTO

**Autor:** (configurar en entidades/*/config.json)
**Perfil:** Ingeniero de sistemas con especialización en seguridad de la información, desarrollador full stack con conocimientos de arquitectura de software.

## OBJETIVO

Automatizar la generación de informes de actividades para justificar pagos mensuales de contratos de prestación de servicios en 4 entidades públicas del Distrito de Bogotá.

---

## ENTIDADES Y CONTRATOS

| Entidad | Rol | Sistema Principal | Mesa de Servicios | Gestión Proyectos |
|---------|-----|-------------------|-------------------|-------------------|
| IDARTES | Desarrollador Full Stack | Pandora | GLPI | Jira |
| SDMUJER | OSI + Desarrollador | Pandora | GLPI | N/A |
| IDT | Desarrollador Full Stack | Pandora | Correo (Gmail) | N/A |
| UAECD | Arquitecto/Desarrollador | Pandora | Correo (Outlook) | N/A |

---

## RAMAS GIT POR ENTIDAD

| Entidad | Rama Principal | Patrón de Ramas Feature |
|---------|----------------|------------------------|
| IDARTES | `master_proxy` | `CP-*`, `GLPI-*` |
| SDMUJER | `masterSDMujer_proxy` | `*SDMujer*`, `GLPI-*` |
| IDT | `masterIDT_proxy` | `IDT*`, `idt_*` |
| UAECD | `masterCatastro_proxy` | `uaecd*`, `catastro*` |

---

## ESTRUCTURA DEL PROYECTO

```
AUTOMATINFORMES/
├── AGENTS.md                    # Instrucciones canónicas (<200 líneas)
├── CLAUDE.md → AGENTS.md        # Symlink para Claude Code
├── agents/                      # Fuente de verdad
│   ├── skills/                  # 12 skills + shared/
│   ├── rules/                   # 6 rules (ortografía, estilo, fechas, log, OneDrive, pasos)
│   └── subagents/               # (vacío por ahora)
├── .claude/                     # Symlinks a agents/
│   ├── skills/{name} → ../../agents/skills/{name}
│   └── rules/{name}.md → ../../agents/rules/{name}.md
├── entidades/                   # Configuración por entidad
│   ├── {ENTIDAD}/README.md      # Obligaciones contractuales
│   └── {ENTIDAD}/config.json    # Rutas, correos, ramas, anexos
├── scripts/                     # Python: extracción y generación de entregables
│   ├── glpi_extract.py          # GLPI REST API
│   ├── jira_extract.py          # Jira Cloud API
│   ├── commits_to_docx.py       # JSON → Word
│   ├── glpi_to_excel.py         # JSON → Excel
│   ├── jira_to_excel.py         # JSON → Excel
│   ├── correos_to_docx.py       # JSON → Word
│   ├── reuniones_to_docx.py     # JSON → Word
│   └── organize_evidencias.py   # Manifest → OBLIGACION_N/ folders
├── .env.example                 # Template de variables de entorno
├── .mcp.json                    # MCP servers (Jira, Gmail, Outlook, Calendar)
└── contexto/                    # Prompts originales (referencia)
```

---

## TIPOS DE EVIDENCIAS

| Tipo | Skill | API | Entidades |
|------|-------|-----|-----------|
| Commits Git | `/generar-commits` | git log | Todas |
| Soportes GLPI | `/generar-soportes-glpi` | `/extraer-tickets-glpi` | IDARTES, SDMUJER |
| Soportes Correo | `/generar-soportes-correo` | `/extraer-correos-gmail`, `/extraer-correos-outlook` | IDT, UAECD |
| Historias Jira | — | `/extraer-issues-jira` | IDARTES |
| Reuniones | `/resumen-reuniones` | `/extraer-reuniones-calendario` | Todas |
| Plan de Acción | `/generar-plan-accion` | — | SDMUJER |
| Casos de Prueba | Manual (Excel/Word) | — | IDARTES, SDMUJER, UAECD |

---

## DIRECTRICES DE REDACCIÓN

> **Detalle completo en rules:** `agents/rules/redaccion-español.md` y `agents/rules/estilo-informes.md`

- **Primera persona + pasado**: "Realicé la implementación", "Atendí N solicitudes"
- **Tildes obligatorias** en todo texto generado (ver rule `redaccion-español`)
- **Sin calificativos**: No "gran esfuerzo", "significativo avance"
- **No inventar**: Solo actividades con evidencia documentada
- **Citar evidencia**: Al final de cada justificación de obligación

---

## FLUJO DE GENERACIÓN

```
/generar-informe [ENTIDAD] [FECHA_INICIO] [FECHA_FIN]
   │
   ├── PASO 0:  Resolver rutas + inicializar log
   ├── PASO 0B: Verificar/crear estructura de carpetas
   ├── PASO 1:  Cargar config + README
   ├── PASO 2:  Extraer insumos vía API (subagentes paralelos)
   │   ├── 2A: GLPI/Gmail/Outlook    2B: Jira (bg)
   │   ├── 2C: Gmail suplem. (bg)    2D: Calendario
   │   └── 2E: Resumen reuniones
   ├── PASO 3:  /buscar-evidencias
   ├── PASO 4:  /generar-commits
   ├── PASO 5:  /generar-soportes-{glpi|correo}
   ├── PASO 6:  /generar-plan-accion (solo SDMUJER)
   ├── PASO 7:  Consolidar inventario
   ├── PASO 8:  Mapear a obligaciones
   ├── PASO 9:  Redactar justificación
   ├── PASO 10: Organizar anexos en OBLIGACION_N/
   └── PASO 11: Guardar informe en {carpeta_mes}/
```

**Salida:** Informe `.md` + log `.md` en `{carpeta_mes}/`, entregables en `{carpeta_fuentes}/`, carpetas `OBLIGACION_N/` en `{carpeta_evidencias}/`

---

## SKILLS DISPONIBLES

| Skill | Descripción | Entidades |
|-------|-------------|-----------|
| `/generar-informe` | Orquesta sub-skills y genera informe completo | Todas |
| `/buscar-evidencias` | Busca archivos del período, clasifica, organiza en OBLIGACION_N/ | Todas |
| `/generar-commits` | Extrae y formatea commits del período | Todas |
| `/generar-soportes-glpi` | Procesa tickets GLPI (API-first, fallback a archivo) | IDARTES, SDMUJER |
| `/generar-soportes-correo` | Procesa correos (API-first, fallback a PDF) | IDT, UAECD |
| `/resumen-reuniones` | Procesa transcripciones y genera resumen | Todas |
| `/extraer-issues-jira` | Extrae issues de Jira Cloud vía API | IDARTES |
| `/extraer-correos-gmail` | Extrae correos enviados vía Gmail API | IDT, IDARTES |
| `/extraer-correos-outlook` | Extrae correos enviados vía Outlook M365 | SDMUJER, UAECD |
| `/extraer-tickets-glpi` | Extrae tickets GLPI vía REST API | IDARTES, SDMUJER |
| `/generar-plan-accion` | Genera reporte Plan de Acción | SDMUJER |
| `/extraer-reuniones-calendario` | Extrae reuniones del calendario vía API | Todas |
| `/verificar-informe` | Valida coherencia obligación ↔ evidencia (modelo opus) | Todas |

Todos los skills aceptan argumentos: `ENTIDAD FECHA_INICIO FECHA_FIN`

---

## USO RÁPIDO

```bash
# Flujo completo automatizado
/generar-informe IDT 2026-01-16 2026-01-31

# Paso a paso manual
/buscar-evidencias IDARTES 2026-02-01 2026-02-28
/generar-commits IDARTES 2026-02-01 2026-02-28
/generar-soportes-glpi IDARTES 2026-02-01 2026-02-28
/generar-informe IDARTES 2026-02-01 2026-02-28

# Extracción directa vía API
/extraer-issues-jira IDARTES 2026-02-01 2026-02-28
/extraer-correos-gmail IDT 2026-02-01 2026-02-28
```

---

## CONFIGURACIÓN MCP

**Obligatorio:** `awslabs.document-loader-mcp-server` — lectura de PDF/DOCX/XLSX/PPTX

**Integraciones API** (configuradas en `.mcp.json`, credenciales en `.env`):

| MCP Server | Entidad | Tipo |
|------------|---------|------|
| `jira-idartes` | IDARTES | Jira Cloud |
| `gmail-idt`, `gmail-idartes` | IDT, IDARTES | Gmail |
| `outlook-sdmujer`, `outlook-uaecd` | SDMUJER, UAECD | Outlook + Calendar |
| `calendar-idt`, `calendar-idartes` | IDT, IDARTES | Google Calendar |

**GLPI** usa `scripts/glpi_extract.py` (REST API, no MCP).

**Principio API-first con Fallback:** Los skills intentan la API primero. Si falla, continúan con archivo local.

---

## NOTAS TÉCNICAS

- **Repositorios Pandora:** pandora_proxy, apiadministrador, apiplaneacion, modadministrador, modplaneacionoap, modcontratacion, modpazysalvo
- **Subagentes:** `generar-informe` usa Agent tool (background) para Jira y Gmail
- **Anexos estructurados:** `config.json["anexos"]` determina qué archivos van a qué OBLIGACION_N/
- **PASO 0 compartido:** `agents/skills/shared/paso0-rutas.md` — resolución de rutas idéntica para los 12 skills
- **`nombre_corto`:** Campo opcional en `config.json["anexos"]` para nombres de archivo cortos (UAECD: ≤30 chars)
- **Entregables:** JSON intermedio → script Python → DOCX/Excel en `{carpeta_fuentes}/` → se elimina JSON

## RULES ACTIVAS

| Rule | Código | Qué enforce |
|------|--------|-------------|
| `redaccion-español` | R1 | Tildes, sin calificativos, citar evidencia, scripts Python con tildes, idioma es-CO |
| `estilo-informes` | R2 | Primera persona + pasado (Memorando SDMUJER 3-2026-000375) |
| `fechas-estrictas` | R3 | NUNCA modificar rangos de fecha en búsquedas |
| `log-debugging` | R4 | Comandos exactos + resultados en cada paso del log |
| `onedrive-find` | R5 | Warm-up obligatorio + no stat + retry-once |
| `cumplimiento-pasos` | R6 | Cada PASO es obligatorio, reportar antes de avanzar |
| `no-inventar-contenido` | R7 | NUNCA fabricar correos/evidencias. PDF ilegible → reportar, no inventar |

**Inyección:** Las 7 reglas están condensadas en `agents/skills/shared/paso0-rutas.md` (sección "Reglas compactas"). Todos los skills las cargan automáticamente al ejecutar PASO 0.
