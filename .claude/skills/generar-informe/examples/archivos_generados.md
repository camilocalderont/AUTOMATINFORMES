# Archivos Generados por generar-informe

## Archivos .md (procesamiento AI)

| Archivo | Ubicacion |
|---------|-----------|
| `evidencias_{entidad}_{mes}.md` | `{carpeta_evidencias}/` |
| `commits_{entidad}_{mes}.md` | `{carpeta_evidencias}/` |
| `soportes_glpi_{entidad}_{mes}.md` o `soportes_correo_{entidad}_{mes}.md` | `{carpeta_evidencias}/` |
| `tickets_glpi_api_{entidad}_{mes}.md` (GLPI via API) | `{carpeta_evidencias}/` |
| `correos_api_{entidad}_{mes}.md` (correo via API) | `{carpeta_evidencias}/` |
| `jira_issues_{entidad}_{mes}.md` (solo IDARTES) | `{carpeta_evidencias}/` |
| `reuniones_calendario_{entidad}_{mes}.md` (calendario API) | `{carpeta_evidencias}/` |
| `reuniones_{entidad}_{mes}.md` | `{carpeta_evidencias}/` |
| `Informe_Obligaciones_{$0}_{mes}_{year}.md` | `{carpeta_evidencias}/../` (carpeta_mes) |
| `log_{entidad_lower}_{mes}_{year}.md` | `{carpeta_evidencias}/../` (carpeta_mes) |

## Archivos entregables (evidencia formal en {carpeta_fuentes})

| Archivo | Tipo | Fuente |
|---------|------|--------|
| `commits_{entidad}_{mes}.docx` | Word | Commits git |
| `correos_soporte_{entidad}_{mes}.docx` | Word | Correos Gmail/Outlook |
| `glpi_{entidad}_{mes}.xlsx` | Excel | Tickets GLPI |
| `jira_{entidad}_{mes}.xlsx` | Excel | Issues Jira |
| `reuniones_{entidad}_{mes}.docx` | Word | Transcripciones + calendario |

## Carpetas de obligaciones

Derivadas de `config.json["anexos"]`. Cada anexo se copia a las carpetas `OBLIGACION_N/` segun su array `obligaciones`.

**Resultado esperado en disco (ejemplo IDARTES):**
```
{carpeta_mes}/
├── ANEXOS/                                    ← {carpeta_evidencias}
│   ├── OBLIGACION_1/
│   │   ├── Anexo 1A. Historias de Usuario Jira.xlsx
│   │   └── Anexo 1B. Informe de commits.docx
│   ├── OBLIGACION_2/
│   │   ├── Anexo 2A. Soportes GLPI.xlsx
│   │   └── Anexo 2B. Correos de Soporte.docx
│   ├── OBLIGACION_3/
│   │   └── Anexo 1B. Informe de commits.docx
│   ├── OBLIGACION_6/
│   │   ├── Anexo 1A. Historias de Usuario Jira.xlsx
│   │   └── Anexo 1B. Informe de commits.docx
│   ├── OBLIGACION_9/
│   │   └── Anexo 9A. Resumen de Reuniones.docx
│   ├── commits_idartes_febrero.md
│   ├── evidencias_idartes_febrero.md
│   ├── soportes_glpi_idartes_febrero.md
│   └── ...
├── FUENTE/                                    ← {carpeta_fuentes}
│   ├── TRANSCRIPCIONES/                       ← {carpeta_reuniones}
│   │   └── transcripcion_reunion_X.md
│   ├── commits_idartes_febrero.docx
│   ├── jira_idartes_febrero.xlsx
│   ├── glpi_idartes_febrero.xlsx
│   ├── correos_soporte_idartes_febrero.docx
│   └── reuniones_idartes_febrero.docx
├── Informe_Obligaciones_IDARTES_febrero_2026.md
└── log_idartes_febrero_2026.md
```
