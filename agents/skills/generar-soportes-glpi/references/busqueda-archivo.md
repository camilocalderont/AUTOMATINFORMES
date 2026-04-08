# Búsqueda de archivo GLPI (PASO 2)

Auto-localizar en 3 niveles de búsqueda:

## Nivel 1 — FUENTES (prioridad máxima)

Archivos fuente del informe con fecha hasta hoy:

```bash
find "{carpeta_fuentes}" -type f \
  -newermt "$1" -not -newermt "{dia_actual}" \
  \( -name "*glpi*.xlsx" -o -name "*glpi*.csv" -o -name "*GLPI*.xlsx" -o -name "*GLPI*.csv" -o -name "*tickets*.xlsx" -o -name "*soportes*.xlsx" \) \
  2>/dev/null
```

## Nivel 2 — carpeta_evidencias

Archivos modificados en el período:

```bash
find "{carpeta_evidencias}" -type f \
  -newermt "$1" -not -newermt "$2" \
  \( -name "*glpi*.xlsx" -o -name "*glpi*.csv" -o -name "*GLPI*.xlsx" -o -name "*GLPI*.csv" -o -name "*tickets*.xlsx" -o -name "*soportes*.xlsx" \) \
  2>/dev/null
```

## Nivel 3 — carpeta_anual (fallback)

Excluyendo INFORMES/:

```bash
find "{carpeta_anual}" -type f \
  -newermt "$1" -not -newermt "$2" \
  -not -path "*/INFORMES/*" \
  \( -name "*glpi*.xlsx" -o -name "*glpi*.csv" -o -name "*GLPI*.xlsx" -o -name "*GLPI*.csv" -o -name "*tickets*.xlsx" -o -name "*soportes*.xlsx" \) \
  2>/dev/null
```

## Reglas

- Usar el primer nivel que devuelva resultados
- La carpeta FUENTES/ es donde el usuario deja los exports de GLPI para el informe, y se busca con `{dia_actual}` como límite porque se generan después del período
- Si se encuentra más de un archivo, usar el más reciente
