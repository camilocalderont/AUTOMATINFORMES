---
name: extraer-tickets-glpi
description: Extracts GLPI helpdesk tickets via REST API using the glpi_extract.py Python script for a specific entity and date range. Generates Markdown report with ticket details and Excel deliverable with summary sheets. Use when user says "extraer tickets glpi", "GLPI API", "extract GLPI tickets", "tickets mesa servicios", or needs raw GLPI data for IDARTES or SDMUJER.
argument-hint: "[ENTIDAD] [FECHA_INICIO] [FECHA_FIN]"
metadata:
  author: solercia
  version: "1.0.0"
  category: data-processing
  tags: [glpi, tickets, api, mesa-servicios]
---

> **REGLAS OBLIGATORIAS** (R1-R7) — ver `agents/skills/shared/paso0-rutas.md#reglas-compactas`. Aplican sin excepción a este skill.


# Skill: Extraer Tickets de GLPI via API

Extrae tickets de la mesa de servicios GLPI en el periodo indicado, usando el script Python `scripts/glpi_extract.py` que consume la REST API de GLPI.

## ENTRADA
- **$0**: Entidad (IDARTES o SDMUJER)
- **$1**: Fecha inicio (YYYY-MM-DD)
- **$2**: Fecha fin (YYYY-MM-DD)

## PROCESO

### PASO 0: Resolver rutas

Ejecutar la resolucion de rutas estandar segun `.claude/skills/shared/paso0-rutas.md`.

Verificar `{carpeta_evidencias}` existe; si no, buscar desde `{carpeta_mes}` o preguntar al usuario.

### PASO 1: Validar entidad y configuracion API

1. Solo IDARTES y SDMUJER usan GLPI. Si otra entidad, informar y terminar.
2. Verificar que la entidad tenga `api.glpi` en su config.json.
3. Si no tiene configuracion API, informar que se requieren las variables de entorno y terminar.

### PASO 2: Ejecutar script de extraccion

1. Definir la ruta de salida del .md:
```
{output_path} = {carpeta_evidencias}/tickets_glpi_api_{entidad_lower}_{mes}.md
```

2. Resolver `{carpeta_fuentes}` desde `config.json rutas.carpeta_fuentes`:
   - Reemplazar `{carpeta_evidencias}` en el valor de `rutas.carpeta_fuentes`
   - Si `rutas.carpeta_fuentes` no existe en config → usar `{carpeta_evidencias}/FUENTES/`
   - Ejecutar: `mkdir -p "{carpeta_fuentes}"`

3. Definir la ruta de salida del .xlsx:
```
{xlsx_path} = {carpeta_fuentes}/glpi_{entidad_lower}_{mes}.xlsx
```

4. Ejecutar con ambas salidas:
```bash
python3 scripts/glpi_extract.py $0 $1 $2 "{output_path}" --output-xlsx "{xlsx_path}"
```

### PASO 3: Verificar resultado

- Si el script termina con exit code 0:
  - Leer el archivo generado en `{output_path}`
  - Mostrar el contenido en la conversacion
  - Informar si el Excel fue generado: `{xlsx_path}`
- Si falla:
  - Mostrar el error al usuario
  - Indicar posibles causas:
    1. Variables de entorno no configuradas (`.env`)
    2. API GLPI no habilitada por el administrador
    3. App Token o User Token invalidos
    4. URL de API incorrecta

## PREREQUISITOS

Variables de entorno en `.env`:
```
GLPI_{ENTIDAD}_URL=https://glpi.{entidad}.gov.co/apirest.php
GLPI_{ENTIDAD}_APP_TOKEN=<generado-por-admin>
GLPI_{ENTIDAD}_USER_TOKEN=<generado-desde-perfil>
```

## EJEMPLO DE USO

```
/extraer-tickets-glpi IDARTES 2026-02-01 2026-02-28
/extraer-tickets-glpi SDMUJER 2026-02-01 2026-02-28
```

## Ejemplos

### Ejemplo 1: Extraccion exitosa
User says: `/extraer-tickets-glpi IDARTES 2026-02-01 2026-02-28`
Actions:
1. Verifica api.glpi en config, ejecuta glpi_extract.py
2. Extrae 25 tickets del periodo via REST API
3. Genera .md con tabla y .xlsx con hojas Resumen + Tickets
Result: `tickets_glpi_api_idartes_febrero.md` + `glpi_idartes_febrero.xlsx`

### Ejemplo 2: Variables de entorno faltantes
User says: `/extraer-tickets-glpi SDMUJER 2026-02-01 2026-02-28`
Actions:
1. glpi_extract.py falla: "GLPI_SDMUJER_URL not set"
2. Indica: configurar GLPI_SDMUJER_URL, _APP_TOKEN, _USER_TOKEN en .env
Result: No genera archivos, muestra instrucciones de configuracion

## ARCHIVOS GENERADOS

| Campo | Valor |
|-------|-------|
| Nombre MD | `tickets_glpi_api_{entidad_lower}_{mes}.md` |
| Ubicacion MD | `{carpeta_evidencias}/` |
| Nombre Excel | `glpi_{entidad_lower}_{mes}.xlsx` |
| Ubicacion Excel | `{carpeta_fuentes}/` |
| Ejemplo MD | `.../ANEXOS/tickets_glpi_api_idartes_febrero.md` |
| Ejemplo Excel | `.../FUENTE/glpi_idartes_febrero.xlsx` |
