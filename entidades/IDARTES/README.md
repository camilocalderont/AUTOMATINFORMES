# IDARTES - Instituto Distrital de las Artes

## OBJETO DEL CONTRATO

Prestar servicios profesionales al Instituto Distrital de las Artes - Oficina Asesora de Planeacion y Tecnologias de la informacion OAPTI, en actividades asociadas al desarrollo de los sistemas de informacion institucional, con enfasis en la aplicacion de estandares de calidad y criterios de seguridad de la informacion para su optimo funcionamiento, de acuerdo con las indicaciones dadas por la dependencia.

---

## OBLIGACIONES CONTRACTUALES

| # | Obligacion | Skill Aplicable | Tipo de Evidencia |
|---|------------|-----------------|-------------------|
| 1 | Desarrollar mejoras y optimizacion de funcionalidades de los sistemas de informacion de la entidad, aplicando estandares de calidad en el desarrollo, acorde con las apuestas establecidas en el PETI, y siguiendo los lineamientos de la dependencia. | `/generar-commits` | Commits, Historias de Usuario |
| 2 | Realizar el soporte tecnico de acuerdo con la asignacion realizada por la mesa de servicios de la entidad, propendiendo por el optimo funcionamiento de los sistemas de informacion y en estricto cumplimiento de los ANS, siguiendo la indicacion de la dependencia. | `/generar-soportes-glpi` | Tickets GLPI |
| 3 | Aportar en la disminucion de brechas de seguridad de los sistemas de informacion de la entidad a traves de la aplicacion de buenas practicas en el desarrollo velando por la proteccion de datos y la continuidad de negocio, acorde con los lineamientos de la dependencia. | `/generar-commits` | Commits (seguridad) |
| 4 | Formular e implementar un plan de trabajo en torno a la transferencia de conocimiento de buenas practicas para el desarrollo de software que involucre niveles de trabajo tecnico y funcional, aportando a la eficiencia de los procesos de la entidad, acorde con los lineamientos de la dependencia. | Manual | Documentos, Capacitaciones |
| 5 | Realizar cesion de los acuerdos de licenciamiento, propiedad de los codigos fuente y los derechos de propiedad intelectual asociados con el contenido de los aplicativos entregados al IDARTES. | N/A | Clausula contractual |
| 6 | Desarrollar y hacer seguimiento a la aplicacion de estandares de calidad en el desarrollo y aplicacion de codigos de los sistemas de informacion de la entidad, que asegurar su optimo funcionamiento escalabilidad y mantenimiento, acorde con las indicaciones de la dependencia. | `/generar-commits` | Commits (refactorizacion), Casos de Prueba |
| 7 | Aportar en la definicion de procedimientos y documentacion asociada al desarrollo de software con el objetivo de documentar las buenas practicas en el desarrollo de los sistemas de informacion, acorde con la estructura del Sistema Integrado de Gestion, y atendiendo las indicaciones de la dependencia. | Manual | Documentos SIG |
| 8 | Construir y remitir en oportunidad los reportes de cumplimiento de actividades incluidas dentro de los distintos instrumentos de planeacion de la OAPTI, acorde con los lineamientos de la dependencia. | N/A | Este informe + SECOP |
| 9 | Asistir a las actividades y reuniones a las cuales sea convocado por la dependencia. | Manual | Transcripciones/Resumenes |

---

## MAPEO DE COMMITS A OBLIGACIONES

| Tipo de Commit | Obligacion |
|----------------|------------|
| Nuevas funciones, mejoras, correcciones de logica | 1 |
| Mencion explicita de seguridad, vulnerabilidad, XSS, SQL injection | 3 |
| Refactorizacion, estandares, patrones, formato de codigo | 6 |

---

## ANEXOS ESTANDAR

| Anexo | Contenido | Obligaciones |
|-------|-----------|--------------|
| Anexo 1A | Historias de Usuario Jira (.xlsx/.csv) | 1, 6 |
| Anexo 1B | Informe de commits (.docx/.md) | 1, 3, 6 |
| Anexo 2A | Soportes GLPI (.xlsx/.csv) | 2 |
| Anexo 8A | Informe Pago Pandora mes anterior (.pdf) | 8 |
| Anexo 8B | Reporte SECOP II mes anterior (.pdf) | 8 |
| Anexo 9A | Resumen de Reuniones (.docx) | 9 |

---

## RUTAS DE EVIDENCIAS

```
CARPETA_ANUAL: (ver config.json → rutas.carpeta_anual)
CARPETA_EVIDENCIAS: {CARPETA_ANUAL}/INFORMES/{MES}/FUENTE
```
