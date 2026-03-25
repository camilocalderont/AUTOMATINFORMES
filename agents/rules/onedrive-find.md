---
name: onedrive-find
description: >
  Protocolo obligatorio para ejecutar find en carpetas de OneDrive o Google Drive.
  OneDrive Files On-Demand no enumera archivos hasta acceder al directorio.
  Requiere warm-up previo, prohíbe -exec stat, y exige retry si retorna 0.
type: rule
scope: path-scoped
paths:
  - "**/*.md"
severity: required
metadata:
  author: solercia
  version: "1.0.0"
  category: architecture
  tags: [onedrive, find, cache, filesystem]
---

# Protocolo OneDrive para find

## Pre-requisitos antes de find

OneDrive Files On-Demand usa un filesystem virtual (FUSE) que no enumera archivos hasta que se accede al directorio. Un `find` desde la raíz retorna 0 archivos en el primer intento.

### Paso 1: Warm-up obligatorio

Antes de CUALQUIER `find` en una carpeta de OneDrive o Google Drive:

```bash
for dir in "{carpeta_raiz}"/*/; do ls "$dir" >/dev/null 2>&1; done
```

### Paso 2: Ejecutar find

Ejecutar el `find` normalmente después del warm-up.

### Paso 3: Retry-once

Si el find retorna 0 archivos después del warm-up, ejecutar UNA vez más. Si sigue en 0, aceptar el resultado (NO ampliar fechas — ver rule `fechas-estrictas`).

## Prohibiciones

- **NUNCA usar `-exec stat -f`** en paths de OneDrive — `stat` falla silenciosamente en paths virtuales, haciendo que find parezca retornar 0
- **NUNCA** asumir que 0 resultados significa "no hay archivos" sin haber hecho warm-up primero
- **NUNCA** ampliar el rango de fechas como compensación por 0 resultados

## Incidentes de referencia

- `find` desde carpeta_anual retornó 0; después de listar subdirectorios, retornó 287+ archivos
- `-exec stat -f` falló silenciosamente en OneDrive, haciendo que find retornara output vacío
