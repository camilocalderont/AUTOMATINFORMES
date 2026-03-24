# SDMUJER - Secretaria Distrital de la Mujer

## CPS No.836 DE 2026

## OBJETO DEL CONTRATO

Prestar los servicios profesionales a la Oficina Asesora de Planeación en la implementación, mantenimiento y sostenibilidad de soluciones de información innovadoras, así como, en el fortalecimiento de la seguridad de la información, acorde con los lineamientos de la Política de Gobierno Digital y de la Política de Seguridad Digital.

---

## OBLIGACIONES CONTRACTUALES

| # | Obligación | Skill Aplicable | Tipo de Evidencia |
|---|------------|-----------------|-------------------|
| 1 | Apoyar las etapas de planificación, análisis, diseño, desarrollo, pruebas, implementación y mantenimiento de los aplicativos y sistemas de información de acuerdo con los proyectos planteados en materia de tecnología. | `/generar-commits` | Commits, Documentos |
| 2 | Apoyar la formulación y actualización de la política de seguridad de la información, Plan de Tratamiento de Riesgos de Seguridad, Plan de Seguridad y Privacidad de la Información en concordancia con los lineamientos y requerimientos de las entidades competentes y los de la Entidad, en materia de seguridad. | Manual | Documentos SGSI |
| 3 | Gestionar la implementación del modelo de seguridad y privacidad de la información (MSPI) y el sistema de gestión de continuidad del negocio (SGCN). | Manual | Documentos MSPI |
| 4 | Atender de forma correcta y oportuna los requerimientos internos, de la ciudadanía, entes de control y demás entidades reguladoras en materia de TI, relacionadas con los temas de Gobierno Digital y Seguridad Digital. | `/generar-soportes-glpi` | Tickets GLPI, Correos |
| 5 | Apoyar a la Oficina Asesora de Planeación en la documentación del ciclo de vida de desarrollo de software seguro en la Entidad y acciones para su apropiación. | `/generar-commits` | Commits, Documentos |
| 6 | Apoyar en el lineamiento e implementación de la actualización de los activos de información en conjunto con los enlaces definidos en cada dependencia de la Entidad. | Manual | Matriz Activos |
| 7 | Acompañar requerimientos de Arquitectura Empresarial y la ejecución del PETI relacionados con seguridad de la información. | Manual | Documentos PETI |
| 8 | Apoyar la supervisión de los contratos, mediante el seguimiento administrativo, la revisión de documentos, el control de plazos y la elaboración de los soportes necesarios para la adecuada ejecución contractual. | Manual | Documentos Supervisión |
| 9 | Las demás actividades que, en el marco del objeto contractual, sean requeridas por el supervisor del contrato y guarden relación directa con la naturaleza del mismo. | Manual | Varios |

---

## MAPEO DE COMMITS A OBLIGACIONES

| Tipo de Commit | Obligación |
|----------------|------------|
| Desarrollo de funcionalidades Pandora | 1 |
| Documentación de desarrollo seguro | 1, 5 |
| Cualquier commit en ramas SDMUJER | 1 |

---

## ANEXOS ESTANDAR

| Anexo | Contenido | Obligaciones |
|-------|-----------|--------------|
| Anexo 1A | Informe de commits (.docx) | 1, 5 |
| Anexo 4A | Correos enviados periodo (.docx) | 4, 9 |
| Anexo 4B | Soportes GLPI (.xlsx) | 4 |
| Plan de Acción | Reporte seguimiento Plan TI (.docx) | 2, 3 |
| Anexo 9A | Resumen de Reuniones (.docx) | 9 |

---

## RUTAS DE EVIDENCIAS

```
CARPETA_ANUAL: (ver config.json → rutas.carpeta_anual)
CARPETA_EVIDENCIAS: {CARPETA_ANUAL}/PLANES/{MES}
```

---

## NOTA ESPECIAL

Este contrato tiene un componente dual:
1. **Desarrollo Pandora:** Obligaciones 1, 5 (desarrollo de aplicativos y documentación ciclo de vida)
2. **OSI (Oficial de Seguridad):** Obligaciones 2, 3, 4, 6, 7
3. **Supervisión contractual:** Obligación 8
4. **General:** Obligación 9

El reporte de Plan de Acción TI es un insumo adicional que se genera con el skill específico de SDMUJER.
