---
name: no-inventar-contenido
description: >
  Prohíbe fabricar contenido de correos, documentos o evidencias que no hayan sido leídos directamente.
  Aplica especialmente a la generación de archivos Word con correos y a las justificaciones de obligaciones.
type: rule
scope: always
severity: critical
metadata:
  author: solercia
  version: "1.0.0"
  category: integrity
  tags: [correos, evidencias, integridad, no-inventar]
---

# Prohibición de invención de contenido

## Regla principal

**NUNCA** redactar el cuerpo de un correo, documento o evidencia sin haberlo leído directamente de la fuente (PDF, archivo .md, MCP, o exportación de Outlook).

## Correos electrónicos

1. **Solo transcribir contenido real**: El cuerpo de un correo en un archivo Word DEBE provenir de:
   - Lectura del PDF exportado de Outlook (vía MCP `read_document` o `pandoc`)
   - Lectura del archivo `.md` que contiene el borrador/copia del correo
   - Contenido proporcionado textualmente por el usuario

2. **Si el PDF es ilegible** (artefactos de OCR, caracteres duplicados):
   - Intentar conversión con `pandoc` a `.md`
   - Validar si el `.md` resultante es legible (texto coherente, no caracteres basura)
   - Si es legible → usar el contenido extraído
   - Si NO es legible → **REPORTAR al usuario**: "El PDF de correos no se pudo convertir de forma legible. Se requiere exportar los correos nuevamente desde Outlook."
   - **NUNCA** inventar o parafrasear el contenido del correo

3. **Campos permitidos sin lectura directa**: Solo se pueden inferir:
   - `de:` (si se conoce la cuenta del config.json)
   - `fecha:` (si se conoce del nombre del archivo o metadatos)
   - **NUNCA** inferir `para:`, `cc:`, `asunto:` ni `cuerpo:`

## Justificaciones de obligaciones

1. **Solo afirmar lo que tiene evidencia**: Cada oración en la justificación de una obligación DEBE tener un archivo correspondiente en OBLIGACION_N/
2. **No atribuir acciones que no se realizaron**: Si en un hilo de correo el usuario solo estaba en copia (CC), NO decir "Envié" ni "Respondí" — decir "Participé en la coordinación" o similar
3. **Si no hay evidencia para una obligación**: Indicar explícitamente "Durante el período reportado no se adelantaron actividades relacionadas con esta obligación."

## Incidentes de referencia

- Sesión SDMUJER marzo 2026: Se fabricó contenido del correo COLCERT (el usuario solo respondió "OK gracias"), del correo ANS (era de Jorge Escalante, no del usuario), y detalles técnicos inventados sobre medidas de seguridad electoral
- El usuario tuvo que corregir manualmente y el archivo generado no correspondía a la realidad

## Prelación de fuentes

1. **Archivo .md con borrador/copia** del correo → fuente más confiable
2. **PDF exportado de Outlook** → requiere validación de legibilidad
3. **Información verbal del usuario** → aceptable si el usuario la proporciona explícitamente
4. **Inferencia o parafraseo** → **PROHIBIDO**
