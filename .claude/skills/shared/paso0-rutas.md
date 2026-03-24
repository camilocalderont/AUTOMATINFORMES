# PASO 0: Resolucion de rutas (compartido por todos los skills)

Este bloque es identico para los 11 skills del proyecto. Cada skill DEBE ejecutar estos pasos al inicio.

## Pasos

1. Extraer ano de $1 → `{year}`
2. Extraer mes de $1 → mapear a `{month_name}`:
   01→"01. ENERO", 02→"02. FEBRERO", 03→"03. MARZO", 04→"04. ABRIL",
   05→"05. MAYO", 06→"06. JUNIO", 07→"07. JULIO", 08→"08. AGOSTO",
   09→"09. SEPTIEMBRE", 10→"10. OCTUBRE", 11→"11. NOVIEMBRE", 12→"12. DICIEMBRE"
3. Extraer nombre del mes en minusculas → `{mes}` (enero, febrero, ..., diciembre)
4. Leer `entidades/$0/config.json`
5. Resolver `{carpeta_anual}` reemplazando `{year}` en `rutas.carpeta_anual`
6. Resolver `{carpeta_mes}` reemplazando `{carpeta_anual}` y `{month_name}` en `rutas.carpeta_mes`
7. Resolver `{carpeta_evidencias}` reemplazando `{carpeta_mes}` en `rutas.carpeta_evidencias`
8. Resolver `{carpeta_fuentes}` reemplazando `{carpeta_mes}` en `rutas.carpeta_fuentes`
9. Resolver `{carpeta_reuniones}` reemplazando `{carpeta_fuentes}` en `rutas.carpeta_reuniones` (si aplica)
10. Definir `{entidad_lower}` = $0 en minusculas (idt, idartes, sdmujer, uaecd)

## Verificacion de carpetas

- `ls -d "{carpeta_evidencias}" 2>/dev/null`
- **Si NO existe** → Buscar desde `{carpeta_mes}`: `find "{carpeta_mes}" -type d -maxdepth 3 2>/dev/null | sort`
- Si no hay candidato → **detener ejecucion** y preguntar al usuario con AskUserQuestion
- Si existe → `mkdir -p "{carpeta_evidencias}"` (asegurar que exista)

## Variables adicionales (segun skill)

| Variable | Comando | Usado por |
|----------|---------|-----------|
| `{dia_actual}` | `date +%Y-%m-%d` | generar-informe, generar-soportes-*, resumen-reuniones |
| `{dia_siguiente}` | `date -v+1d +%Y-%m-%d` | buscar-evidencias |
| `{log_file}` | `{carpeta_mes}/log_{entidad_lower}_{mes}_{year}.md` | generar-informe |
