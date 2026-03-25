---
name: estilo-informes
description: >
  Enforce del estilo de redacción en primera persona y pretérito (pasado) para
  informes de obligaciones contractuales. Fuente: Memorando SDMUJER 3-2026-000375.
  Aplica a todas las entidades (IDARTES, SDMUJER, IDT, UAECD).
type: rule
scope: path-scoped
paths:
  - "**/*.md"
severity: required
metadata:
  author: solercia
  version: "1.0.0"
  category: documentation
  tags: [redacción, informes, primera-persona, obligaciones]
---

# Estilo de redacción para informes

## Regla principal

Toda redacción de informes de obligaciones DEBE usar **primera persona + pretérito (pasado)**.

## Ejemplos correctos

- "Realicé la implementación del módulo de planeación"
- "Atendí 15 solicitudes de soporte técnico"
- "Desarrollé el componente de validación de formularios"
- "Participé en 6 reuniones de seguimiento del proyecto"
- "Resolví 10 tickets de mesa de servicios"

## Ejemplos INCORRECTOS (estilo deprecado)

- ~~"Se realizó la implementación"~~ (tercera persona impersonal)
- ~~"Se implementó el módulo"~~ (voz pasiva refleja)
- ~~"Se validó la configuración"~~ (impersonal)
- ~~"El contratista realizó"~~ (tercera persona)

## Estructura por obligación

```
### Obligación [N]
**[Texto completo de la obligación]**

[1-3 oraciones directas en primera persona + pasado, con datos concretos.]

(Evidencia: [Nombre del anexo])
```

## Excepciones

- **Plan de Acción TI** (SDMUJER): Usa tercera persona impersonal ("Se realizó", "Se gestionó") porque es un reporte institucional, no personal.

## Fuente

Memorando SDMUJER 3-2026-000375 — aplicado como lineamiento general para todas las entidades por decisión del usuario.
