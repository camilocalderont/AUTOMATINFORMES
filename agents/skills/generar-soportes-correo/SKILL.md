---
name: generar-soportes-correo
description: "Processes support emails (API-first via Gmail/Outlook with fallback to local PDF) to generate a justified support obligation report with classification, statistics, and email detail table. Use when user says \"generar soportes correo\", \"email support report\", \"reporte correos soporte\", or needs helpdesk-via-email evidence for IDT or UAECD."
argument-hint: "[ENTIDAD] [FECHA_INICIO] [FECHA_FIN]"
metadata:
  author: solercia
  version: "1.0.0"
  category: documentation
  tags: [correos, soporte, mesa-servicios, gmail]
---

# Skill: Generar Reporte de Soportes por Correo

## ENTRADA
- **$0**: Entidad (IDT, UAECD)
- **$1**: Fecha inicio (YYYY-MM-DD)
- **$2**: Fecha fin (YYYY-MM-DD)
- **$3** *(opcional)*: Ruta al archivo PDF de correos. Si no se proporciona, se auto-localiza.

## PROCESO

### PASO 0: Resolver rutas

Ejecutar la resolucion de rutas estandar segun `.claude/skills/shared/paso0-rutas.md`.

**Variables adicionales de este skill:**
- `{dia_actual}` = `date +%Y-%m-%d`
- Verificar `{carpeta_evidencias}` existe; si no, buscar desde `{carpeta_mes}` o preguntar al usuario.

### PASO 1: Validar entidad
Solo IDT y UAECD usan correo como mesa de servicios. Si la entidad es IDARTES o SDMUJER, indicar que deben usar `/generar-soportes-glpi`.

### PASO 1.5: Intentar extraccion via API (si disponible)

**Nota:** Si se proporciono $3 (ruta a archivo), saltar este paso completo y usar el archivo directamente.

**PASO 1.5A: Verificar extraccion previa**

Antes de llamar la API, verificar si ya existe el archivo de extraccion API en `{carpeta_evidencias}`:
```bash
ls "{carpeta_evidencias}/correos_api_{entidad_lower}_{mes}.md" 2>/dev/null
```

- **Si existe** → Leer ese archivo y usarlo como base para generar el reporte de soportes. **Saltar a PASO 4** (no re-extraer).
- **Si NO existe** → Continuar a PASO 1.5B.

**PASO 1.5B: Extraer via API**

Verificar si la entidad tiene API de correo configurada en `config.json`:

1. **Si tiene `api.gmail`** (IDT, IDARTES):
   - Ejecutar `/extraer-correos-gmail $0 $1 $2`
   - Si la extraccion es exitosa:
     - El output se guarda en `{carpeta_evidencias}/correos_api_{entidad_lower}_{mes}.md`
     - Leer ese archivo y usarlo como base para generar el reporte de soportes
     - **Saltar a PASO 4** (ya se tiene el contenido de los correos)
   - Si falla (MCP no disponible, error de autenticacion, etc.):
     - Registrar el error en la conversacion
     - Continuar a PASO 2 (fallback a archivo PDF local)

2. **Si tiene `api.outlook`** (SDMUJER, UAECD):
   - Ejecutar `/extraer-correos-outlook $0 $1 $2`
   - Misma logica: exito → PASO 4, fallo → PASO 2

3. **Si NO tiene API configurada:**
   - Continuar a PASO 2 (flujo actual sin cambios)

### PASO 2: Localizar archivo de correos

**Si $3 fue proporcionado:** Usar esa ruta directamente.

**Si $3 NO fue proporcionado:** Auto-localizar en 3 niveles de busqueda:

**Nivel 1 - FUENTES** (prioridad maxima, archivos fuente del informe con fecha hasta hoy):
```bash
find "{carpeta_fuentes}" -type f \
  -newermt "$1" -not -newermt "{dia_actual}" \
  \( -name "*correo*soporte*.pdf" -o -name "*correos*soporte*.pdf" -o -name "*soporte*.pdf" -o -name "*correo*.pdf" \) \
  2>/dev/null
```

**Nivel 2 - carpeta_evidencias** (archivos modificados en el periodo):
```bash
find "{carpeta_evidencias}" -type f \
  -newermt "$1" -not -newermt "$2" \
  \( -name "*correo*soporte*.pdf" -o -name "*correos*soporte*.pdf" -o -name "*soporte*.pdf" \) \
  2>/dev/null
```

**Nivel 3 - carpeta_anual** (fallback, excluyendo INFORMES/):
```bash
find "{carpeta_anual}" -type f \
  -newermt "$1" -not -newermt "$2" \
  -not -path "*/INFORMES/*" \
  \( -name "*correo*soporte*.pdf" -o -name "*correos*soporte*.pdf" -o -name "*soporte*.pdf" \) \
  2>/dev/null
```

**REGLA:** Usar el primer nivel que devuelva resultados. La carpeta FUENTES/ es donde el usuario deja los PDFs de correos exportados para el informe, y se busca con `{dia_actual}` como limite porque se generan despues del periodo.

Si se encuentra mas de un archivo, usar el mas reciente.

**Si no se encuentra ningun archivo Y la API tampoco genero datos (PASO 1.5):**
- NO solicitar ruta manualmente
- Redactar el reporte indicando: "Durante el periodo reportado no se registraron solicitudes de soporte atendidas por correo electronico."
- Saltar a PASO 7 (guardar output con el mensaje de no actividad)

### PASO 3: Leer archivo PDF
Usar MCP `read_document` para archivos PDF:
```json
{
  "file_path": "{ruta_archivo}",
  "file_type": "pdf"
}
```

**Fallback si `read_document` falla:** Si el MCP no responde, intentar leer el PDF con la herramienta `Read` nativa (extrae texto parcial). Si tampoco funciona, alertar al usuario indicando el archivo que no pudo leerse.

### PASO 4: Extraer informacion de correos
De cada correo extraer:
- Fecha de envio
- Asunto
- Destinatario(s)
- Resumen del contenido (soporte brindado)

### PASO 5: Clasificar por tipo de soporte
- Soporte funcional (uso del sistema)
- Soporte tecnico (errores, bugs)
- Consultas (como hacer X)
- Capacitacion (explicaciones detalladas)

### PASO 6: Generar contenido

#### A) Resumen General
```
Durante el periodo reportado se brindo soporte especializado a traves
de [N] comunicaciones por correo electronico, atendiendo consultas
relacionadas con [modulos/funcionalidades].
```

#### B) Detalle por Tipo
- Soportes funcionales: N
- Soportes tecnicos: N
- Consultas: N
- Capacitaciones: N

#### C) Tabla de Correos
| Fecha | Asunto | Tipo | Descripcion |
|-------|--------|------|-------------|

### PASO 7: Guardar output

Guardar el contenido generado en:
```
{carpeta_evidencias}/soportes_correo_{entidad_lower}_{mes}.md
```

Ejemplo: `.../ANEXOS/soportes_correo_idt_enero.md`

**Tambien mostrar el resultado en la conversacion** para que el usuario pueda revisarlo.

## DIRECTRICES DE REDACCION

1. **Primera persona + pasado**: "Brinde soporte especializado", "Atendi la consulta", "Resolvi el incidente"
2. **Claro y verificable**: Cantidades, tipos, destinatarios
3. **Sin calificativos**: Evitar "atencion oportuna", "soporte efectivo"
4. **Objetivo**: Justificar la obligacion de soporte
5. **Evidencia**: Referenciar el anexo correspondiente de config.json (`anexos.correos_soporte`)
6. **Ortografia:** Aplicar TODAS las reglas de "REGLAS DE ORTOGRAFIA ESPAÑOL" de CLAUDE.md

## Ejemplos

### Ejemplo 1: Extraccion via API exitosa
User says: `/generar-soportes-correo IDT 2026-02-01 2026-02-28`
Actions:
1. PASO 1.5A: No existe correos_api_idt_febrero.md
2. PASO 1.5B: Ejecuta /extraer-correos-gmail → extrae 18 correos
3. PASO 4: Lee el .md generado, clasifica correos
4. PASO 6: Genera reporte con tabla y estadisticas
Result: `soportes_correo_idt_febrero.md`

### Ejemplo 2: API no disponible, fallback a PDF
User says: `/generar-soportes-correo UAECD 2026-02-01 2026-02-28`
Actions:
1. PASO 1.5B: Outlook MCP no configurado → falla
2. PASO 2: Auto-localiza correos_soporte.pdf en carpeta_fuentes
3. Lee PDF con MCP read_document, extrae correos
4. Genera reporte
Result: `soportes_correo_uaecd_febrero.md`

## ARCHIVO GENERADO

| Campo | Valor |
|-------|-------|
| Nombre | `soportes_correo_{entidad_lower}_{mes}.md` |
| Ubicacion | `{carpeta_evidencias}/` |
| Ejemplo | `.../01. ENERO/ANEXOS/soportes_correo_idt_enero.md` |
