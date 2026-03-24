"""
PANDORA Mail Agent - CLI Principal

Uso:
    python main.py --mailbox pandora test-connection
    python main.py --mailbox personal read --days 30
    python main.py --mailbox pandora stats --days 30
    python main.py --mailbox pandora classify --days 7
    python main.py --mailbox pandora bot --interval 300
"""

import sys
import time
from datetime import datetime, timedelta, timezone

import click
from rich.console import Console

from config import config, MAILBOX_PROFILES
from connectors import create_connector

console = Console()


@click.group()
@click.option(
    "--mailbox", "-m",
    type=click.Choice(list(MAILBOX_PROFILES.keys()), case_sensitive=False),
    default=None,
    help="Buzón a usar: pandora o personal",
)
def cli(mailbox: str | None):
    """PANDORA Mail Agent - Automatización de correo corporativo."""
    if mailbox:
        config.mailbox = mailbox


@cli.command("test-connection")
def test_connection():
    """Prueba la conexión al correo."""
    profile = config.active_profile
    console.print(f"\nBuzón: [bold]{config.mailbox}[/] ({profile['description']})")
    console.print(f"Método: [bold]{config.connection_method}[/]")

    connector = create_connector(config)
    if connector.connect():
        console.print("[green]Conexión exitosa![/]")

        # Probar lectura de 3 correos recientes
        emails = connector.fetch_emails(limit=3)
        if emails:
            console.print(f"\nÚltimos {len(emails)} correos:")
            for e in emails:
                console.print(
                    f"   {e.date:%Y-%m-%d %H:%M} | {e.sender_name} | {e.subject[:60]}"
                )
        else:
            console.print("Sin correos disponibles (puede ser normal si no hay exports)")

        connector.disconnect()
    else:
        console.print("[red]No se pudo conectar[/]")
        sys.exit(1)


@cli.command("test-smtp")
@click.option("--to", "to_email", default="", help="Correo destino para prueba")
def test_smtp(to_email: str):
    """Prueba el envío SMTP (sin enviar correo real a menos que uses --to)."""
    from connectors.smtp_connector import SmtpConnector

    console.print("\nProbando SMTP...")
    smtp = SmtpConnector(
        host=config.smtp_host,
        port=config.smtp_port,
        email=config.smtp_email,
        password=config.smtp_password,
    )

    if smtp.connect():
        console.print("[green]SMTP funcional![/]")
        console.print(f"   Host: {config.smtp_host}:{config.smtp_port}")
        console.print(f"   Email: {config.smtp_email}")

        if to_email:
            success = smtp.send_email(
                to=to_email,
                subject="[TEST] PANDORA Mail Agent - Prueba SMTP",
                body_html="<p>Este es un correo de prueba del Mail Agent.</p>",
            )
            if success:
                console.print(f"[green]Correo de prueba enviado a {to_email}[/]")
        else:
            console.print("   Usa --to correo@ejemplo.com para enviar un correo de prueba")

        smtp.disconnect()
    else:
        console.print("[red]SMTP no funciona[/]")
        sys.exit(1)


@cli.command("read")
@click.option("--days", default=30, help="Días hacia atrás a consultar")
@click.option("--folder", default="INBOX", help="Carpeta de correo")
@click.option("--limit", default=100, help="Máximo de correos")
def read_emails(days: int, folder: str, limit: int):
    """Lee correos de un período determinado."""
    since = datetime.now(timezone.utc) - timedelta(days=days)

    connector = create_connector(config)
    if not connector.connect():
        sys.exit(1)

    console.print(f"\nLeyendo correos de los últimos {days} días...")
    emails = connector.fetch_emails(folder=folder, since=since, limit=limit)

    console.print(f"   Encontrados: {len(emails)} correos\n")

    for e in emails:
        read_mark = "[dim]leído[/]" if e.is_read else "[bold]NUEVO[/]"
        attach = "[cyan]adj[/]" if e.has_attachments else "   "
        console.print(
            f" {read_mark} {attach} {e.date:%Y-%m-%d %H:%M} | "
            f"[bold]{e.sender_name[:25]:25s}[/] | {e.subject[:55]}"
        )

    connector.disconnect()


@cli.command("stats")
@click.option("--days", default=30, help="Días hacia atrás")
@click.option("--export-csv", is_flag=True, help="Exportar a CSV")
def generate_stats(days: int, export_csv: bool):
    """Genera estadísticas de soporte para informes de pago."""
    from analyzers.support_stats import SupportAnalyzer

    since = datetime.now(timezone.utc) - timedelta(days=days)
    until = datetime.now(timezone.utc)

    connector = create_connector(config)
    if not connector.connect():
        sys.exit(1)

    console.print(f"\nGenerando estadísticas ({days} días)...")

    # Leer inbox y enviados
    console.print("   Leyendo bandeja de entrada...")
    inbox = connector.fetch_emails(folder="INBOX", since=since, limit=500)
    console.print(f"   -> {len(inbox)} recibidos")

    console.print("   Leyendo correos enviados...")
    sent = connector.fetch_sent_emails(since=since, limit=500)
    console.print(f"   -> {len(sent)} enviados")

    # Analizar
    analyzer = SupportAnalyzer(config.user_email)
    stats = analyzer.analyze(inbox, sent, since, until)

    # Mostrar reporte
    analyzer.print_report(stats)

    # Exportar si se pidió
    if export_csv:
        dfs = analyzer.to_dataframe(stats)
        for name, df in dfs.items():
            filename = f"stats_{name}_{since:%Y%m%d}_{until:%Y%m%d}.csv"
            df.to_csv(filename, index=False)
            console.print(f"   Exportado: {filename}")

    connector.disconnect()


@cli.command("classify")
@click.option("--days", default=7, help="Días hacia atrás")
@click.option("--unread-only", is_flag=True, help="Solo correos no leídos")
def classify_emails(days: int, unread_only: bool):
    """Clasifica correos para el bot de respuesta."""
    from analyzers.classifier import EmailClassifier

    since = datetime.now(timezone.utc) - timedelta(days=days)

    connector = create_connector(config)
    if not connector.connect():
        sys.exit(1)

    console.print(f"\nClasificando correos ({days} días)...\n")

    emails = connector.fetch_emails(since=since, limit=100)

    if unread_only:
        emails = [e for e in emails if not e.is_read]

    classifier = EmailClassifier()
    results = classifier.classify_batch(emails)

    for email_msg, classification in results:
        classifier.print_classification(email_msg, classification)

    # Resumen
    from collections import Counter
    cat_counts = Counter(c.category.value for _, c in results)
    auto_count = sum(1 for _, c in results if c.auto_respondable)

    console.print(f"\n[bold]Resumen de clasificación:[/]")
    for cat, count in cat_counts.most_common():
        console.print(f"   {cat}: {count}")
    console.print(f"\n   Auto-respondables: {auto_count} / {len(results)}")

    connector.disconnect()


@cli.command("bot")
@click.option("--interval", default=300, help="Segundos entre revisiones")
@click.option("--auto", "full_auto", is_flag=True, help="Modo full automático")
def run_bot(interval: int, full_auto: bool):
    """Ejecuta el bot de respuesta automática en modo continuo."""
    from analyzers.classifier import EmailClassifier
    from responders.auto_responder import AutoResponder

    connector = create_connector(config)
    if not connector.connect():
        sys.exit(1)

    classifier = EmailClassifier()
    responder = AutoResponder(connector, full_auto=full_auto)

    mode = "[red]FULL AUTO[/]" if full_auto else "[green]SEMI-AUTO[/]"
    console.print(f"\nBot iniciado en modo {mode}")
    console.print(f"   Revisando cada {interval} segundos")
    console.print("   Presiona Ctrl+C para detener\n")

    processed_ids = set()

    try:
        while True:
            # Leer correos no leídos recientes
            since = datetime.now(timezone.utc) - timedelta(hours=24)
            emails = connector.fetch_emails(since=since, limit=50)

            # Filtrar ya procesados
            new_emails = [
                e for e in emails if e.id not in processed_ids and not e.is_read
            ]

            if new_emails:
                console.print(
                    f"\n[bold]{len(new_emails)} correo(s) nuevo(s) "
                    f"({datetime.now():%H:%M:%S})[/]"
                )

                classified = classifier.classify_batch(new_emails)
                responder.process_batch(classified)

                for e in new_emails:
                    processed_ids.add(e.id)
            else:
                console.print(
                    f"[dim]   Sin correos nuevos ({datetime.now():%H:%M:%S})[/]"
                )

            time.sleep(interval)

    except KeyboardInterrupt:
        console.print("\n\nBot detenido")

        if responder.action_log:
            console.print(f"\nAcciones realizadas: {len(responder.action_log)}")
            for entry in responder.action_log:
                console.print(
                    f"   [{entry['action']:8s}] {entry['subject'][:50]} "
                    f"-> {entry['category']}"
                )

    finally:
        connector.disconnect()


if __name__ == "__main__":
    cli()
