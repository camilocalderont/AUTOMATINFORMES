# Comandos git log — Doble Pasada

## Pasada A: Por ramas (filtro existente)

```bash
for gitdir in $(find "{ruta_proyecto}" -maxdepth 2 -name ".git" -type d 2>/dev/null | sort); do
  repo_dir=$(dirname "$gitdir")
  repo_name=$(basename "$repo_dir")
  (cd "$repo_dir" && \
   GIT_PAGER=cat git log \
     --author="{author_filter}" \
     --since="$1" --until="$2" \
     {branch_filters} \
     --format="$repo_name|%H|%h|%ad|%s|%D" \
     --date=format:"%Y-%m-%d %H:%M" \
     2>/dev/null)
done
```

## Pasada B: Por mensaje del commit (filtro nuevo)

Si `git.patrones_mensaje` existe en config.json:

```bash
for gitdir in $(find "{ruta_proyecto}" -maxdepth 2 -name ".git" -type d 2>/dev/null | sort); do
  repo_dir=$(dirname "$gitdir")
  repo_name=$(basename "$repo_dir")
  (cd "$repo_dir" && \
   GIT_PAGER=cat git log \
     --author="{author_filter}" \
     --since="$1" --until="$2" \
     --all \
     --grep="{message_filters}" \
     --format="$repo_name|%H|%h|%ad|%s|%D" \
     --date=format:"%Y-%m-%d %H:%M" \
     2>/dev/null)
done
```

## Combinar y deduplicar

Unir la salida de ambas pasadas, eliminar líneas duplicadas por hash completo (campo 2), y ordenar por fecha:

```bash
(pasada_a; pasada_b) | sort -t'|' -k2 -u | sort -t'|' -k4 -r
```

## Notas

- La Pasada B captura commits que están en ramas con nombre diferente al patrón (ej: rama `masterSdMujer` no coincide con patrón `*SDMujer*`, pero el mensaje `feat(sdmujer):` sí coincide con el patrón de mensaje).
- Filtrar stash commits: Excluir líneas donde el mensaje (campo 5) empiece con `WIP on ` o `index on `.
- **Formato de salida:** `repo_name|hash_completo|hash_corto|fecha|mensaje|decoraciones`
- Cada línea es un commit. Si no hay output, no hubo commits en el período para esa entidad.
