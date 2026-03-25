# Salida Esperada — resumen-reuniones

## Template por reunion (PASO 3)

```markdown
### Reunion: [Nombre/tema de la reunion]

- **Fecha y hora:** [Extraer del contenido o nombre del archivo]
- **Asistentes:** [Lista de participantes identificados]

**Resumen de la sesion:**
[Parrafo breve describiendo el proposito y desarrollo de la reunion, en primera persona + pasado]

**Puntos clave:**
1. [Punto 1]
2. [Punto 2]
...

**Acuerdos y compromisos:**
- [Acuerdo 1]
- [Acuerdo 2]
...
```

## Tabla resumen (PASO 4A)

```markdown
## Tabla Resumen

| # | Fecha | Reunion | Participantes | Temas Principales |
|---|-------|---------|---------------|-------------------|
| 1 | YYYY-MM-DD | [Nombre] | [N personas] | [Temas clave] |
| 2 | ... | ... | ... | ... |
```

## Reuniones sin transcripcion — solo calendario (PASO 4B)

```markdown
## Reuniones sin transcripcion (datos de calendario)

Las siguientes reuniones fueron identificadas en el calendario institucional pero no cuentan con transcripcion disponible:

| # | Fecha | Hora | Duracion | Reunion | Organizador | Participantes | Tipo |
|---|-------|------|----------|---------|-------------|---------------|------|
| 1 | 2026-02-05 | 10:00 | 1h | Sprint Planning | org@ent.gov.co | 5 | Virtual |
```

**Nota:** Solo incluir reuniones que no coincidan (por titulo y fecha) con las transcripciones ya procesadas en PASO 3.

## Footer del documento (PASO 4C)

```markdown
---
**Anexo:** {anexos.reuniones}
**Obligacion relacionada:** [N]
**Total reuniones en el periodo:** [N] ([M] con transcripcion, [K] solo calendario)
**Fuente calendario:** {Si/No}
```
