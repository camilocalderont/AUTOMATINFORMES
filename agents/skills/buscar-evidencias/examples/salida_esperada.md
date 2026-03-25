# Salida Esperada — buscar-evidencias

## Formato del archivo `evidencias_{entidad_lower}_{mes}.md`

```markdown
# Evidencias del Periodo - $0
## $1 a $2

### Archivos Encontrados: [N] archivos

---

## 1. [nombre_archivo.docx]
- **Fecha:** YYYY-MM-DD HH:MM
- **Tipo:** Documento Word
- **Ubicacion:** [ruta relativa]
- **Resumen:** [Descripcion del contenido]
- **Obligaciones relacionadas:** [1, 6, 7]
- **Copiado a:** OBLIGACION_1/, OBLIGACION_6/

---

## 2. [nombre_archivo.xlsx]
...

---

## Archivos No Leidos (errores)
| Archivo | Error |
|---------|-------|
| archivo.zip | Formato no soportado |

---

## Carpetas Creadas
| Carpeta | Archivos |
|---------|----------|
| OBLIGACION_1/ | documento_requisitos.docx, transcripcion.md |
| OBLIGACION_3/ | casos_prueba.xlsx |

---

## Resumen por Obligacion

| Obligacion | Archivos Relacionados |
|------------|----------------------|
| 1 | archivo1.docx, archivo2.pdf |
| 2 | archivo3.xlsx |
| ... | ... |
```

## Estructura de carpetas resultante

```
{carpeta_evidencias}
├── evidencias_idt_enero.md          ← Inventario generado
├── OBLIGACION_1/                    ← Archivos para obligacion 1
│   ├── documento_requisitos.docx
│   └── transcripcion_reunion.md
├── OBLIGACION_3/                    ← Solo si hay archivos
│   └── casos_prueba.xlsx
└── (archivos pre-existentes no se tocan)
```
