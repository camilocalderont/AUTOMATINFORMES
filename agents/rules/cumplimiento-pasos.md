---
name: cumplimiento-pasos
description: >
  Enforce de ejecución completa de todos los pasos numerados en skills.
  Cada PASO es obligatorio sin importar presión de contexto o tamaño de
  conversación. Prohíbe saltar, resumir o inferir pasos. Exige reportar
  resultado antes de avanzar al siguiente paso.
type: rule
scope: path-scoped
paths:
  - "**/*.md"
severity: required
metadata:
  author: solercia
  version: "1.0.0"
  category: architecture
  tags: [skills, pasos, cumplimiento, obligatorio]
---

# Cumplimiento obligatorio de pasos

## Regla principal

Cada PASO numerado en un skill es **OBLIGATORIO**. No existen pasos opcionales a menos que el skill lo indique explícitamente con una condición (ej: "Solo si tiene api.jira").

## Prohibiciones

1. **NUNCA saltar un paso** por presión de contexto, tamaño de la conversación, o porque "ya se tiene suficiente información"
2. **NUNCA sustituir un comando Bash** por inferencia, conocimiento previo o lectura de directorio — si el skill dice "ejecutar via Bash", ejecutar literalmente
3. **NUNCA resumir o abreviar** la ejecución de un paso — ejecutar completo con todos sus sub-pasos
4. **NUNCA avanzar al siguiente paso** sin reportar el resultado del paso actual (conteo, archivos generados, éxito/error)

## Validaciones obligatorias

- **buscar-evidencias PASO 2**: Verificar que los 3 `find` se ejecutaron (2A, 2B, 2C). El log DEBE mostrar el conteo de cada uno
- **generar-informe PASO 3**: Verificar que buscar-evidencias completó los 3 finds. Si solo muestra archivos de FUENTES, repetir
- **generar-informe PASO 10**: Es tan obligatorio como PASO 1. Crear TODAS las carpetas OBLIGACION_N/ y copiar TODOS los entregables
- **generar-informe PASO 11**: Siempre guardar informe final + finalizar log. NUNCA terminar antes

## PASO 10 y PASO 11 no son opcionales

Los últimos pasos de un skill se saltan con frecuencia cuando el contexto está lleno. PASO 10 (organizar anexos) y PASO 11 (guardar informe) son entregables finales — sin ellos, la ejecución está incompleta.

## Incidentes de referencia

- **PASO 2A saltado** (2026-03-04): buscar-evidencias para UAECD omitió el find principal, dejando 32 archivos sin encontrar
- **PASO 6 saltado** (2026-03-09): 200+ archivos consumieron el contexto y la IA saltó la organización en OBLIGACION_N/
- **PASO 10 parcial** (múltiples sesiones): La IA hacía solo algunas carpetas OBLIGACION_N/ en vez de todas
