# Salida Esperada — extraer-reuniones-calendario

## Formato del archivo `reuniones_calendario_{entidad_lower}_{mes}.md`

```markdown
# Reuniones del Calendario - $0
## Periodo: $1 a $2

### Resumen
Durante el periodo se identificaron [N] reuniones en el calendario institucional.

### Estadisticas
- Total reuniones: [N]
- Reuniones virtuales: [N]
- Reuniones presenciales: [N]
- Horas estimadas en reuniones: [N]h

### Tabla de Reuniones

| # | Fecha | Hora | Duracion | Reunion | Organizador | Participantes | Tipo | Transcripcion |
|---|-------|------|----------|---------|-------------|---------------|------|---------------|
| 1 | 2026-02-05 | 10:00 | 1h | Sprint Planning | org@ent.gov.co | 5 | Virtual | Si (archivo.md) |
| 2 | 2026-02-07 | 14:00 | 30m | Seguimiento GLPI | org@ent.gov.co | 3 | Virtual | No |

---

**Anexo:** {anexos.reuniones}
**Obligacion relacionada:** [N]
**Total reuniones en el periodo:** [N]
**Reuniones con transcripcion:** [N] de [N]
```
