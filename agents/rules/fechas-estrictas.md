---
name: fechas-estrictas
description: >
  Prohíbe modificar, ampliar o inventar rangos de fechas en búsquedas de archivos.
  Si un find retorna 0 resultados, reportar 0 y continuar — NUNCA inventar
  rangos alternativos. El usuario prefiere precisión de fechas sobre completitud.
type: rule
scope: path-scoped
paths:
  - "**/*.md"
severity: required
metadata:
  author: solercia
  version: "1.0.0"
  category: security
  tags: [fechas, find, búsqueda, precisión]
---

# Regla crítica de fechas

## NUNCA modificar rangos de fecha

Cuando se ejecutan comandos `find` con parámetros de fecha (`-newermt`):

1. **Usar las fechas exactas** proporcionadas por el usuario ($1 y $2)
2. **Si un find retorna 0 archivos**, reportar 0 y continuar al siguiente paso
3. **NUNCA** ampliar, ajustar ni inventar rangos alternativos
4. **NUNCA** cambiar `-newermt "$1"` por una fecha anterior "para capturar más archivos"
5. **NUNCA** cambiar `! -newermt "$2"` por una fecha posterior

## Por qué

Los timestamps de OneDrive/Google Drive pueden no coincidir con las fechas reales de creación de los archivos. Esto es un hecho documentado que el usuario conoce. El usuario **prefiere precisión de fechas sobre completitud** — es mejor reportar 0 archivos que incluir archivos de un período incorrecto.

## Incidente de referencia

En febrero 2026, la IA amplió el rango de fechas cuando find retornó 0, trayendo archivos de marzo al informe de febrero (memorando_INFORMES.pdf del 3/03, Santi_informeActividades del 5/03). Estos archivos no pertenecían al período y contaminaron el informe.
