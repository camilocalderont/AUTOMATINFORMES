---
name: redaccion-español
description: >
  Enforce de ortografía correcta en español para todo texto generado por el sistema.
  Garantiza tildes obligatorias en verbos, sustantivos y términos técnicos.
  Prohíbe calificativos subjetivos, inventar actividades y omitir citación de evidencias.
type: rule
scope: always
severity: required
metadata:
  author: solercia
  version: "1.0.0"
  category: documentation
  tags: [ortografía, español, tildes, redacción]
---

# Ortografía y redacción en español

## Tildes obligatorias

**Verbos en pasado (pretérito):** realizó, implementó, validó, configuró, desarrolló, ejecutó, gestionó, atendió, resolvió, diseñó, corrigió, ajustó, actualizó, verificó, documentó, coordinó, participó, presentó, revisó, efectuó, brindó, elaboró, identificó, integró, optimizó, generó, registró, procesó, adelantó, estableció

**Sustantivos y términos técnicos:** gestión, atención, módulo, período, aplicación, configuración, implementación, documentación, información, resolución, integración, solución, ejecución, administración, planeación, contratación, evaluación, coordinación, operación, función, versión, descripción, migración, validación, corrección, comunicación

**Palabras comunes:** también, además, según, través (a través), técnico/a, específico/a, único/a, último/a, número, código, método, automático/a, electrónico/a, página, teléfono, próximo/a, día, más, así, aquí

## Prohibiciones

- **No mayúsculas sostenidas** en texto redactado (excepto siglas: GLPI, UAECD, IDARTES, etc.)
- **No omitir tildes** — cada palabra de las listas anteriores DEBE llevar tilde siempre
- **No calificativos subjetivos**: Evitar "gran esfuerzo", "significativo avance", "atención oportuna", "importante contribución"
- **No inventar actividades**: Solo redactar sobre actividades con evidencia documentada

## Obligaciones de citación

- Citar evidencia específica al final de cada justificación de obligación
- Si no hay actividad para una obligación, indicar explícitamente: "Durante el período reportado no se adelantaron actividades relacionadas con esta obligación."
- Las evidencias DEBEN corresponder al período reportado
- Para reuniones con compromisos, incluir evidencia (acta, correo o captura)

## Alcance

Aplica a TODO texto generado: informes de obligaciones, evidencias, commits, reuniones, soportes, log de ejecución, correos.

**Incluye scripts Python** — los strings visibles en documentos Word/Excel generados por scripts en `scripts/` (labels de tablas, encabezados, footers, mensajes) DEBEN tener tildes correctas. Ejemplos:
- ❌ `"Reunion"` → ✅ `"Reunión"`
- ❌ `"Descripcion"` → ✅ `"Descripción"`
- ❌ `"Periodo"` → ✅ `"Período"`
- ❌ `"sesion"` → ✅ `"sesión"`
- ❌ `"transcripcion"` → ✅ `"transcripción"`
- ❌ `"Estadisticas"` → ✅ `"Estadísticas"`
- ❌ `"Categoria"` → ✅ `"Categoría"`
- ❌ `"Solucion"` → ✅ `"Solución"`
- ❌ `"automaticamente"` → ✅ `"automáticamente"`
- ❌ `"Titulo"` → ✅ `"Título"`

**Idioma del documento:** Los documentos Word generados DEBEN configurar el idioma a `es-CO` (español Colombia) para que Word no marque las palabras con tilde como errores ortográficos.
