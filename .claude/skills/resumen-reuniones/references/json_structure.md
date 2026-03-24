# Estructura JSON — reuniones_to_docx.py

Archivo intermedio: `{carpeta_fuentes}/_reuniones_data_{entidad_lower}_{mes}.json`

```json
{
    "entidad": "{$0}",
    "periodo_inicio": "{$1}",
    "periodo_fin": "{$2}",
    "total_reuniones": N,
    "con_transcripcion": M,
    "solo_calendario": K,
    "reuniones": [
        {
            "nombre": "Sprint Planning",
            "fecha": "2026-02-05",
            "hora": "10:00",
            "asistentes": ["persona1@ent.gov.co"],
            "resumen": "Se planificaron tareas...",
            "puntos_clave": ["Punto 1"],
            "acuerdos": ["Acuerdo 1"],
            "tiene_transcripcion": true
        }
    ],
    "tabla_resumen": [
        {
            "num": 1,
            "fecha": "2026-02-05",
            "nombre": "Sprint Planning",
            "participantes": "5 personas",
            "temas": "Planificacion sprint 10"
        }
    ]
}
```

Escribir el JSON usando la herramienta Write.
