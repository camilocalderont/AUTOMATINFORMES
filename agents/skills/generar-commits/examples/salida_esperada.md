# Salida Esperada — generar-commits

## Ejemplo concreto de comando (IDT)

```bash
for gitdir in $(find "{ruta_proyecto}" -maxdepth 2 -name ".git" -type d 2>/dev/null | sort); do
  repo_dir=$(dirname "$gitdir")
  repo_name=$(basename "$repo_dir")
  (cd "$repo_dir" && \
   GIT_PAGER=cat git log \
     --author="correo1@entidad.gov.co\|correo2@entidad.gov.co\|correo.personal@gmail.com" \
     --since="2026-01-16" --until="2026-01-31" \
     --branches='masterIDT_proxy*' \
     --branches='IDT*' \
     --branches='idt_*' \
     --format="$repo_name|%H|%h|%ad|%s|%D" \
     --date=format:"%Y-%m-%d %H:%M" \
     2>/dev/null)
done
```

## Formato del archivo `commits_{entidad_lower}_{mes}.md`

```markdown
## Descripcion General

Durante el periodo reportado realice actividades de desarrollo en el sistema Pandora,
abarcando los repositorios pandora_proxy y apiadministrador con un total de 12 commits.

Los cambios se centraron en el modulo de contratacion, donde implemente mejoras en
la generacion de informes de pago, y en el modulo de administracion, donde corregi
validaciones de formularios.

## Desarrollos Semana a Semana

### Semana 1 (01/01 - 07/01)
Estado: Finalizado
Fecha Inicio: 01/01/2026
Fecha Fin: 07/01/2026
Funcionalidades:
- Implementacion de logging en peticiones al servicio ORFEO para trazabilidad de integracion
- Actualizacion de rutas de URL en el modulo de contratacion para compatibilidad con nuevo servidor

### Semana 2 (08/01 - 14/01)
Estado: Finalizado
Fecha Inicio: 08/01/2026
Fecha Fin: 14/01/2026
Funcionalidades:
- Correccion de validacion de fechas en formularios de pago
- Ajuste en consultas SQL del modulo de reportes para optimizacion de rendimiento

## Tabla Completa de Commits

| # | Commit ID | Repositorio | Rama | Descripcion | Fecha |
|---|-----------|-------------|------|-------------|-------|
| 1 | 68abaf52 | pandora_proxy | GLPI-45148 | Implementacion de logging en peticiones a ORFEO | 02/01/2026 |
| 2 | a1b2c3d4 | pandora_proxy | master_proxy | Actualizacion de rutas de URL | 05/01/2026 |
```
