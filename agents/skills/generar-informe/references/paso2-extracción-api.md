# PASO 2: Detalle de extracción API

Ejecutar las extracciones API como insumos previos. **Los pasos 2B, 2C y 2D se pueden lanzar como agentes paralelos.**

## PASO 2A: Mesa de servicios (GLPI o Correo)

Consultar `mesa_servicios.tipo` del config.json:

**Si tipo == "glpi"** (IDARTES, SDMUJER) y tiene `api.glpi` con tokens no vacíos:
```
/extraer-tickets-glpi $0 $1 $2
```

**Si tipo == "correo"** y tiene `api.gmail` (IDT) — **usar Agent tool** (subagent_type: "general-purpose") con prompt que incluya:
1. ToolSearch para cargar herramientas del MCP server `{api.gmail.mcp_server}`
2. Buscar correos: `from:me after:{YYYY/MM/DD} before:{YYYY/MM/DD}`
3. Leer contenido COMPLETO de cada correo (incluyendo hilos RE:/FW:)
4. Clasificar correos por tipo
5. Escribir JSON intermedio en `{carpeta_fuentes}/_correos_data_{entidad_lower}_{mes}.json`
6. Ejecutar `python3 scripts/correos_to_docx.py` para generar .docx
7. Eliminar JSON si exitoso
8. Escribir .md en `{carpeta_evidencias}/correos_api_{entidad_lower}_{mes}.md`

**Si tipo == "correo"** y tiene `api.outlook` (UAECD):
```
/extraer-correos-outlook $0 $1 $2
```

**Si no tiene API o falla:** Registrar en log, continuar (PASO 5 usará fallback).

## PASO 2B: Gestión de proyectos (Jira) — Subagente

**Si tiene `api.jira`** (IDARTES): Lanzar Agent (subagent_type: "general-purpose", **run_in_background: true**) que ejecute:
```bash
python3 scripts/jira_extract.py $0 $1 $2 "{carpeta_evidencias}/jira_issues_{entidad_lower}_{mes}.md" --output-xlsx "{carpeta_fuentes}/jira_{entidad_lower}_{mes}.xlsx"
```

**Si no tiene `api.jira`:** Saltar.

## PASO 2C: Correo suplementario (solo entidades con GLPI + Gmail) — Subagente

Si `mesa_servicios.tipo == "glpi"` Y tiene `api.gmail` (ej: IDARTES): Lanzar Agent (run_in_background: true) con la misma plantilla del PASO 2A (versión Gmail).

## PASO 2D: Calendario

Si tiene `api.calendar`:
```
/extraer-reuniones-calendario $0 $1 $2
```

## PASO 2E: Resumen de reuniones

```
/resumen-reuniones $0 $1 $2
```
→ Genera .md y .docx **antes** de buscar-evidencias para que los entregables sean encontrados.

## Paralelización del PASO 2

2B y 2C se lanzan en **background**. 2D se ejecuta normal. 2E espera (depende de 2D). Finalmente esperar resultados de 2B y 2C con TaskOutput.
