#!/usr/bin/env python3
"""
Organiza archivos de evidencias en carpetas OBLIGACION_N/ segun un manifest JSON.

Uso:
    python3 scripts/organize_evidencias.py <manifest_json>

Input JSON:
    {
        "carpeta_evidencias": "/path/to/ANEXOS",
        "archivos": [
            {
                "ruta": "/path/to/archivo.docx",
                "obligaciones": [1, 2],
                "accion": "copy"
            },
            {
                "ruta": "/path/to/ANEXOS/archivo_local.pdf",
                "obligaciones": [4],
                "accion": "move"
            }
        ]
    }

Logica:
- accion "copy": shutil.copy2() (archivos fuera de carpeta_evidencias)
- accion "move": shutil.move() (archivos dentro de carpeta_evidencias)
- Crea carpetas OBLIGACION_N/ automaticamente
- Imprime resumen JSON a stdout
"""

import json
import os
import shutil
import sys


def organize(manifest_path):
    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    carpeta = manifest["carpeta_evidencias"]
    archivos = manifest.get("archivos", [])

    stats = {}  # obligacion -> count
    errors = []
    processed = 0

    for entry in archivos:
        ruta = entry["ruta"]
        obligaciones = entry.get("obligaciones", [])
        accion = entry.get("accion", "copy")

        if not os.path.isfile(ruta):
            errors.append({"ruta": ruta, "error": "archivo no encontrado"})
            continue

        nombre = os.path.basename(ruta)

        for i, obl in enumerate(obligaciones):
            destdir = os.path.join(carpeta, f"OBLIGACION_{obl}")
            os.makedirs(destdir, exist_ok=True)
            dest = os.path.join(destdir, nombre)

            try:
                # Move only on the last obligation to avoid losing the source
                # for subsequent copies. If only one obligation and action is
                # move, move directly.
                if accion == "move" and i == len(obligaciones) - 1:
                    shutil.move(ruta, dest)
                else:
                    shutil.copy2(ruta, dest)

                stats[obl] = stats.get(obl, 0) + 1
            except Exception as e:
                errors.append({"ruta": ruta, "obligacion": obl, "error": str(e)})

        processed += 1

    result = {
        "procesados": processed,
        "carpetas_creadas": sorted(stats.keys()),
        "archivos_por_obligacion": {str(k): v for k, v in sorted(stats.items())},
        "errores": errors,
    }

    print(json.dumps(result, ensure_ascii=False, indent=2))

    total_ops = sum(stats.values())
    n_carpetas = len(stats)
    print(
        f"\nResumen: {processed} archivos procesados, "
        f"{total_ops} copias/movimientos en {n_carpetas} carpetas OBLIGACION_N/",
        file=sys.stderr,
    )
    if errors:
        print(f"Errores: {len(errors)}", file=sys.stderr)

    return 0 if not errors else 1


def main():
    if len(sys.argv) < 2:
        print(
            "Uso: python3 scripts/organize_evidencias.py <manifest_json>",
            file=sys.stderr,
        )
        sys.exit(1)

    manifest_path = sys.argv[1]
    if not os.path.isfile(manifest_path):
        print(f"Error: manifest no encontrado: {manifest_path}", file=sys.stderr)
        sys.exit(1)

    exit_code = organize(manifest_path)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
