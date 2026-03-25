# Formatos de Log para generar-informe

Cada PASO del orquestador debe registrar su resultado en `{log_file}`. Los formatos a continuación son plantillas — reemplazar los valores entre `{}` con datos reales de la ejecución.

**REGLA OBLIGATORIA:** Todo comando Bash ejecutado durante el informe DEBE quedar registrado en el log con:
1. El comando exacto (con valores sustituidos, no variables)
2. El resultado (número de archivos, output resumido, o "0 resultados")
3. Si hubo error o retry, documentar ambos intentos

---

## PASO 0: Resolución de rutas

```markdown
## PASO 0: Resolución de rutas

### Rutas resueltas:
- carpeta_anual: `{valor}`
- carpeta_mes: `{valor}`
- carpeta_evidencias: `{valor}`
- carpeta_fuentes: `{valor}`
- carpeta_reuniones: `{valor}`
```

---

## PASO 0B: Estructura de carpetas

```markdown
## PASO 0B: Estructura de carpetas

### Comandos ejecutados:
\```bash
mkdir -p "{carpeta_evidencias}"
mkdir -p "{carpeta_fuentes}/TRANSCRIPCIONES"
\```

### Estado: {Creada nueva|Subcarpetas agregadas|Existente usada}
### Archivos previos en FUENTE/: {lista o "ninguno"}
```

---

## PASO 2: Extraer insumos via API

```markdown
## PASO 2: Extraer insumos via API

### PASO 2A - Mesa de servicios ({mesa_servicios.tipo}):
- API configurada: {Si/No}
- Comando: `{comando ejecutado o "SALTADO — motivo"}`
- Resultado: {Exitoso - N registros | Fallido - motivo | Saltado}
- Archivo: {ruta del archivo generado o N/A}

### PASO 2B - Gestion de proyectos ({gestion_proyectos.tipo}):
- Ejecutado como: {Subagente background | Saltado}
- Comando: `{python3 scripts/jira_extract.py ... o "SALTADO"}`
- Resultado: {Exitoso - N issues | Saltado}
- Archivo: {ruta o N/A}

### PASO 2C - Correo suplementario:
- Aplica: {Si/No}
- Ejecutado como: {Subagente background | Saltado}
- Resultado: {Exitoso - N correos | Saltado}
- Archivo: {ruta o N/A}

### PASO 2D - Calendario:
- API configurada: {Si/No}, Tipo: {google/outlook}
- Comando: `{skill ejecutado o "SALTADO — motivo"}`
- Resultado: {Exitoso - N reuniones | Fallido - motivo | Saltado}
- Archivo: {ruta o N/A}

### PASO 2E - Resumen de reuniones:
- Transcripciones encontradas: {N}
- Reuniones calendario: {M}
- Resultado: {Exitoso - N reuniones procesadas | Sin transcripciones}
- Archivos: {rutas .md y .docx}
```

---

## PASO 3: buscar-evidencias

```markdown
## PASO 3: buscar-evidencias

### PASO 2 PRE — Calentar cache OneDrive:
\```bash
for dir in "{carpeta_anual}"/*/; do ls "$dir" >/dev/null 2>&1; done
\```

### PASO 2A — Comando find carpeta_anual:
\```bash
find "{carpeta_anual}" -type f -newermt "{$1}" ! -newermt "{$2}" ! -name ".DS_Store" ! -name "*.tmp" ! -name "~*" ! -path "*/node_modules/*" ! -path "*/.git/*" ! -path "*/INFORMES/*" 2>/dev/null | sort
\```
- Resultado: {N} archivos
- Retry: {Si/No — motivo si aplica}

### PASO 2B — Comando find carpeta_evidencias:
\```bash
find "{carpeta_evidencias}" -type f -newermt "{$1}" ! -newermt "{$2}" ! -name ".DS_Store" ! -name "*.tmp" ! -name "~*" ! -path "*/node_modules/*" ! -path "*/.git/*" 2>/dev/null | sort
\```
- Resultado: {N} archivos

### PASO 2C — Comando find carpeta_fuentes:
\```bash
find "{carpeta_fuentes}" -type f -newermt "{$1}" ! -newermt "{dia_siguiente}" ! -name ".DS_Store" ! -name "*.tmp" ! -name "~*" 2>/dev/null | sort
\```
- Resultado: {N} archivos

### Consolidación:
- PASO 2A: {X} archivos en carpeta_anual
- PASO 2B: {X} archivos en carpeta_evidencias
- PASO 2C: {X} archivos en carpeta_fuentes
- TOTAL: {X} archivos únicos

### Archivos relevantes filtrados: {N} (tras excluir ruido: .opencode/, ACTUALES/, scripts/, etc.)
### PASO 6 organize_evidencias: {N} archivos copiados a {M} carpetas OBLIGACION_N/
### Archivo: `{carpeta_evidencias}/evidencias_{entidad}_{mes}.md`
```

---

## PASO 4: generar-commits

```markdown
## PASO 4: generar-commits

### Auto-descubrimiento de repositorios:
\```bash
find "{git.ruta_proyecto}" -maxdepth 2 -name ".git" -type d 2>/dev/null | sort
\```
- Repositorios encontrados: {lista}

### Comando git log ejecutado (por cada repo con resultados):
\```bash
cd "{repo_dir}" && GIT_PAGER=cat git log --author="{author_filter}" --since="{$1}" --until="{$2}" --branches='{rama_principal}*' --branches='{patron}' --format="{repo_name}|%H|%h|%ad|%s|%D" --date=format:"%Y-%m-%d %H:%M"
\```

### Resultado:
- {repo_name}: {N} commits
- Total: {N} commits

### Generación Word:
\```bash
python3 scripts/commits_to_docx.py "{json_path}" "{docx_path}"
\```
- Resultado: {Exitoso | Fallido}

### Archivos: `{carpeta_evidencias}/commits_{entidad}_{mes}.md`, `{carpeta_fuentes}/commits_{entidad}_{mes}.docx`
```

---

## PASO 5: generar-soportes

```markdown
## PASO 5: generar-soportes-{correo|glpi}

### Tipo de mesa: {mesa_servicios.tipo}
### Fuente usada: {API previa (PASO 2) | Archivo local | Sin archivo encontrado}

### Comando de búsqueda de archivo (si aplica):
\```bash
find "{carpeta_fuentes}" -type f -newermt "{$1}" ! -newermt "{dia_actual}" \( -name "*glpi*.xlsx" -o -name "*glpi*.csv" \) 2>/dev/null
\```
- Archivo encontrado: {ruta y tamaño}

### Comando de lectura:
\```bash
python3 -c "import openpyxl; wb = openpyxl.load_workbook('{ruta}'); ..."
\```
(o MCP read_document si aplica)

### Resultado: {N} tickets procesados
### Generación Excel (si aplica):
\```bash
python3 scripts/glpi_to_excel.py "{json_path}" "{xlsx_path}"
\```

### Archivo: `{carpeta_evidencias}/soportes_{tipo}_{entidad}_{mes}.md`
```

---

## PASO 6: generar-plan-accion (condicional)

```markdown
## PASO 6: Plan de Acción

### Aplica: {Si — fuente_key "plan_accion" en config | No — saltado}
### Modo: {sub-skill (evidencias existía) | standalone}

### Comandos ejecutados:
\```bash
pandoc /tmp/md_to_docx_temp.md -o "{docx_path}" --from markdown --to docx --wrap=none
cp "{docx_path}" "{carpeta_fuentes}/plan_accion_{entidad}_{mes}.docx"
cp "{carpeta_fuentes}/plan_accion_{entidad}_{mes}.docx" "{carpeta_evidencias}/OBLIGACION_{N}/{nombre_anexo}.docx"
\```

### Archivos: `{carpeta_planes}/{MES}_{year}.md`, `{carpeta_planes}/{MES}_{year}.docx`
### Copia: `{carpeta_fuentes}/plan_accion_{entidad}_{mes}.docx`
### Copiado a: {OBLIGACION_N/ lista}
```

---

## PASO 10: Organización de anexos en OBLIGACION_N/

```markdown
## PASO 10: Organización de anexos en carpetas OBLIGACION_N/

### Carpeta base: {carpeta_evidencias}/

### Comandos ejecutados:
\```bash
mkdir -p "{carpeta_evidencias}/OBLIGACION_{N}/"
cp -n "{fuente}" "{carpeta_evidencias}/OBLIGACION_{N}/{nombre_anexo}{ext}"
\```

| Anexo | Archivo Fuente | Destino |
|-------|---------------|---------|
| {nombre_anexo} | {archivo_fuente} | OBLIGACION_{N1}/, OBLIGACION_{N2}/ |
| ... | ... | ... |

### Archivos no encontrados:
{lista o "Ninguno"}

### Resumen carpetas:
- OBLIGACION_1/: {N} archivos ({M} evidencias + {K} anexos)
- OBLIGACION_2/: ...
- ...
```

---

## PASO 11: Informe generado (cierre del log)

```markdown
## PASO 11: Informe generado

### Archivos .md generados:
- {lista completa de .md en carpeta_evidencias}

### Archivos entregables generados (en {carpeta_fuentes}):
- {lista de .docx/.xlsx}

### Anexos organizados en carpetas:
{resumen de carpetas OBLIGACION_N/ con conteo}

### Obligaciones con actividad: {N} de {total}
### Total evidencias documentales: {N} archivos únicos
### Fin de ejecución: {fecha/hora}
```
