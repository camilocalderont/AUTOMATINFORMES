"""
Bot de respuesta automática.

Flujo:
1. Recibe correo clasificado
2. Si es auto_respondable → prepara respuesta con template
3. Muestra preview para aprobación (modo semi-automático)
4. Envía respuesta via conector

⚠️ MODO SEGURO: Por defecto, las respuestas requieren aprobación humana.
   Cambia FULL_AUTO=true en .env para modo totalmente automático (bajo tu riesgo).
"""

import os
from datetime import datetime

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm

from connectors.base import BaseConnector, EmailMessage
from analyzers.classifier import ClassificationResult, EmailCategory
from responders.templates import render_template

console = Console()


class AutoResponder:
    """Motor de respuestas automáticas."""

    def __init__(self, connector: BaseConnector, full_auto: bool = False):
        self.connector = connector
        self.full_auto = full_auto
        self._log: list[dict] = []

    def process(
        self,
        email: EmailMessage,
        classification: ClassificationResult,
    ) -> bool:
        """Procesa un correo clasificado y decide si responder."""

        if not classification.auto_respondable:
            console.print(
                f"  ⏭️  [dim]{email.subject[:60]}[/] → "
                f"[yellow]Requiere atención manual[/] ({classification.category.value})"
            )
            self._log_action(email, classification, "skipped", "Requiere revisión manual")
            return False

        # Preparar datos para el template
        template_data = {
            "sender_name": email.sender_name or email.sender.split("@")[0],
            **classification.extracted_data,
        }

        # Renderizar respuesta
        response_html = render_template(classification.category, template_data)
        if not response_html:
            console.print(f"  ⚠️  Sin template para {classification.category.value}")
            return False

        # Preview
        console.print(
            Panel(
                f"[bold]Para:[/] {email.sender}\n"
                f"[bold]Asunto:[/] Re: {email.subject}\n"
                f"[bold]Categoría:[/] {classification.category.value}\n"
                f"[bold]Confianza:[/] {classification.confidence:.0%}\n\n"
                f"[dim]--- Vista previa de respuesta ---[/]\n"
                f"{self._html_preview(response_html)}",
                title="📤 Respuesta preparada",
                border_style="green",
            )
        )

        # Aprobación
        if not self.full_auto:
            approved = Confirm.ask("¿Enviar esta respuesta?", default=False)
            if not approved:
                console.print("  ❌ Respuesta cancelada")
                self._log_action(email, classification, "rejected", "Cancelada por usuario")
                return False

        # Enviar
        success = self.connector.send_reply(email, response_html)

        if success:
            self._log_action(email, classification, "sent", "Respuesta enviada")
        else:
            self._log_action(email, classification, "error", "Error al enviar")

        return success

    def process_batch(
        self,
        classified_emails: list[tuple[EmailMessage, ClassificationResult]],
    ) -> dict:
        """Procesa un lote de correos clasificados."""
        results = {"sent": 0, "skipped": 0, "rejected": 0, "errors": 0}

        auto_respondable = [
            (e, c) for e, c in classified_emails if c.auto_respondable
        ]
        manual = [
            (e, c) for e, c in classified_emails if not c.auto_respondable
        ]

        console.print(f"\n[bold]📬 Procesando {len(classified_emails)} correos[/]")
        console.print(
            f"   Auto-respondables: {len(auto_respondable)} | "
            f"Manuales: {len(manual)}\n"
        )

        for email, classification in auto_respondable:
            success = self.process(email, classification)
            if success:
                results["sent"] += 1
            else:
                results["skipped"] += 1

        results["skipped"] += len(manual)

        console.print(f"\n[bold]Resumen:[/]")
        console.print(f"  ✅ Enviados: {results['sent']}")
        console.print(f"  ⏭️  Omitidos: {results['skipped']}")
        console.print(f"  ❌ Rechazados: {results['rejected']}")

        return results

    def _html_preview(self, html: str, max_lines: int = 15) -> str:
        """Genera preview legible del HTML."""
        import html2text
        h = html2text.HTML2Text()
        h.ignore_links = True
        h.body_width = 70
        text = h.handle(html)
        lines = text.strip().split("\n")
        if len(lines) > max_lines:
            return "\n".join(lines[:max_lines]) + "\n[dim]...(truncado)[/]"
        return "\n".join(lines)

    def _log_action(
        self,
        email: EmailMessage,
        classification: ClassificationResult,
        action: str,
        note: str,
    ):
        """Registra acción para auditoría."""
        self._log.append({
            "timestamp": datetime.now().isoformat(),
            "email_id": email.id,
            "subject": email.subject,
            "sender": email.sender,
            "category": classification.category.value,
            "confidence": classification.confidence,
            "action": action,
            "note": note,
        })

    @property
    def action_log(self) -> list[dict]:
        return self._log
