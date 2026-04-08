# PASO 12: Verificar coherencia informe vs evidencias

Ejecutar el skill de verificación como paso final:

```
/verificar-informe {$0} {$1} {$2}
```

Este skill (con modelo opus) lee cada archivo en OBLIGACION_N/, valida que:
- Cada anexo mencionado en el informe existe como archivo
- Cada archivo en las carpetas está referenciado en el informe
- El contenido de cada archivo corresponde al período reportado
- No hay duplicados de formato (PDF > Word > MD)
- Las afirmaciones numéricas (N commits, N tickets, N reuniones) coinciden con la evidencia

Si hay FAIL → corregir antes de dar por terminado.
Si hay WARNING → reportar al usuario para decisión.

**Registrar en log** el resultado del verificador.
