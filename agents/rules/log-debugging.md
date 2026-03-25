---
name: log-debugging
description: >
  Exige que cada paso de ejecución registre en el log los comandos exactos
  ejecutados (con valores sustituidos, no variables) y sus resultados.
  El usuario necesita ver qué se ejecutó para debugging y verificación.
type: rule
scope: path-scoped
paths:
  - "**/*.md"
severity: required
metadata:
  author: solercia
  version: "1.0.0"
  category: documentation
  tags: [log, debugging, comandos, trazabilidad]
---

# Log con comandos exactos

## Regla

Cada paso de ejecución DEBE registrar en el archivo de log:

1. **Comando exacto ejecutado** — con todas las variables ya sustituidas (no `{carpeta_anual}` sino la ruta real)
2. **Resultado del comando** — conteo de archivos, éxito/error, archivos generados
3. **Hora de ejecución** del paso

## Ejemplo correcto

```markdown
### PASO 2A: Carpeta anual
**Comando:**
```bash
find "/Users/camilo/OneDrive/SDMUJER/2026" -type f -newermt "2026-02-01" ! -newermt "2026-03-01" ! -path "*/INFORMES/*"
```
**Resultado:** 98 archivos encontrados
**Hora:** 14:32
```

## Ejemplo INCORRECTO

```markdown
### PASO 2A: Carpeta anual
Se buscaron archivos del período. Se encontraron 98 archivos.
```

## Por qué

Sin ver el comando exacto, el usuario no puede verificar si se usaron las fechas correctas, si se excluyeron los paths correctos, ni reproducir la búsqueda manualmente para debugging.
