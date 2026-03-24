#!/usr/bin/env python3
"""
Extrae issues de Jira Cloud via REST API directa.
Usa /rest/api/3/search/jql (endpoint actual, no el deprecado /search).

Uso:
    python3 scripts/jira_extract.py ENTIDAD FECHA_INICIO FECHA_FIN OUTPUT_MD [--output-xlsx PATH]

Ejemplo:
    python3 scripts/jira_extract.py IDARTES 2026-02-01 2026-02-28 output.md --output-xlsx output.xlsx

Requiere en .env:
    JIRA_IDARTES_EMAIL=...
    JIRA_IDARTES_API_TOKEN=...
"""

import sys
import os
import json
import urllib.request
import urllib.parse
import urllib.error
import base64
from datetime import datetime


def load_env(env_path=".env"):
    """Carga variables desde .env sin dependencias externas."""
    if not os.path.exists(env_path):
        return
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            if key not in os.environ or not os.environ[key]:
                os.environ[key] = value


def load_config(entidad):
    """Carga config.json de la entidad."""
    config_path = os.path.join("entidades", entidad, "config.json")
    if not os.path.exists(config_path):
        print(f"Error: No se encontro {config_path}", file=sys.stderr)
        sys.exit(1)
    with open(config_path) as f:
        return json.load(f)


def jira_request(url, email, token):
    """Hace request autenticado a Jira Cloud."""
    auth = base64.b64encode(f"{email}:{token}".encode()).decode()
    req = urllib.request.Request(url)
    req.add_header("Authorization", f"Basic {auth}")
    req.add_header("Accept", "application/json")
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode() if e.fp else ""
        print(f"Error HTTP {e.code}: {body}", file=sys.stderr)
        sys.exit(1)


def search_issues(base_url, email, token, jql, fields):
    """Busca issues usando /rest/api/3/search/jql (endpoint actual)."""
    params = urllib.parse.urlencode({
        "jql": jql,
        "fields": fields,
        "maxResults": 100,
    })
    url = f"{base_url}/rest/api/3/search/jql?{params}"
    data = jira_request(url, email, token)
    return data.get("issues", [])


def format_date(iso_date):
    """Formatea fecha ISO a YYYY-MM-DD."""
    if not iso_date:
        return "N/A"
    return iso_date[:10]


def main():
    if len(sys.argv) < 5:
        print("Uso: python3 jira_extract.py ENTIDAD FECHA_INICIO FECHA_FIN OUTPUT_MD [--output-xlsx PATH]")
        sys.exit(1)

    entidad = sys.argv[1].upper()
    fecha_inicio = sys.argv[2]
    fecha_fin = sys.argv[3]
    output_md = sys.argv[4]

    output_xlsx = None
    if "--output-xlsx" in sys.argv:
        idx = sys.argv.index("--output-xlsx")
        if idx + 1 < len(sys.argv):
            output_xlsx = sys.argv[idx + 1]

    # Cargar .env y config
    load_env()
    config = load_config(entidad)

    jira_config = config.get("api", {}).get("jira")
    if not jira_config:
        print(f"Error: {entidad} no tiene api.jira configurado", file=sys.stderr)
        sys.exit(1)

    # Credenciales
    email_env = jira_config.get("email_env", f"JIRA_{entidad}_EMAIL")
    token_env = jira_config.get("token_env", f"JIRA_{entidad}_API_TOKEN")
    email = os.environ.get(email_env, "")
    token = os.environ.get(token_env, "")

    if not email or not token:
        print(f"Error: Variables {email_env} y/o {token_env} no configuradas en .env", file=sys.stderr)
        sys.exit(1)

    base_url = config.get("gestion_proyectos", {}).get("url", "")
    if not base_url:
        url_env = jira_config.get("url_env", f"JIRA_{entidad}_URL")
        base_url = os.environ.get(url_env, "")
    base_url = base_url.rstrip("/")

    # Construir JQL
    proyecto = jira_config.get("proyecto", "CP")
    account_id = jira_config.get("account_id", "")

    if account_id:
        jql = (f"project = {proyecto} AND assignee = {account_id} "
               f"AND statusCategory = Done "
               f"AND resolved >= '{fecha_inicio}' AND resolved <= '{fecha_fin}' "
               f"ORDER BY resolved DESC")
    else:
        jql = (f"project = {proyecto} AND assignee = currentUser() "
               f"AND statusCategory = Done "
               f"AND resolved >= '{fecha_inicio}' AND resolved <= '{fecha_fin}' "
               f"ORDER BY resolved DESC")

    print(f"JQL: {jql}")
    print(f"URL: {base_url}")

    # Buscar issues
    fields = "summary,status,issuetype,reporter,priority,created,updated,resolutiondate,project"
    issues = search_issues(base_url, email, token, jql, fields)

    print(f"Issues encontradas: {len(issues)}")

    # Procesar issues
    processed = []
    for issue in issues:
        f = issue.get("fields", {})
        processed.append({
            "key": issue.get("key", ""),
            "tipo": f.get("issuetype", {}).get("name", ""),
            "resumen": f.get("summary", ""),
            "estado": f.get("status", {}).get("name", ""),
            "estado_categoria": f.get("status", {}).get("statusCategory", {}).get("name", ""),
            "informador": f.get("reporter", {}).get("displayName", ""),
            "prioridad": f.get("priority", {}).get("name", ""),
            "fecha_creacion": format_date(f.get("created", "")),
            "fecha_actualizacion": format_date(f.get("updated", "")),
            "fecha_resolucion": format_date(f.get("resolutiondate", "")),
            "espacio": f.get("project", {}).get("name", ""),
        })

    # Estadisticas (solo issues finalizados)
    total = len(processed)

    por_tipo = {}
    for i in processed:
        por_tipo[i["tipo"]] = por_tipo.get(i["tipo"], 0) + 1

    # Generar Markdown
    mes_nombre = datetime.strptime(fecha_inicio, "%Y-%m-%d").strftime("%B").upper()
    lines = []
    lines.append(f"# Issues Jira Finalizados - {entidad}")
    lines.append(f"## Periodo: {fecha_inicio} a {fecha_fin}")
    lines.append(f"## Proyecto: {proyecto} ({processed[0]['espacio'] if processed else 'N/A'})")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Resumen General")
    lines.append("")
    lines.append(f"Durante el periodo reportado se finalizaron {total} issues en Jira, "
                 f"distribuidas en {', '.join(f'{v} {k}' for k, v in por_tipo.items())}.")
    lines.append("")
    lines.append("### Estadisticas")
    lines.append(f"- **Total issues finalizados:** {total}")
    for tipo, count in por_tipo.items():
        lines.append(f"- **{tipo}:** {count}")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Tabla de Issues Finalizados")
    lines.append("")
    lines.append("| # | Key | Tipo | Resumen | Estado | Informador | Creada | Resuelta | Prioridad |")
    lines.append("|---|-----|------|---------|--------|------------|--------|----------|-----------|")
    for idx, i in enumerate(processed, 1):
        resumen_corto = i["resumen"][:80] + ("..." if len(i["resumen"]) > 80 else "")
        lines.append(f"| {idx} | {i['key']} | {i['tipo']} | {resumen_corto} | {i['estado']} | {i['informador']} | {i['fecha_creacion']} | {i['fecha_resolucion']} | {i['prioridad']} |")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Detalle por issue
    lines.append("## Detalle de Issues Finalizados")
    lines.append("")
    for i in processed:
        lines.append(f"### {i['key']}: {i['resumen']}")
        lines.append(f"- **Tipo:** {i['tipo']}")
        lines.append(f"- **Estado:** {i['estado']}")
        lines.append(f"- **Prioridad:** {i['prioridad']}")
        lines.append(f"- **Informador:** {i['informador']}")
        lines.append(f"- **Creada:** {i['fecha_creacion']}")
        lines.append(f"- **Resuelta:** {i['fecha_resolucion']}")
        lines.append(f"- **Proyecto:** {i['espacio']}")
        lines.append("")

    md_content = "\n".join(lines)

    # Guardar MD
    os.makedirs(os.path.dirname(output_md) or ".", exist_ok=True)
    with open(output_md, "w", encoding="utf-8") as f:
        f.write(md_content)
    print(f"MD generado: {output_md}")

    # Generar JSON para jira_to_excel.py si se pide xlsx
    if output_xlsx:
        json_data = {
            "entidad": entidad,
            "periodo_inicio": fecha_inicio,
            "periodo_fin": fecha_fin,
            "total": total,
            "issues": [
                {
                    "key": i["key"],
                    "tipo": i["tipo"],
                    "resumen": i["resumen"],
                    "estado": i["estado"],
                    "story_points": None,
                    "sprint": None,
                    "fecha_creacion": i["fecha_creacion"],
                    "fecha_resolucion": i["fecha_resolucion"],
                    "fecha_actualizacion": i["fecha_actualizacion"],
                    "prioridad": i["prioridad"],
                    "informador": i["informador"],
                    "espacio": i["espacio"],
                }
                for i in processed
            ],
        }
        json_path = output_xlsx.replace(".xlsx", "_data.json")
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(json_data, f, ensure_ascii=False, indent=2)

        # Intentar generar Excel
        script_dir = os.path.dirname(os.path.abspath(__file__))
        excel_script = os.path.join(script_dir, "jira_to_excel.py")
        if os.path.exists(excel_script):
            ret = os.system(f'python3 "{excel_script}" "{json_path}" "{output_xlsx}"')
            if ret == 0:
                os.remove(json_path)
                print(f"Excel generado: {output_xlsx}")
            else:
                print(f"Error generando Excel (exit {ret}), JSON conservado: {json_path}", file=sys.stderr)
        else:
            print(f"Script {excel_script} no encontrado, JSON conservado: {json_path}", file=sys.stderr)


if __name__ == "__main__":
    main()
