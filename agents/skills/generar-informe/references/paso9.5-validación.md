# PASO 9.5: Validar correos y evidencias complementarias

**Antes de organizar anexos, validar las fuentes de correo.**

## A) Validar PDF de correos (si existe)

Si hay un PDF de correos en `{carpeta_fuentes}` (ej: `correos.pdf`):

1. Intentar convertir a Markdown con pandoc:
```bash
pandoc "{carpeta_fuentes}/correos.pdf" -o "/tmp/correos_validacion.md" --from pdf --to markdown 2>/dev/null
```

2. Leer las primeras 100 líneas del .md resultante y evaluar legibilidad:
   - **Legible:** Texto coherente, se pueden extraer De/Para/Asunto/Fecha → usar como fuente
   - **Ilegible:** Caracteres duplicados (ej: "CCCCrrrriiiissssttttiiiiaaaannnn"), texto basura → **REPORTAR al usuario**: "El PDF de correos no se pudo convertir de forma legible. Se requiere exportar los correos nuevamente desde Outlook en formato legible."

3. **REGLA CRÍTICA (rule `no-inventar-contenido`):** NUNCA fabricar el cuerpo de un correo. Solo transcribir contenido leído directamente de archivos .md o PDFs legibles.

## B) Verificar evidencias complementarias por obligación

Para cada obligación que mencione reuniones, correos o documentos específicos:
- Hay transcripción formateada? Si no → generar con el skill de reuniones
- Hay Word de correos? Si no → verificar si existen archivos .md con borradores de correo en la carpeta anual
- El documento específico mencionado (ej: GT-MA-3 V5) está en la carpeta? Si no → buscarlo y copiarlo
