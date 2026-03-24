"""
Conector que lee correos exportados por Power Automate.

Power Automate exporta correos como archivos JSON a una carpeta
de OneDrive. Este conector los lee y convierte a EmailMessage.

Flujo:
1. Power Automate guarda correos en OneDrive/{export_folder}/
   - inbox_{fecha}.json para bandeja de entrada
   - sent_{fecha}.json para correos enviados
2. Este conector lee esos archivos
3. Para responder, usa SmtpConnector

Estructura del JSON exportado por Power Automate:
[
  {
    "id": "AAMk...",
    "subject": "Asunto del correo",
    "from": "nombre@entidad.gov.co",
    "from_name": "Nombre Apellido",
    "to": ["dest1@entidad.gov.co"],
    "date": "2026-03-01T10:30:00Z",
    "body": "Texto completo del cuerpo del correo...",
    "is_read": true,
    "has_attachments": false,
    "conversation_id": "AAQk...",
    "importance": "normal"
  }
]

Solo se necesita un campo "body" con el texto completo.
No se necesita "body_html" — ahorra 95% de peso.
"""

import json
from datetime import datetime, timezone
from pathlib import Path

from connectors.base import BaseConnector, EmailMessage
from connectors.smtp_connector import SmtpConnector


class PowerAutomateConnector(BaseConnector):
    """Lee correos desde JSON exportados por Power Automate, envía via SMTP."""

    def __init__(
        self,
        export_folder: str,
        smtp_host: str = "",
        smtp_port: int = 587,
        smtp_email: str = "",
        smtp_password: str = "",
    ):
        self.export_folder = Path(export_folder)
        self._smtp: SmtpConnector | None = None
        if smtp_host and smtp_email:
            self._smtp = SmtpConnector(smtp_host, smtp_port, smtp_email, smtp_password)

    def connect(self) -> bool:
        if not self.export_folder.exists():
            print(f"Carpeta de export no existe: {self.export_folder}")
            print("Crea la carpeta o verifica la ruta en POWERAUTOMATE_EXPORT_FOLDER")
            return False

        json_files = list(self.export_folder.glob("*.json"))
        print(f"Carpeta de export: {self.export_folder}")
        print(f"Archivos JSON encontrados: {len(json_files)}")

        # Conectar SMTP si está configurado
        if self._smtp:
            smtp_ok = self._smtp.connect()
            if smtp_ok:
                print("SMTP listo para enviar respuestas")
            else:
                print("SMTP no disponible (solo lectura)")

        return True

    def disconnect(self):
        if self._smtp:
            self._smtp.disconnect()

    def fetch_emails(
        self,
        folder: str = "INBOX",
        since: datetime | None = None,
        until: datetime | None = None,
        limit: int = 100,
    ) -> list[EmailMessage]:
        """Lee correos desde archivos JSON exportados."""
        prefix = "inbox" if folder.upper() in ("INBOX", "") else "sent"
        messages = self._load_json_files(prefix)

        # Filtrar por fecha
        if since:
            since_aware = since if since.tzinfo else since.replace(tzinfo=timezone.utc)
            messages = [m for m in messages if m.date >= since_aware]
        if until:
            until_aware = until if until.tzinfo else until.replace(tzinfo=timezone.utc)
            messages = [m for m in messages if m.date <= until_aware]

        # Ordenar por fecha descendente
        messages.sort(key=lambda m: m.date, reverse=True)
        return messages[:limit]

    def fetch_sent_emails(
        self,
        since: datetime | None = None,
        until: datetime | None = None,
        limit: int = 100,
    ) -> list[EmailMessage]:
        return self.fetch_emails(folder="SENT", since=since, until=until, limit=limit)

    def send_reply(self, original: EmailMessage, body_html: str) -> bool:
        if self._smtp:
            return self._smtp.send_reply(original, body_html)
        print("SMTP no configurado. No se puede enviar.")
        return False

    def _load_json_files(self, prefix: str) -> list[EmailMessage]:
        """Carga todos los JSON que coincidan con el prefijo."""
        messages = []
        seen_ids = set()

        for json_file in sorted(self.export_folder.glob(f"{prefix}*.json"), reverse=True):
            try:
                data = json.loads(json_file.read_text(encoding="utf-8"))
                items = data if isinstance(data, list) else [data]
                for item in items:
                    msg = self._parse_json_email(item)
                    if msg and msg.id not in seen_ids:
                        messages.append(msg)
                        seen_ids.add(msg.id)
            except (json.JSONDecodeError, KeyError) as e:
                print(f"Error leyendo {json_file.name}: {e}")

        return messages

    def _parse_json_email(self, data: dict) -> EmailMessage | None:
        """Convierte un dict JSON a EmailMessage."""
        try:
            date_str = data.get("date", "")
            if date_str:
                # Soportar ISO 8601 con y sin Z
                date_str = date_str.replace("Z", "+00:00")
                date = datetime.fromisoformat(date_str)
            else:
                date = datetime.now(timezone.utc)

            from_addr = data.get("from", "")
            from_name = data.get("from_name", "")
            if not from_name and from_addr:
                from_name = from_addr.split("@")[0]

            to = data.get("to", [])
            if isinstance(to, str):
                to = [to]

            return EmailMessage(
                id=data.get("id", f"pa_{hash(date_str + from_addr)}"),
                subject=data.get("subject", "(Sin asunto)"),
                sender=from_addr,
                sender_name=from_name,
                recipients=to,
                date=date,
                body_text=data.get("body", data.get("body_text", "")),
                body_html=data.get("body_html", ""),
                is_read=data.get("is_read", False),
                has_attachments=data.get("has_attachments", False),
                conversation_id=data.get("conversation_id", ""),
                in_reply_to=data.get("in_reply_to", ""),
                folder=data.get("folder", ""),
            )
        except Exception as e:
            print(f"Error parseando email JSON: {e}")
            return None
