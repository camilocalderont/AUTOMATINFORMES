---
name: generar-commits
description: "Extracts git commits for a specific entity and date range from multiple Pandora repositories, generates a formatted weekly summary with functional descriptions, complete commit table, and Word document. Use when user says \"generar commits\", \"extract commits\", \"commit report\", \"reporte de commits\", or needs git activity evidence for a reporting period."
argument-hint: "[ENTIDAD] [FECHA_INICIO] [FECHA_FIN]"
metadata:
  author: solercia
  version: "1.0.0"
  category: data-processing
  tags: [git, commits, desarrollo, pandora]
---

# Skill: Generar Reporte de Commits

## ENTRADA
- **$0**: Entidad (IDARTES, SDMUJER, IDT, UAECD)
- **$1**: Fecha inicio (YYYY-MM-DD)
- **$2**: Fecha fin (YYYY-MM-DD)

## PROCESO

### PASO 0: Resolver rutas

Ejecutar la resolucion de rutas estandar segun `.claude/skills/shared/paso0-rutas.md`.

Verificar `{carpeta_evidencias}` existe; si no, buscar desde `{carpeta_mes}` o preguntar al usuario.

### PASO 1: Construir y ejecutar comando unico de extraccion

Del config.json ya leido, construir las variables:
- `{author_filter}` = `correo_autor[]` unido con `\|`
- `{branch_filters}` = `--branches='{rama_principal}*'` + un `--branches='{patron}'` por cada elemento de `git.patrones_ramas`
- `{ruta_proyecto}` = `git.ruta_proyecto`

Ejecutar un **unico comando** que auto-descubre repos y extrae commits:

```bash
for gitdir in $(find "{ruta_proyecto}" -maxdepth 2 -name ".git" -type d 2>/dev/null | sort); do
  repo_dir=$(dirname "$gitdir")
  repo_name=$(basename "$repo_dir")
  (cd "$repo_dir" && \
   GIT_PAGER=cat git log \
     --author="{author_filter}" \
     --since="$1" --until="$2" \
     {branch_filters} \
     --format="$repo_name|%H|%h|%ad|%s|%D" \
     --date=format:"%Y-%m-%d %H:%M" \
     2>/dev/null)
done
```

**Ejemplo concreto para IDT:** ver `examples/salida_esperada.md`

**Formato de salida:** `repo_name|hash_completo|hash_corto|fecha|mensaje|decoraciones`

Cada linea es un commit. Si no hay output, no hubo commits en el periodo para esa entidad.

### PASO 2: Generar contenido

El archivo .md DEBE seguir estrictamente este orden de secciones:

#### A) Descripcion General (2-3 parrafos detallados)

Redactar en primera persona y pasado:
- Areas de trabajo del periodo (que modulos/sistemas se tocaron)
- Repositorios con actividad y cantidad de commits por cada uno
- Resumen ejecutivo de los cambios principales (funcionalidades, correcciones, mejoras)

#### B) Desarrollos Semana a Semana

Para cada semana del periodo que tenga commits:

```
### Semana N (dd/mm - dd/mm)
Estado: Finalizado
Fecha Inicio: dd/mm/aaaa
Fecha Fin: dd/mm/aaaa
Funcionalidades:
- [Descripcion funcional detallada, NO solo el mensaje del commit]
- [Agrupar commits relacionados en una sola funcionalidad]
- [Usar lenguaje no tecnico orientado a la justificacion de actividades]
```

**Reglas:**
- Agrupar commits que pertenecen a la misma funcionalidad en un solo bullet
- Describir el impacto funcional, no el detalle tecnico del commit
- Semanas sin commits no se incluyen

#### C) Tabla Completa de Commits

```
| # | Commit ID | Repositorio | Rama | Descripcion | Fecha |
|---|-----------|-------------|------|-------------|-------|
| 1 | 8 chars   | nombre repo | nombre rama | mensaje commit | dd/mm/aaaa |
```

Incluir TODOS los commits ordenados por fecha descendente.

### PASO 3: Guardar output .md

Guardar el contenido generado en:
```
{carpeta_evidencias}/commits_{entidad_lower}_{mes}.md
```

Ejemplo: `.../ANEXOS/commits_idt_enero.md`

**Tambien mostrar el resultado en la conversacion** para que el usuario pueda revisarlo.

### PASO 4: Generar documento Word

1. Resolver `{carpeta_fuentes}` (ya resuelto en PASO 0)
2. Construir el JSON intermedio con la estructura requerida por `commits_to_docx.py`:

```json
{
    "entidad": "{$0}",
    "periodo_inicio": "{$1}",
    "periodo_fin": "{$2}",
    "total_commits": N,
    "repositorios": ["repo1", "repo2"],
    "descripcion": "Texto de la seccion A del PASO 2...",
    "semanas": [
        {
            "nombre": "Semana 1 (dd/mm - dd/mm)",
            "estado": "Finalizado",
            "fecha_inicio": "dd/mm/aaaa",
            "fecha_fin": "dd/mm/aaaa",
            "funcionalidades": ["func1", "func2"]
        }
    ],
    "commits": [
        {
            "hash": "8chars",
            "fecha": "YYYY-MM-DD",
            "mensaje": "mensaje del commit",
            "rama": "nombre_rama",
            "repositorio": "nombre_repo"
        }
    ]
}
```

3. Escribir JSON intermedio en: `{carpeta_fuentes}/_commits_data_{entidad_lower}_{mes}.json`
4. Ejecutar:
```bash
python3 scripts/commits_to_docx.py "{carpeta_fuentes}/_commits_data_{entidad_lower}_{mes}.json" "{carpeta_fuentes}/commits_{entidad_lower}_{mes}.docx"
```
5. Si exitoso: eliminar JSON intermedio
6. Informar: "Word generado: `{carpeta_fuentes}/commits_{entidad_lower}_{mes}.docx`"

**Si no hay commits:** No generar Word, solo informar que no se encontraron commits.

## DIRECTRICES DE REDACCION

1. **Primera persona + pasado**: "Implementé el módulo", "Ajusté la configuración", "Corregí el error"
2. **Claro y detallado**: Describir impacto funcional, no solo el detalle técnico
3. **Sin calificativos**: Evitar "gran", "significativo", "importante"
4. **Objetivo**: Justificar la obligacion contractual de desarrollo
5. **No inventar**: Solo incluir commits existentes
6. **Funcionalidades agrupadas**: En la seccion semanal, agrupar commits relacionados en una sola descripcion funcional
7. **Ortografia:** Aplicar TODAS las reglas de "REGLAS DE ORTOGRAFIA ESPAÑOL" de CLAUDE.md

## Ejemplos

### Ejemplo 1: Extraccion estandar
User says: `/generar-commits IDT 2026-01-16 2026-01-31`
Actions:
1. Lee config IDT, resuelve rutas
2. Ejecuta git log en 7 repos con filtros de ramas IDT
3. Encuentra 12 commits en 2 semanas
4. Genera .md con descripcion, semanas y tabla
5. Genera .docx via commits_to_docx.py
Result: `commits_idt_enero.md` + `commits_idt_enero.docx`

### Ejemplo 2: Sin commits
User says: `/generar-commits UAECD 2026-12-01 2026-12-31`
Actions:
1. Lee config UAECD, resuelve rutas
2. Ejecuta git log — sin output
Result: Reporta "No se encontraron commits para UAECD en el periodo", no genera Word

## SALIDA ESPERADA

**Ver formato completo en** `examples/salida_esperada.md`

## ARCHIVOS GENERADOS

| Campo | Tipo | Nombre | Ubicacion |
|-------|------|--------|-----------|
| Markdown | .md | `commits_{entidad_lower}_{mes}.md` | `{carpeta_evidencias}/` |
| Word | .docx | `commits_{entidad_lower}_{mes}.docx` | `{carpeta_fuentes}/` |
