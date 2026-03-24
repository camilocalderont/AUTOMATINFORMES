# UAECD - Unidad Administrativa Especial de Catastro Distrital

## OBJETO DEL CONTRATO

Prestacion de servicios profesionales para el mantenimiento (evolutivo y correctivo), adaptacion y desarrollo de nuevas funcionalidades y soporte tecnico para la optima operacion del sistema PANDORA de acuerdo con los requerimientos y necesidades de la UAECD.

---

## OBLIGACIONES CONTRACTUALES

| # | Obligacion | Skill Aplicable | Tipo de Evidencia |
|---|------------|-----------------|-------------------|
| 1 | Aplicar el ciclo de vida completo de desarrollo de software (SDLC) en todas las intervenciones del sistema PANDORA, garantizando la ejecucion de las fases de analisis de requerimientos, diseno tecnico, desarrollo, pruebas funcionales y documentacion, bajo estandares de calidad, seguridad y siguiendo las buenas practicas de ingenieria de software establecidas por la Gerencia de Tecnologia de la UAECD. | `/generar-commits`, `/buscar-evidencias` | Commits, Documentos tecnicos |
| 2 | Disenar y ejecutar estrategias tecnicas para la evolucion de la arquitectura del sistema PANDORA, orientadas a la modernizacion tecnologica (transicion de monolitos modulares a microservicios), aplicando patrones de diseno, principios SOLID, arquitectura limpia y estandares de codificacion que garanticen la escalabilidad, mantenibilidad y sostenibilidad del sistema. | `/generar-commits` | Commits (refactoring, patrones), Documentos arquitectura |
| 3 | Realizar el mantenimiento evolutivo y correctivo del sistema PANDORA mediante el analisis, diseno, desarrollo e implementacion de nuevas funcionalidades, mejoras en los modulos existentes, y la atencion de incidencias, errores y fallas reportadas, aplicando metodologias agiles y asegurando la integracion continua con los componentes del sistema. | `/generar-commits` | Commits (features, fixes) |
| 4 | Brindar orientacion tecnica especializada y soporte a usuarios funcionales y equipos internos en la definicion, solucion de requerimientos operativos y atencion de solicitudes, evaluando la viabilidad tecnica, resolviendo incidencias de manera efectiva y asegurando que las propuestas se alineen con la arquitectura objetivo, estandares institucionales y buenas practicas de desarrollo. | `/generar-soportes-correo` | Correos soporte |
| 5 | Elaborar y mantener actualizada la documentacion tecnica del sistema, incluyendo arquitectura de software, diagramas de componentes, modelos de datos, decisiones de diseno, protocolos de integracion, manuales tecnicos y guias de desarrollo, facilitando la transferencia de conocimiento y garantizando la trazabilidad del sistema. | `/buscar-evidencias` | Documentos tecnicos (.docx, .xlsx) |
| 6 | Monitorear la calidad, rendimiento y seguridad del sistema PANDORA mediante la revision de indicadores tecnicos (performance, disponibilidad, errores), analisis de logs, aplicacion de practicas de code review y analisis estatico de codigo, proponiendo acciones preventivas y correctivas que mantengan la estabilidad y eficiencia operativa. | `/generar-commits` | Commits (validaciones, fixes), Informes de monitoreo |
| 7 | Las demas actividades asignadas dentro del ambito tecnico del contrato, en concordancia con el objeto contractual y los lineamientos institucionales establecidos por la UAECD. | Manual | Varios |

---

## MAPEO DE COMMITS A OBLIGACIONES

| Tipo de Commit | Obligacion |
|----------------|------------|
| Analisis, diseno, desarrollo, pruebas, documentacion | 1 |
| Refactorizacion, desacoplamiento, patrones SOLID, arquitectura limpia | 2 |
| Nuevas funcionalidades, mejoras, correccion de errores | 3 |
| Validaciones, manejo de errores, code review, analisis de codigo | 6 |
| Migraciones de BD (CREATE/ALTER TABLE) | 1, 3 |

---

## ANEXOS ESTANDAR

| Anexo | Contenido | Obligaciones |
|-------|-----------|--------------|
| Anexo 1A | Documento SDLC / desarrollo (.docx) | 1 |
| Anexo 2A | Documento arquitectura (.docx) | 2 |
| Anexo 3A | Informe desarrollo y mantenimiento (.docx) | 3 |
| Anexo 5A | Documentacion tecnica (.docx) | 5 |
| correos_soporte.pdf | Correos soporte Outlook | 4 |
| correos_generales.pdf | Correos generales | 4, 7 |

---

## RUTAS DE EVIDENCIAS

```
CORREO: Outlook institucional UAECD
CARPETA_ANUAL: (ver config.json → rutas.carpeta_anual)
CARPETA_EVIDENCIAS: (ver config.json → rutas.carpeta_evidencias)
```

---

## NOTA ESPECIAL

Este contrato tiene enfasis en:
1. **SDLC Completo:** Obligacion 1 (ciclo de vida de desarrollo)
2. **Arquitectura:** Obligacion 2 (transicion a microservicios, patrones SOLID)
3. **Desarrollo:** Obligaciones 1, 3 (mantenimiento evolutivo y correctivo)
4. **Soporte:** Obligacion 4 (orientacion tecnica y atencion de solicitudes)
5. **Documentacion:** Obligacion 5 (documentacion tecnica actualizada)
6. **Calidad:** Obligacion 6 (monitoreo, code review, analisis estatico)
