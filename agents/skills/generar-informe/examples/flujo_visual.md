# Flujo Visual de generar-informe

```
/generar-informe $0 $1 $2
    │
    ├── PASO 0: Resolver rutas → {carpeta_evidencias}, {carpeta_fuentes}
    ├── PASO 0B: Verificar/crear estructura de carpetas
    ├── PASO 1: Cargar config.json + README.md
    │
    ├── PASO 2: Extraer insumos via API + generar entregables
    │   ├── 2A: /extraer-tickets-glpi O subagente Gmail/Outlook
    │   │       → .md + .xlsx/.docx
    │   ├── 2B: Subagente Jira (background) ──┐
    │   │       → .md + .xlsx                  │ paralelo
    │   ├── 2C: Subagente Gmail (background) ──┘
    │   │       → .md + .docx
    │   ├── 2D: /extraer-reuniones-calendario (esperar)
    │   │       → .md (datos calendario)
    │   └── 2E: /resumen-reuniones (esperar)
    │           → .md + .docx
    │   [Esperar agentes background 2B, 2C]
    │
    ├── PASO 3: /buscar-evidencias $0 $1 $2
    │   └── → evidencias_{entidad}_{mes}.md
    │   └── (encuentra PDF/Excel/DOCX generados en PASO 2)
    │
    ├── PASO 4: /generar-commits $0 $1 $2
    │   └── → commits_{entidad}_{mes}.md + .docx
    │
    ├── PASO 5: /generar-soportes-{correo|glpi} $0 $1 $2
    │   └── → soportes_{tipo}_{entidad}_{mes}.md
    │   └── (detecta extraccion API previa del PASO 2)
    │
    ├── PASO 7: Consolidar inventario
    ├── PASO 8: Mapear a obligaciones
    ├── PASO 9: Redactar justificacion
    │
    ├── PASO 10: Organizar anexos en carpetas OBLIGACION_N/
    │   └── {carpeta_evidencias}/OBLIGACION_1/, OBLIGACION_2/, ...
    │
    └── PASO 11: Guardar informe + log
        ├── → Informe_Obligaciones_{$0}_{mes}_{year}.md
        └── → log_{entidad_lower}_{mes}_{year}.md
```

## Ejemplo de ejecucion para IDT

```
/generar-informe IDT 2026-01-16 2026-01-31
```

Ejecuta secuencialmente:
1. PASO 0B: Verificar/crear carpeta del periodo
2. PASO 2A: Extraer correos via Gmail API (subagente) → .md + .docx
3. PASO 2D: Extraer reuniones calendario → .md
4. PASO 2E: /resumen-reuniones → .md + .docx
5. PASO 3: /buscar-evidencias (encuentra .docx generados)
6. PASO 4: /generar-commits → .md + .docx
7. PASO 5: /generar-soportes-correo (detecta API previa)
8. PASO 10: Organizar anexos en carpetas numeradas
9. PASO 11: Guardar informe
