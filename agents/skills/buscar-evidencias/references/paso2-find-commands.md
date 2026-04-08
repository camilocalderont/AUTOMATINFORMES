# PASO 2: Comandos find detallados

## PASO 2 PRE: Calentar caché OneDrive

OneDrive Files On-Demand no enumera archivos hasta que se accede al directorio. Ejecutar ANTES de los find:

```bash
for dir in "{carpeta_anual}"/*/; do ls "$dir" >/dev/null 2>&1; done
```

Esto fuerza la enumeración de archivos en cada subcarpeta de primer nivel.

## PASO 2A: Carpeta ANUAL — archivos del período en toda la carpeta anual

```bash
find "{carpeta_anual}" \
  -type f \
  -newermt "$1" ! -newermt "$2" \
  ! -name ".DS_Store" \
  ! -name "*.tmp" \
  ! -name "~*" \
  ! -path "*/node_modules/*" \
  ! -path "*/.git/*" \
  ! -path "*/INFORMES/*" \
  2>/dev/null | sort
```

**Si devuelve 0:** Reintentar UNA vez (a veces OneDrive necesita un segundo acceso). Si sigue en 0, reportar 0 y continuar.

**Después del find, reportar:** "PASO 2A: {N} archivos en carpeta_anual"
**Comando ejecutado:** Pegar el comando find exacto con las fechas sustituidas (para el log).

## PASO 2B: Carpeta EVIDENCIAS — anexos dejados manualmente en el período

```bash
find "{carpeta_evidencias}" \
  -type f \
  -newermt "$1" ! -newermt "$2" \
  ! -name ".DS_Store" \
  ! -name "*.tmp" \
  ! -name "~*" \
  ! -path "*/node_modules/*" \
  ! -path "*/.git/*" \
  2>/dev/null | sort
```
**Después del find, reportar:** "PASO 2B: {N} archivos en carpeta_evidencias"
**Comando ejecutado:** Pegar el comando find exacto con las fechas sustituidas.

## PASO 2C: Carpeta FUENTES — insumos generados (transcripciones, correos, GLPI, Jira)

La carpeta `{carpeta_fuentes}` contiene fuentes base para el informe. Estos archivos se generan **después** del período reportado, por lo que el rango va desde `$1` hasta `{dia_siguiente}` (incluye archivos creados hoy):

```bash
find "{carpeta_fuentes}" \
  -type f \
  -newermt "$1" ! -newermt "{dia_siguiente}" \
  ! -name ".DS_Store" \
  ! -name "*.tmp" \
  ! -name "~*" \
  2>/dev/null | sort
```
**Después del find, reportar:** "PASO 2C: {N} archivos en carpeta_fuentes"
**Comando ejecutado:** Pegar el comando find exacto con las fechas sustituidas.

**Nota:** Si la carpeta FUENTES no existe, reportar "PASO 2C: 0 archivos (carpeta no existe)" y continuar sin error.

## Consolidación PASO 2

Mostrar resumen obligatorio:
```
PASO 2A: X archivos en carpeta_anual
PASO 2B: X archivos en carpeta_evidencias
PASO 2C: X archivos en carpeta_fuentes
TOTAL:   X archivos únicos
```

**Si TOTAL == 0, DETENERSE y preguntar al usuario** antes de continuar.
