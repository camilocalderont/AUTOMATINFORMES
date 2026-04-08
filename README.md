# AUTOMATINFORMES

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python&logoColor=white)
![Claude Code](https://img.shields.io/badge/Claude%20Code-CLI-6f42c1?logo=anthropic&logoColor=white)
![Skills](https://img.shields.io/badge/Skills-12-green)
![Rules](https://img.shields.io/badge/Rules-6-orange)
![Entidades](https://img.shields.io/badge/Entidades-4-informational)

Sistema para **automatizar la generación de informes mensuales de actividades** que soportan pagos de contratos de prestación de servicios en cuatro entidades públicas del Distrito de Bogotá.

El flujo se orquesta con **skills de Claude Code** y scripts en **Python** para extraer evidencias desde múltiples fuentes (Git, GLPI, Jira, Gmail, Outlook, Calendar), consolidar la información y producir entregables (Markdown, Word y Excel) organizados por obligación contractual.

---

## Tabla de contenidos

- [Entidades soportadas](#entidades-soportadas)
- [Requisitos previos](#requisitos-previos)
- [Instalación](#instalación)
- [Estructura del proyecto](#estructura-del-proyecto)
- [Uso rápido](#uso-rápido)
- [Flujo de generación](#flujo-de-generación)
- [Skills disponibles](#skills-disponibles)
- [Rules activas](#rules-activas)
- [Configuración por entidad](#configuración-por-entidad)
- [Integraciones API](#integraciones-api)
- [Salida y entregables](#salida-y-entregables)

---

## Entidades soportadas

| Entidad | Rol | Mesa de Servicios | Gestión Proyectos |
|---------|-----|-------------------|-------------------|
| **IDARTES** | Desarrollador Full Stack | GLPI | Jira |
| **SDMUJER** | OSI + Desarrollador | GLPI | — |
| **IDT** | Desarrollador Full Stack | Correo (Gmail) | — |
| **UAECD** | Arquitecto/Desarrollador | Correo (Outlook) | — |

Todas las entidades comparten el sistema **Pandora** como plataforma principal de desarrollo.

---

## Requisitos previos

- [Claude Code CLI](https://docs.anthropic.com/en/docs/claude-code) instalado y autenticado
- **Python 3.10+** con pip
- **MCP Server obligatorio:**
  - `awslabs.document-loader-mcp-server` — lectura de PDF, DOCX, XLSX, PPTX
- **MCP Servers opcionales** (según entidad):
  - `mcp-atlassian` — Jira Cloud (IDARTES)
  - `@gongrzhe/server-gmail-autoauth-mcp` — Gmail (IDT, IDARTES)
  - `@softeria/ms-365-mcp-server` — Outlook/M365 (SDMUJER, UAECD)
  - `@cocal/google-calendar-mcp` — Google Calendar (IDT, IDARTES)
- Acceso a las cuentas institucionales configuradas en `config.json`

---

## Instalación

```bash
# 1. Clonar el repositorio
git clone <URL_DEL_REPOSITORIO>
cd AUTOMATINFORMES

# 2. Instalar dependencias Python
pip install -r requirements.txt

# 3. Configurar variables de entorno
cp .env.example .env
# Editar .env con credenciales de GLPI, Jira, Outlook, etc.

# 4. Configurar MCP servers
# Editar .mcp.json con los servers disponibles en tu entorno

# 5. Configurar rutas por entidad
# Editar entidades/{ENTIDAD}/config.json con las rutas locales
```

### Variables de entorno requeridas

```bash
# Jira Cloud (IDARTES)
JIRA_IDARTES_URL=https://idartes-tecnologia.atlassian.net
JIRA_IDARTES_EMAIL=tu-email@idartes.gov.co
JIRA_IDARTES_API_TOKEN=token-aquí

# GLPI REST API (IDARTES, SDMUJER)
GLPI_IDARTES_URL=https://soporteti.idartes.gov.co/apirest.php
GLPI_IDARTES_APP_TOKEN=token-aquí
GLPI_IDARTES_USER_TOKEN=token-aquí

# Outlook / Microsoft 365 (SDMUJER, UAECD)
SDMUJER_TENANT_ID=tenant-id
SDMUJER_CLIENT_ID=client-id
SDMUJER_CLIENT_SECRET=secret
```

> Las credenciales de Gmail y Calendar usan OAuth y se almacenan en `~/.gmail-mcp/` y `~/.google-calendar-mcp/` respectivamente.

---

## Estructura del proyecto

```
AUTOMATINFORMES/
├── AGENTS.md                    # Instrucciones canónicas (<200 líneas)
├── CLAUDE.md → AGENTS.md        # Symlink para Claude Code
│
├── agents/                      # Fuente de verdad
│   ├── skills/                  # 12 skills + shared/
│   │   ├── generar-informe/     # Orquestador principal
│   │   ├── buscar-evidencias/   # Búsqueda de archivos del período
│   │   ├── generar-commits/     # Extracción de commits Git
│   │   ├── generar-soportes-glpi/
│   │   ├── generar-soportes-correo/
│   │   ├── resumen-reuniones/
│   │   ├── extraer-issues-jira/
│   │   ├── extraer-correos-gmail/
│   │   ├── extraer-correos-outlook/
│   │   ├── extraer-tickets-glpi/
│   │   ├── generar-plan-accion/
│   │   ├── extraer-reuniones-calendario/
│   │   └── shared/              # PASO 0 compartido (resolución de rutas)
│   ├── rules/                   # 6 rules enforceable
│   └── subagents/
│
├── .claude/                     # Symlinks a agents/
│   ├── skills/{name} → ../../agents/skills/{name}
│   └── rules/{name}.md → ../../agents/rules/{name}.md
│
├── entidades/                   # Configuración por entidad
│   ├── IDARTES/
│   │   ├── README.md            # Obligaciones contractuales
│   │   └── config.json          # Rutas, correos, ramas, anexos
│   ├── SDMUJER/
│   ├── IDT/
│   └── UAECD/
│
├── scripts/                     # Python: extracción y entregables
│   ├── glpi_extract.py          # GLPI REST API → JSON/Excel
│   ├── jira_extract.py          # Jira Cloud API → JSON/Excel
│   ├── commits_to_docx.py       # JSON → Word (commits)
│   ├── glpi_to_excel.py         # JSON → Excel (tickets)
│   ├── jira_to_excel.py         # JSON → Excel (issues)
│   ├── correos_to_docx.py       # JSON → Word (correos)
│   ├── reuniones_to_docx.py     # JSON → Word (reuniones)
│   └── organize_evidencias.py   # Manifest → OBLIGACION_N/ folders
│
├── .env.example                 # Plantilla de variables de entorno
├── .mcp.json                    # Configuración de MCP servers
└── requirements.txt             # openpyxl, python-docx, fpdf2
```

---

## Uso rápido

```bash
# Flujo completo automatizado (orquesta todos los sub-skills)
/generar-informe IDT 2026-01-16 2026-01-31

# Paso a paso manual
/buscar-evidencias IDARTES 2026-02-01 2026-02-28
/generar-commits IDARTES 2026-02-01 2026-02-28
/generar-soportes-glpi IDARTES 2026-02-01 2026-02-28
/generar-informe IDARTES 2026-02-01 2026-02-28

# Extracción directa vía API
/extraer-issues-jira IDARTES 2026-02-01 2026-02-28
/extraer-correos-gmail IDT 2026-02-01 2026-02-28
/extraer-reuniones-calendario SDMUJER 2026-02-01 2026-02-28
```

---

## Flujo de generación

```
/generar-informe [ENTIDAD] [FECHA_INICIO] [FECHA_FIN]
   │
   ├── PASO 0:  Resolver rutas + inicializar log
   ├── PASO 0B: Verificar/crear estructura de carpetas
   ├── PASO 1:  Cargar config + README de obligaciones
   │
   ├── PASO 2:  Extraer insumos vía API (subagentes paralelos)
   │   ├── 2A: GLPI / Gmail / Outlook
   │   ├── 2B: Jira (background, solo IDARTES)
   │   ├── 2C: Gmail suplementario (background)
   │   ├── 2D: Calendario (Google / Outlook)
   │   └── 2E: Resumen de reuniones → .md + .docx
   │
   ├── PASO 3:  /buscar-evidencias → inventario de archivos del período
   ├── PASO 4:  /generar-commits → reporte semanal + .docx
   ├── PASO 5:  /generar-soportes-{glpi|correo} → reporte + .xlsx/.docx
   ├── PASO 6:  /generar-plan-accion (solo SDMUJER)
   │
   ├── PASO 7:  Consolidar inventario de todas las fuentes
   ├── PASO 8:  Mapear evidencias a obligaciones contractuales
   ├── PASO 9:  Redactar justificación por obligación
   ├── PASO 10: Organizar anexos en carpetas OBLIGACION_N/
   └── PASO 11: Guardar informe final + log
```

**Principio API-first con Fallback:** cada skill intenta la API primero. Si falla o no está configurada, continúa con archivos locales.

---

## Skills disponibles

Todos los skills aceptan argumentos: `ENTIDAD FECHA_INICIO FECHA_FIN`

| Skill | Descripción | Entidades |
|-------|-------------|-----------|
| `/generar-informe` | Orquesta todos los sub-skills y genera el informe completo | Todas |
| `/buscar-evidencias` | Busca archivos del período, clasifica y organiza en OBLIGACION_N/ | Todas |
| `/generar-commits` | Extrae commits Git y genera reporte semanal + Word | Todas |
| `/generar-soportes-glpi` | Procesa tickets GLPI (API-first, fallback a CSV/Excel) | IDARTES, SDMUJER |
| `/generar-soportes-correo` | Procesa correos de soporte (API-first, fallback a PDF) | IDT, UAECD |
| `/resumen-reuniones` | Resume transcripciones + calendario → Word | Todas |
| `/extraer-issues-jira` | Extrae issues finalizados de Jira Cloud → Excel | IDARTES |
| `/extraer-correos-gmail` | Extrae correos enviados de Gmail → Word | IDT, IDARTES |
| `/extraer-correos-outlook` | Extrae correos enviados de Outlook → Word | SDMUJER, UAECD |
| `/extraer-tickets-glpi` | Extrae tickets GLPI vía REST API → Excel | IDARTES, SDMUJER |
| `/generar-plan-accion` | Genera reporte de Plan de Acción TI → Word | SDMUJER |
| `/extraer-reuniones-calendario` | Extrae reuniones del calendario vía API | Todas |

---

## Rules activas

Las rules se cargan automáticamente y aplican restricciones durante la ejecución:

| Rule | Qué enforce |
|------|-------------|
| `redaccion-español` | Tildes obligatorias, sin calificativos subjetivos, citar evidencia, no inventar actividades |
| `estilo-informes` | Redacción en primera persona + pasado ("Realicé", "Atendí", "Desarrollé") |
| `fechas-estrictas` | NUNCA modificar rangos de fecha en búsquedas — si retorna 0, reportar 0 |
| `log-debugging` | Cada paso debe registrar comandos exactos ejecutados + resultados |
| `onedrive-find` | Warm-up obligatorio antes de `find` en OneDrive, no usar `stat`, retry-once |
| `cumplimiento-pasos` | Cada PASO numerado es obligatorio — no saltar bajo presión de contexto |

---

## Configuración por entidad

Cada entidad requiere dos archivos en `entidades/{ENTIDAD}/`:

### `README.md` — Obligaciones contractuales

Define el texto completo de cada obligación del contrato y el mapeo de evidencias:

```markdown
## Obligación 1
Apoyar en el desarrollo y mantenimiento de los sistemas de información...

**Evidencia:** Commits, historias de usuario Jira
```

### `config.json` — Configuración técnica

```json
{
  "autor": { "nombre": "...", "email": "..." },
  "git": {
    "ruta_proyecto": "/ruta/a/pandora_proxy",
    "repositorios": ["pandora_proxy", "modplaneacionoap", "..."],
    "rama_principal": "master_proxy"
  },
  "rutas": {
    "carpeta_anual": "/ruta/a/ENTIDAD/2026",
    "carpeta_mes": "{carpeta_anual}/{month_name}",
    "carpeta_evidencias": "{carpeta_mes}/ANEXOS",
    "carpeta_fuentes": "{carpeta_evidencias}/FUENTE"
  },
  "mesa_servicios": { "tipo": "glpi" },
  "api": {
    "glpi": { "url_env": "GLPI_IDARTES_URL", "..." },
    "jira": { "..." },
    "gmail": { "mcp_server": "gmail-idartes" }
  },
  "anexos": {
    "1A": {
      "nombre": "Commits de desarrollo",
      "extension": ".docx",
      "obligaciones": [1, 3, 6],
      "fuente_key": "commits"
    }
  }
}
```

---

## Integraciones API

| Servicio | MCP Server | Entidades | Script |
|----------|------------|-----------|--------|
| **Jira Cloud** | `jira-idartes` (mcp-atlassian) | IDARTES | `jira_extract.py` |
| **Gmail** | `gmail-idt`, `gmail-idartes` | IDT, IDARTES | — |
| **Outlook/M365** | `outlook-sdmujer`, `outlook-uaecd` | SDMUJER, UAECD | — |
| **GLPI** | — (REST directo) | IDARTES, SDMUJER | `glpi_extract.py` |
| **Google Calendar** | `calendar-idt`, `calendar-idartes` | IDT, IDARTES | — |
| **Outlook Calendar** | Reutiliza `outlook-*` | SDMUJER, UAECD | — |

---

## Salida y entregables

Después de ejecutar `/generar-informe`, se genera:

```
{carpeta_mes}/
├── Informe_Obligaciones_{ENTIDAD}_{mes}_{año}.md   # Informe final
├── log_{entidad}_{mes}_{año}.md                     # Log de ejecución
└── ANEXOS/                                          # {carpeta_evidencias}
    ├── evidencias_{entidad}_{mes}.md                # Inventario de archivos
    ├── commits_{entidad}_{mes}.md                   # Reporte de commits
    ├── soportes_{entidad}_{mes}.md                  # Reporte de soportes
    ├── reuniones_{entidad}_{mes}.md                 # Resumen de reuniones
    ├── OBLIGACION_1/                                # Entregables por obligación
    │   ├── Commits_de_desarrollo.docx
    │   └── Tickets_GLPI.xlsx
    ├── OBLIGACION_2/
    │   └── ...
    └── FUENTE/                                      # {carpeta_fuentes}
        ├── commits_{entidad}_{mes}.docx
        ├── glpi_{entidad}_{mes}.xlsx
        ├── jira_{entidad}_{mes}.xlsx
        ├── correos_soporte_{entidad}_{mes}.docx
        └── reuniones_{entidad}_{mes}.docx
```

---

## Arquitectura de agentes

Este proyecto usa la **estructura canónica de agentes IA**:

- `agents/` es la **fuente de verdad** para skills, rules y subagents
- `.claude/` contiene solo **symlinks** que apuntan a `agents/`
- `AGENTS.md` es el archivo de configuración principal; `CLAUDE.md` es un symlink a él
- Las rules se cargan automáticamente según su scope (`always` o `path-scoped`)

Para auditar o modificar el ecosistema:

```bash
/agent-ecosystem audit     # Reporte de salud
/agent-ecosystem setup     # Crear/normalizar estructura
/agent-ecosystem optimize  # Plan de optimización
```
