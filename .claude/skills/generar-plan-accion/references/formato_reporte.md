# Formato del Reporte — Plan de Accion

## Indicador institucional (SDMUJER)

| Campo | Valor |
|-------|-------|
| Objetivo estrategico | Implementar buenas practicas de gestion en la Secretaria Distrital de la Mujer |
| Indicador | Porcentaje de avance en la implementacion de la Politica de Seguridad Digital |
| Responsable | (nombre del contratista) |

## Estructura del reporte .md

```markdown
# SEGUIMIENTO PLAN DE ACCION — {MES} {AÑO}

**Objetivo estrategico:** Implementar buenas practicas de gestion en la Secretaria Distrital de la Mujer
**Indicador:** Porcentaje de avance en la implementacion de la Politica de Seguridad Digital
**Responsable:** (nombre del contratista)
**Periodo:** {fecha_inicio} a {fecha_fin}

---

## Descripcion cualitativa del avance en el mes

**[Tematica 1: titulo descriptivo].** Se realizo [actividad] mediante [accion especifica].
Se actualizo [documento] (nombre_archivo.extension - DD-MMM-YYYY) alineandolo con [marco/norma].
[Continuar describiendo actividades de esta tematica con referencias a archivos.]
Estas actividades contribuyen al cumplimiento del control ISO 27002:2022 ([numero - nombre del control]).

**[Tematica 2: titulo descriptivo].** [Descripcion con el mismo patron...]

**[Tematica N: titulo descriptivo].** [...]

---

## Retrasos y factores limitantes para el cumplimiento

[Solo si hay retrasos documentados. Si no hay, dejar la seccion vacia.]

---

## Soluciones propuestas para resolver los retrasos y factores limitantes para el cumplimiento

[Solo si hay retrasos. Si no hay, dejar la seccion vacia.]
```

## Tematicas tipicas de seguridad (SDMUJER)

Usar como guia para agrupar actividades:

1. **Actualizacion de documentacion del SGSI** — Politicas, manuales, procedimientos, SoA, listado maestro
2. **Gestion de riesgos de seguridad** — Matriz de riesgos, plan de tratamiento, analisis BIA
3. **Gestion de incidentes de seguridad** — Investigacion forense, escalamiento, alertas COLCERT
4. **Sensibilizacion y capacitacion** — Charlas, presentaciones, material de concienciacion
5. **Desarrollo seguro y Pandora** — Commits, historias de usuario, ciclo SDLC
6. **Revision de convenios y acuerdos** — Intercambio de informacion, clausulas de seguridad
7. **Atencion de requerimientos** — Tickets GLPI, solicitudes internas, entes de control
8. **Arquitectura empresarial y PETI** — Plan de seguridad, alineacion con marcos de referencia
9. **Inteligencia de amenazas** — Monitoreo, alertas, procedimientos nuevos

## Insumos consolidados

Estructura del archivo `INSUMOS_CONSOLIDADOS_{MES}_{AÑO}.txt`:

```
================================================================================
INSUMOS CONSOLIDADOS - PLAN DE ACCION {MES} {AÑO}
Fecha de generacion: {fecha_actual}
Periodo de reporte: {fecha_inicio} a {fecha_fin}
================================================================================

================================================================================
ARCHIVO 1: {nombre_archivo.extension}
Ruta: {ruta_completa}
Tipo: {PDF/DOCX/XLSX/PPTX/MD}
Fecha modificacion: {fecha}
================================================================================

{contenido_extraido_del_archivo}

================================================================================
ARCHIVO 2: {nombre_archivo.extension}
...
================================================================================

{contenido_extraido_del_archivo}

... (repetir para cada archivo)

================================================================================
FIN DEL DOCUMENTO CONSOLIDADO
Total de archivos procesados: {N}
================================================================================
```

## Controles ISO 27001:2022 / ISO 27002:2022 frecuentes

| Control | Nombre | Tematica asociada |
|---------|--------|-------------------|
| 5.1 | Politicas de seguridad de la informacion | Documentacion SGSI |
| 5.7 | Inteligencia de amenazas | Inteligencia de amenazas |
| 5.19 | Seguridad en relaciones con proveedores | Convenios |
| 5.24 | Planificacion gestion de incidentes | Gestion de incidentes |
| 5.25 | Evaluacion de eventos de seguridad | Gestion de incidentes |
| 5.26 | Respuesta a incidentes | Gestion de incidentes |
| 5.30 | Preparacion TIC para continuidad | Arquitectura/PETI |
| 6.3 | Concienciacion y capacitacion | Sensibilizacion |
| 8.8 | Gestion de vulnerabilidades tecnicas | Gestion de riesgos |
| 8.25 | Ciclo de vida de desarrollo seguro | Desarrollo Pandora |
| 8.28 | Codificacion segura | Desarrollo Pandora |
