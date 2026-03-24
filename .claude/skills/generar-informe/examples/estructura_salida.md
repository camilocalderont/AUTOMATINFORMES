# Estructura de Salida — generar-informe

## Formato del archivo `Informe_Obligaciones_{ENTIDAD}_{mes}_{year}.md`

```markdown
# INFORME DE ACTIVIDADES - [ENTIDAD]
## Periodo: [FECHA_INICIO] a [FECHA_FIN]

---

### Obligacion 1
**[Texto completo]**

[1-3 oraciones concisas con datos concretos y tildes correctas.]

(Evidencia: [Nombre del anexo desde config.json])

---

[... repetir para todas las obligaciones ...]

---

## ANEXOS REFERENCIADOS

| Anexo | Obligaciones | Carpetas |
|-------|--------------|---------|
| Anexo 1A. Historias de Usuario Jira | 1, 6 | OBLIGACION_1/, OBLIGACION_6/ |
| Anexo 1B. Informe de commits | 1, 3, 6 | OBLIGACION_1/, OBLIGACION_3/, OBLIGACION_6/ |
| ... | ... | ... |
```
