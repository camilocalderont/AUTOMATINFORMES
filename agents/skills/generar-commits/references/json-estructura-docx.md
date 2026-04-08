# Estructura JSON para commits_to_docx.py

El JSON intermedio debe seguir esta estructura exacta:

```json
{
    "entidad": "{$0}",
    "periodo_inicio": "{$1}",
    "periodo_fin": "{$2}",
    "total_commits": N,
    "repositorios": ["repo1", "repo2"],
    "descripcion": "Texto de la sección A del PASO 2...",
    "semanas": [
        {
            "nombre": "Semana 1 (dd/mm - dd/mm)",
            "estado": "Finalizado",
            "fecha_inicio": "dd/mm/aaaa",
            "fecha_fin": "dd/mm/aaaa",
            "funcionalidades": ["func1", "func2"]
        }
    ],
    "commits": [
        {
            "hash": "8chars",
            "fecha": "YYYY-MM-DD",
            "mensaje": "mensaje del commit",
            "rama": "nombre_rama",
            "repositorio": "nombre_repo"
        }
    ]
}
```

## Campos

| Campo | Descripción |
|-------|-------------|
| `entidad` | Nombre de la entidad (IDARTES, IDT, etc.) |
| `periodo_inicio` / `periodo_fin` | Fechas del período en formato YYYY-MM-DD |
| `total_commits` | Número total de commits encontrados |
| `repositorios` | Lista de nombres de repositorios con actividad |
| `descripcion` | Texto de la Descripción General (sección A del PASO 2) |
| `semanas[]` | Array con una entrada por cada semana con commits |
| `commits[]` | Array con todos los commits individuales |
