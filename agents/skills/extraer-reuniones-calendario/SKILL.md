---
name: extraer-reuniones-calendario
description: Extracts calendar meetings from Google Calendar or Outlook for a specific entity and date range using the corresponding MCP server. Filters relevant meetings, extracts attendee and duration info, cross-references with existing transcriptions. Use when user says "extraer reuniones calendario", "calendar meetings", "extract calendar", "reuniones del calendario", or needs meeting list evidence for any entity.
argument-hint: "[ENTIDAD] [FECHA_INICIO] [FECHA_FIN]"
metadata:
  author: solercia
  version: "1.0.0"
  category: data-processing
  tags: [calendario, reuniones, api, extracción]
  mcp-server: calendar-idt
---

> **REGLAS OBLIGATORIAS** (R1-R7) — ver `agents/skills/shared/paso0-rutas.md#reglas-compactas`. Aplican sin excepción a este skill.


# Skill: Extraer Reuniones del Calendario

Extrae la lista de reuniones del calendario institucional de la entidad en el periodo indicado, usando el MCP server correspondiente (Google Calendar o Outlook).

## ENTRADA
- **$0**: Entidad (IDARTES, SDMUJER, IDT, UAECD)
- **$1**: Fecha inicio (YYYY-MM-DD)
- **$2**: Fecha fin (YYYY-MM-DD)

## PROCESO

### PASO 0: Resolver rutas

Ejecutar la resolucion de rutas estandar segun `.claude/skills/shared/paso0-rutas.md`.

Verificar `{carpeta_evidencias}` existe; si no, buscar desde `{carpeta_mes}` o preguntar al usuario.

### PASO 1: Validar configuracion de calendario

Verificar que la entidad tenga `api.calendar` configurado en `config.json`:

- **Si tiene `api.calendar`:** Continuar con el tipo correspondiente (`google` o `outlook`)
- **Si NO tiene:** Informar al usuario que la entidad no tiene calendario API configurado y terminar.

### PASO 2: Obtener eventos del calendario

#### Si `api.calendar.tipo == "google"` (IDT, IDARTES)

Usar la herramienta `list-events` del MCP server indicado en `api.calendar.mcp_server`:

```
Herramienta: list-events
Servidor: {api.calendar.mcp_server}
Argumentos:
  - timeMin: {$1}T00:00:00-05:00
  - timeMax: {$2}T23:59:59-05:00
  - maxResults: 100
  - singleEvents: true
  - orderBy: startTime
```

**Nota:** Si `list-events` no esta disponible, intentar con `search-events` o listar las herramientas disponibles del MCP server.

#### Si `api.calendar.tipo == "outlook"` (SDMUJER, UAECD)

Usar la herramienta `list-calendar-events` o `get-calendar-view` del MCP server indicado en `api.calendar.mcp_server`:

```
Herramienta: list-calendar-events o get-calendar-view
Servidor: {api.calendar.mcp_server}
Argumentos:
  - startDateTime: {$1}T00:00:00
  - endDateTime: {$2}T23:59:59
  - top: 100
```

**Nota:** Si ninguna herramienta de calendario esta disponible, listar las herramientas del MCP para identificar la correcta.

### PASO 3: Filtrar reuniones relevantes

De todos los eventos obtenidos, **incluir solo**:
- Eventos con participantes (mas de 1 persona)
- Reuniones virtuales (con link de Google Meet, Teams, Zoom, etc.)
- Reuniones presenciales con mas de 1 asistente

**Excluir**:
- Eventos de todo el dia que sean recordatorios o bloques personales (ej: "Almuerzo", "Personal")
- Eventos cancelados
- Eventos donde el usuario declino la invitacion

### PASO 4: Extraer informacion de cada reunion

De cada reunion extraer:
- **Fecha:** Fecha y hora de inicio
- **Duracion:** Tiempo estimado (hora fin - hora inicio)
- **Titulo:** Nombre del evento/reunion
- **Organizador:** Quien agendo la reunion
- **Participantes:** Lista de asistentes (nombres o correos)
- **Tipo:** Virtual (Meet/Teams/Zoom) o Presencial
- **Enlace:** Link de videollamada si existe
- **Estado de asistencia:** Aceptada, tentativa, pendiente

### PASO 5: Generar contenido

#### A) Resumen General
```
Durante el periodo reportado se identificaron [N] reuniones en el
calendario institucional, distribuidas en [N] semanas de trabajo.
Se participó en sesiones de [categorías: seguimiento, planeación,
soporte, capacitación, etc.].
```

#### B) Estadisticas
- Total reuniones en el periodo
- Reuniones por semana
- Reuniones por tipo (virtual vs presencial)
- Reuniones como organizador vs como invitado
- Horas totales estimadas en reuniones

#### C) Tabla de Reuniones
| # | Fecha | Hora | Duración | Reunión | Organizador | Participantes | Tipo |
|---|-------|------|----------|---------|-------------|---------------|------|
| 1 | 2026-02-05 | 10:00 | 1h | Sprint Planning | fulano@entidad.gov.co | 5 | Virtual |

#### D) Detalle por semana (opcional)
Agrupar reuniones por semana para facilitar la redaccion del informe.

### PASO 6: Cruzar con transcripciones existentes

Verificar si ya existen transcripciones descargadas en `{carpeta_reuniones}`:

```bash
find "{carpeta_reuniones}" -type f \( -name "*.md" -o -name "*.docx" \) 2>/dev/null
```

Para cada reunion del calendario, marcar si tiene transcripcion disponible:
- **Con transcripcion** → Indicar el archivo
- **Sin transcripcion** → Marcar como "Solo datos de calendario"

Esto permite que `/resumen-reuniones` sepa cuales reuniones puede detallar (con transcripcion) y cuales solo listar (sin transcripcion).

### PASO 7: Guardar output

Guardar el contenido generado en:
```
{carpeta_evidencias}/reuniones_calendario_{entidad_lower}_{mes}.md
```

Ejemplo: `.../ANEXOS/reuniones_calendario_idt_febrero.md`

**Tambien mostrar el resultado en la conversacion** para que el usuario pueda revisarlo.

## MANEJO DE ERRORES

**Ver detalle en** `references/manejo-errores.md`

Si MCP falla: registrar error → ofrecer fallback manual (archivo .md/.csv en carpeta_fuentes) → indicar pasos de solución según tipo (Google/Outlook).

## MAPEO A OBLIGACIONES

Las reuniones evidencian coordinacion y participacion. Segun la entidad:

| Entidad | Obligacion | Descripcion |
|---------|------------|-------------|
| IDARTES | 9 | Asistir a reuniones del area de tecnologia |
| IDT | 6 | Participar en reuniones de seguimiento y coordinacion |
| SDMUJER | 10 | Asistir a reuniones convocadas por la supervision |
| UAECD | 7 | Participar en las reuniones convocadas |

## Ejemplos

### Ejemplo 1: Google Calendar exitoso
User says: `/extraer-reuniones-calendario IDT 2026-02-01 2026-02-28`
Actions:
1. Conecta a calendar-idt MCP, lista eventos del periodo
2. Filtra: 18 reuniones relevantes (excluye 3 eventos personales)
3. Cruza con transcripciones: 7 tienen archivo .md
4. Genera tabla con columna de transcripcion
Result: `reuniones_calendario_idt_febrero.md`

### Ejemplo 2: MCP de calendario no configurado
User says: `/extraer-reuniones-calendario UAECD 2026-02-01 2026-02-28`
Actions:
1. api.calendar configurado como outlook pero MCP no responde
2. Informa: "Outlook Calendar MCP no disponible"
3. Sugiere: verificar credenciales Azure AD
Result: No genera archivo, muestra pasos de solucion

## ARCHIVO GENERADO

| Campo | Valor |
|-------|-------|
| Nombre | `reuniones_calendario_{entidad_lower}_{mes}.md` |
| Ubicacion | `{carpeta_evidencias}/` |
| Ejemplo | `.../ANEXOS/reuniones_calendario_idt_febrero.md` |

## SALIDA ESPERADA

**Ver formato completo en** `examples/salida_esperada.md`
