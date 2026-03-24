# AUTOMATINFORMES - Sistema de Generacion Automatizada de Informes

## CONTEXTO

**Autor:** (configurar en entidades/*/config.json)
**Perfil:** Ingeniero de sistemas con especializacion en seguridad de la informacion, desarrollador full stack con conocimientos de arquitectura de software.

## OBJETIVO

Automatizar la generacion de informes de actividades para justificar pagos mensuales de contratos de prestacion de servicios en 4 entidades publicas del Distrito de Bogota.

---

## ENTIDADES Y CONTRATOS

| Entidad | Rol | Sistema Principal | Mesa de Servicios | Gestion Proyectos |
|---------|-----|-------------------|-------------------|-------------------|
| IDARTES | Desarrollador Full Stack | Pandora | GLPI | Jira |
| SDMUJER | OSI + Desarrollador | Pandora | GLPI | N/A |
| IDT | Desarrollador Full Stack | Pandora | Correo (Gmail) | N/A |
| UAECD | Arquitecto/Desarrollador | Pandora | Correo (Outlook) | N/A |

---

## RAMAS GIT POR ENTIDAD

Cada entidad trabaja sobre ramas especificas del sistema Pandora:

| Entidad | Rama Principal | Patron de Ramas Feature |
|---------|----------------|------------------------|
| IDARTES | `master_proxy` | `CP-*`, `GLPI-*` |
| SDMUJER | `masterSDMujer_proxy` | `*SDMujer*`, `GLPI-*` |
| IDT | `masterIDT_proxy` | `IDT*`, `idt_*` |
| UAECD | `masterCatastro_proxy` | `uaecd*`, `catastro*` |

---

## ESTRUCTURA DEL PROYECTO

```
AUTOMATINFORMES/
├── CLAUDE.md                    # Este archivo - instrucciones generales
├── entidades/                   # Configuracion por entidad
│   ├── IDARTES/
│   │   ├── README.md           # Objeto, obligaciones, skills aplicables
│   │   └── config.json         # Ramas, correos, rutas de evidencias
│   ├── SDMUJER/
│   ├── IDT/
│   └── UAECD/
├── .env.example                 # Template de variables de entorno
├── .mcp.json                    # Configuracion MCP servers (Jira, Gmail, Outlook)
├── .claude/
│   └── skills/                 # Skills compartidos
│       ├── buscar-evidencias/  # Busca archivos del periodo y lee con MCP
│       ├── generar-commits/
│       ├── generar-soportes-glpi/
│       ├── generar-soportes-correo/
│       ├── resumen-reuniones/
│       ├── generar-informe/
│       ├── extraer-issues-jira/     # API: Jira Cloud (IDARTES)
│       ├── extraer-correos-gmail/   # API: Gmail (IDT, IDARTES)
│       ├── extraer-correos-outlook/ # API: Outlook M365 (SDMUJER, UAECD)
│       ├── extraer-tickets-glpi/    # API: GLPI REST (IDARTES, SDMUJER)
│       └── extraer-reuniones-calendario/ # API: Google Calendar / Outlook Calendar
├── scripts/                    # Scripts Python para extraccion y generacion
│   ├── glpi_extract.py         # Extraccion de tickets GLPI via REST API
│   ├── jira_extract.py         # Extraccion de issues Jira via API
│   ├── commits_to_docx.py      # JSON → Word con informe de commits
│   ├── glpi_to_excel.py        # JSON → Excel con tickets GLPI
│   ├── jira_to_excel.py        # JSON → Excel con issues Jira
│   ├── correos_to_docx.py      # JSON → Word con correos enviados
│   └── reuniones_to_docx.py    # JSON → Word con resumen de reuniones
└── contexto/                   # Prompts originales (referencia)
```

---

## TIPOS DE EVIDENCIAS POR OBLIGACION

### 1. Commits de Git (Desarrollo)
- **Comando base:** `git log --author="EMAIL" --since="YYYY-MM-01" --until="YYYY-MM-DD" --all --decorate=full --source`
- **Skill:** `/generar-commits`
- **Aplica a:** IDARTES, SDMUJER, IDT, UAECD

### 2. Soportes GLPI (Mesa de Servicios)
- **Fuente:** API GLPI REST (preferido) o exportacion CSV/Excel
- **Skill:** `/generar-soportes-glpi` (con fallback API → archivo)
- **Skill API:** `/extraer-tickets-glpi`
- **Aplica a:** IDARTES, SDMUJER

### 3. Soportes por Correo (Mesa de Servicios)
- **Fuente:** API Gmail/Outlook (preferido) o PDF exportado
- **Skill:** `/generar-soportes-correo` (con fallback API → archivo)
- **Skills API:** `/extraer-correos-gmail`, `/extraer-correos-outlook`
- **Aplica a:** IDT (Gmail), UAECD (Outlook)

### 4. Historias de Usuario (Jira)
- **Fuente:** API Jira Cloud via MCP
- **Skill:** `/extraer-issues-jira`
- **Aplica a:** IDARTES

### 5. Casos de Prueba
- **Fuente:** Documentos Excel/Word
- **Formato:** Varia por entidad
- **Aplica a:** IDARTES, SDMUJER, UAECD

### 6. Plan de Accion TI (SDMUJER)
- **Fuente:** Archivos en carpeta OneDrive del periodo
- **Skill:** Especifico SDMUJER

---

## DIRECTRICES DE REDACCION (TODAS LAS ENTIDADES)

**Fuente:** Memorando SDMUJER 3-2026-000375 (aplica como lineamiento general para todas las entidades).

1. **Primera persona + pasado:** "Realice la implementacion", "Atendi N solicitudes", "Desarrolle el modulo"
2. **Clara, detallada y verificable:** Cada actividad debe permitir evidenciar el cumplimiento de la obligacion contractual
3. **Sin calificativos:** Evitar "gran esfuerzo", "significativo avance", "atencion oportuna"
4. **Objetivo:** Justificar trabajo realizado en el periodo
5. **Prohibido:**
   - Inventar actividades no documentadas
   - Usar calificativos subjetivos
   - Repetir anexos en multiples obligaciones sin justificacion
6. **Obligatorio:**
   - Citar evidencia especifica al final de cada justificacion
   - Si no hay actividad para una obligacion, indicar explicitamente
   - Las evidencias deben corresponder al periodo reportado
   - Para reuniones con compromisos, incluir evidencia (acta, correo o captura)

---

## REGLAS DE ORTOGRAFIA ESPAÑOL (OBLIGATORIO EN TODO TEXTO GENERADO)

### Tildes obligatorias

**Verbos en pasado (pretérito):** realizó, implementó, validó, configuró, desarrolló, ejecutó, gestionó, atendió, resolvió, diseñó, corrigió, ajustó, actualizó, verificó, documentó, coordinó, participó, presentó, revisó, efectuó, brindó, elaboró, identificó, integró, optimizó, generó, registró, procesó, adelantó, estableció

**Sustantivos y términos técnicos:** gestión, atención, módulo, período, aplicación, configuración, implementación, documentación, información, resolución, integración, solución, ejecución, administración, planeación, contratación, evaluación, coordinación, operación, función, versión, descripción, migración, validación, corrección, comunicación

**Palabras comunes:** también, además, según, través (a través), técnico/a, específico/a, único/a, último/a, número, código, método, automático/a, electrónico/a, página, teléfono, próximo/a, día, más, así, aquí

### Prohibiciones

- **No mayúsculas sostenidas** en texto redactado (excepto siglas: GLPI, UAECD, IDARTES, etc.)
- **No omitir tildes** — cada palabra de la lista anterior DEBE llevar tilde siempre

### Alcance

Aplica a TODO texto generado por el sistema: informe de obligaciones, evidencias, commits, reuniones, soportes, log de ejecución.

---

## FLUJO DE GENERACION DE INFORMES

### Entrada
```
Entidad: [IDARTES|SDMUJER|IDT|UAECD]
Periodo: [YYYY-MM-DD] a [YYYY-MM-DD]
```

### Proceso (Paso a Paso)

```
/generar-informe [ENTIDAD] [FECHA_INICIO] [FECHA_FIN]
   │
   ├── PASO 0:  Resolver rutas + inicializar log
   ├── PASO 0B: Verificar/crear estructura de carpetas
   │   └── Crea carpeta_evidencias y subcarpetas si no existen
   │   └── Si existe con contenido, pregunta al usuario
   ├── PASO 1:  Cargar config + README
   │
   ├── PASO 2:  Extraer insumos via API (con subagentes paralelos)
   │   ├── 2A: /extraer-tickets-glpi O subagente Gmail/Outlook
   │   ├── 2B: Subagente Jira (background, solo IDARTES)
   │   ├── 2C: Subagente Gmail suplementario (background, IDARTES)
   │   ├── 2D: /extraer-reuniones-calendario
   │   └── 2E: /resumen-reuniones → .md + .docx
   │
   ├── PASO 3:  /buscar-evidencias → evidencias_{entidad}_{mes}.md
   ├── PASO 4:  /generar-commits → .md + .docx
   ├── PASO 5:  /generar-soportes-{glpi|correo} → .md (+ .xlsx si CSV local)
   ├── PASO 6:  /generar-plan-accion → .md + .docx (solo SDMUJER, via /md-to-docx)
   │
   ├── PASO 7:  Consolidar inventario
   ├── PASO 8:  Mapear a obligaciones
   ├── PASO 9:  Redactar justificacion
   ├── PASO 10: Organizar anexos en carpetas OBLIGACION_N/ → OBLIGACION_1/, OBLIGACION_2/, ...
   └── PASO 11: Guardar informe en {carpeta_mes}/
```

### Salida
- Archivos `.md` generados en `{carpeta_evidencias}/` (= `{carpeta_mes}/ANEXOS/`)
- Carpetas `OBLIGACION_1/`, `OBLIGACION_2/`, etc. con entregables (.docx, .xlsx) segun config.json
- Informe final en `{carpeta_mes}/Informe_Obligaciones_{ENTIDAD}_{mes}_{year}.md`
- Log de ejecucion en `{carpeta_mes}/log_{entidad}_{mes}_{year}.md`
- Entregables Word/Excel en `{carpeta_fuentes}/`

---

## SKILLS DISPONIBLES

| Skill | Descripcion | Argumentos | Entidades |
|-------|-------------|------------|-----------|
| `/buscar-evidencias` | Busca archivos, lee con MCP, crea carpetas OBLIGACION_N/ | `ENTIDAD FECHA_INICIO FECHA_FIN` | Todas |
| `/generar-commits` | Extrae y formatea commits del periodo | `ENTIDAD FECHA_INICIO FECHA_FIN` | Todas |
| `/generar-soportes-glpi` | Procesa tickets GLPI (API-first, fallback a archivo) | `ENTIDAD FECHA_INICIO FECHA_FIN [ARCHIVO]` | IDARTES, SDMUJER |
| `/generar-soportes-correo` | Procesa correos (API-first, fallback a PDF) | `ENTIDAD FECHA_INICIO FECHA_FIN [ARCHIVO]` | IDT, UAECD |
| `/resumen-reuniones` | Procesa transcripciones y genera resumen de reuniones | `ENTIDAD FECHA_INICIO FECHA_FIN` | Todas |
| `/generar-informe` | Orquesta sub-skills y genera informe completo | `ENTIDAD FECHA_INICIO FECHA_FIN` | Todas |
| `/extraer-issues-jira` | Extrae issues de Jira Cloud via MCP | `ENTIDAD FECHA_INICIO FECHA_FIN` | IDARTES |
| `/extraer-correos-gmail` | Extrae correos enviados via Gmail API MCP | `ENTIDAD FECHA_INICIO FECHA_FIN` | IDT, IDARTES |
| `/extraer-correos-outlook` | Extrae correos enviados via Outlook M365 MCP | `ENTIDAD FECHA_INICIO FECHA_FIN` | SDMUJER, UAECD |
| `/extraer-tickets-glpi` | Extrae tickets GLPI via REST API (script Python) | `ENTIDAD FECHA_INICIO FECHA_FIN` | IDARTES, SDMUJER |
| `/generar-plan-accion` | Genera reporte Plan de Accion (indicador seguridad digital) | `ENTIDAD FECHA_INICIO FECHA_FIN` | SDMUJER |
| `/extraer-reuniones-calendario` | Extrae reuniones del calendario via API (Google/Outlook) | `ENTIDAD FECHA_INICIO FECHA_FIN` | Todas |

---

## USO RAPIDO

```bash
# Flujo completo automatizado (orquesta todos los sub-skills)
/generar-informe IDT 2026-01-16 2026-01-31

# Flujo manual paso a paso para IDARTES enero 2026
/buscar-evidencias IDARTES 2026-01-01 2026-01-31
/generar-commits IDARTES 2026-01-01 2026-01-31
/generar-soportes-glpi IDARTES 2026-01-01 2026-01-31
/extraer-issues-jira IDARTES 2026-01-01 2026-01-31
/generar-informe IDARTES 2026-01-01 2026-01-31

# Soportes con archivo especifico (fallback manual)
/generar-soportes-glpi IDARTES 2026-01-01 2026-01-31 /ruta/glpi.xlsx
/generar-soportes-correo IDT 2026-01-16 2026-01-31 /ruta/correos.pdf

# Extraccion directa via API (sin generar informe)
/extraer-issues-jira IDARTES 2026-02-01 2026-02-28
/extraer-correos-gmail IDT 2026-02-01 2026-02-28
/extraer-correos-outlook UAECD 2026-02-01 2026-02-28
/extraer-tickets-glpi SDMUJER 2026-02-01 2026-02-28
/extraer-reuniones-calendario IDT 2026-02-01 2026-02-28

# Solo extraer commits de SDMUJER
/generar-commits SDMUJER 2026-01-01 2026-01-31

# Solo generar resumen de reuniones
/resumen-reuniones IDT 2026-01-16 2026-01-31

# Buscar documentos de UAECD sin generar informe
/buscar-evidencias UAECD 2026-01-01 2026-01-31
```

---

## CONFIGURACION MCP REQUERIDA

### Lectura de documentos (obligatorio)

**Servidor:** `user-awslabs.document-loader-mcp-server`

| Herramienta | Tipo de archivo | Argumentos |
|-------------|-----------------|------------|
| `read_document` | PDF, DOCX, XLSX, PPTX | `file_path`, `file_type` |
| `read_image` | PNG, JPG, JPEG | `file_path` |

### Integraciones API (opcionales, configuradas en `.mcp.json`)

Los skills de extraccion API usan MCP servers configurados en `.mcp.json`. Cada uno requiere credenciales en `.env`:

| MCP Server | Paquete | Entidad | Credenciales |
|------------|---------|---------|-------------|
| `jira-idartes` | `mcp-atlassian` (uvx) | IDARTES | `JIRA_IDARTES_EMAIL`, `JIRA_IDARTES_API_TOKEN` |
| `gmail-idt` | `@gongrzhe/server-gmail-autoauth-mcp` (npx) | IDT | OAuth en `~/.gmail-mcp/` |
| `gmail-idartes` | `@gongrzhe/server-gmail-autoauth-mcp` (npx) | IDARTES | OAuth en `~/.gmail-mcp/` |
| `outlook-sdmujer` | `@softeria/ms-365-mcp-server` (npx) | SDMUJER | `SDMUJER_TENANT_ID`, `CLIENT_ID`, `CLIENT_SECRET` |
| `outlook-uaecd` | `@softeria/ms-365-mcp-server` (npx) | UAECD | `UAECD_TENANT_ID`, `CLIENT_ID`, `CLIENT_SECRET` |
| `calendar-idt` | `@cocal/google-calendar-mcp` (npx) | IDT | OAuth en `~/.google-calendar-mcp/` |
| `calendar-idartes` | `@cocal/google-calendar-mcp` (npx) | IDARTES | OAuth en `~/.google-calendar-mcp/` |

**Outlook Calendar** (SDMUJER, UAECD) reutiliza los MCP servers `outlook-sdmujer` y `outlook-uaecd` que ya soportan `list-calendar-events`.

**GLPI** usa un script Python (`scripts/glpi_extract.py`) en vez de MCP, con variables `GLPI_{ENTIDAD}_URL`, `_APP_TOKEN`, `_USER_TOKEN`.

### Principio API-first con Fallback

Los skills de soportes (`generar-soportes-glpi`, `generar-soportes-correo`) tienen un **PASO 1.5** que intenta la API primero. Si falla o no esta configurada, continua con el flujo manual (archivo local). Sin credenciales configuradas, todo funciona como antes.

---

## NOTAS TECNICAS

- **MCP requerido:** `awslabs.document-loader-mcp-server` para lectura de PDF/DOCX/XLSX/PPTX
- **MCP opcionales:** `mcp-atlassian` (Jira), `@gongrzhe/server-gmail-autoauth-mcp` (Gmail), `@softeria/ms-365-mcp-server` (Outlook) — configurados en `.mcp.json`
- **Script GLPI:** `scripts/glpi_extract.py` — extraccion directa via REST API sin dependencia de MCP
- **Scripts entregables:** `commits_to_docx.py`, `glpi_to_excel.py`, `jira_to_excel.py`, `correos_to_docx.py`, `reuniones_to_docx.py` — generan Word/Excel desde JSON
- **Credenciales:** `.env` (gitignored), template en `.env.example`
- **Repositorio Pandora:** Multiples repositorios (pandora_proxy, apiadministrador, apiplaneacion, modadministrador, modplaneacionoap, modcontratacion, modpazysalvo)
- **Ruta git comun:** (configurar en entidades/*/config.json → git.ruta_proyecto)
- **Subagentes:** `generar-informe` usa Agent tool (subagent_type: "general-purpose") para Jira y Gmail, corriendo en background para paralelizar
- **Anexos estructurados:** `config.json["anexos"]` es un objeto con metadata (nombre, extension, obligaciones, fuente_key, manual) que determina carpetas numeradas en PASO 10
- **PASO 0 compartido:** `.claude/skills/shared/paso0-rutas.md` — resolucion de rutas identica para los 11 skills. Cada skill referencia este archivo en vez de duplicar el bloque
- **Ahorro de tokens:** Los skills estan disenados para que la IA reciba instrucciones claras y estructuradas, minimizando el contexto necesario
- **nombre_corto:** Campo opcional en `config.json["anexos"]` — cuando presente, PASO 10 usa este nombre como archivo destino en lugar de `nombre`. Permite cumplir restricciones de longitud por entidad.
