"""
Conector SMTP para envío de correos via Outlook/M365.

Probado y funcional con smtp.office365.com:587 + STARTTLS.
Solo soporta ENVÍO. Para lectura, usar PowerAutomateConnector.
"""

import smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from connectors.base import BaseConnector, EmailMessage


class SmtpConnector(BaseConnector):
    """Conector SMTP para envío de correos (no soporta lectura)."""

    def __init__(self, host: str, port: int, email: str, password: str):
        self.host = host
        self.port = port
        self.email = email
        self.password = password
        self._server: smtplib.SMTP | None = None

    def connect(self) -> bool:
        try:
            self._server = smtplib.SMTP(self.host, self.port, timeout=30)
            self._server.ehlo()
            self._server.starttls()
            self._server.ehlo()
            self._server.login(self.email, self.password)
            print(f"SMTP conectado: {self.email}")
            return True
        except Exception as e:
            print(f"Error SMTP: {e}")
            return False

    def disconnect(self):
        if self._server:
            try:
                self._server.quit()
            except Exception:
                pass
            self._server = None

    def fetch_emails(
        self,
        folder: str = "INBOX",
        since: datetime | None = None,
        until: datetime | None = None,
        limit: int = 100,
    ) -> list[EmailMessage]:
        print("SMTP no soporta lectura de correos.")
        print("Usa PowerAutomateConnector para leer.")
        return []

    def send_reply(self, original: EmailMessage, body_html: str) -> bool:
        """Envía respuesta a un correo usando SMTP."""
        if not self._server:
            print("No conectado a SMTP")
            return False

        msg = MIMEMultipart("alternative")
        msg["From"] = self.email
        msg["To"] = original.sender
        msg["Subject"] = f"Re: {original.subject}"
        msg["In-Reply-To"] = original.id
        msg["References"] = original.id

        msg.attach(MIMEText(body_html, "html", "utf-8"))

        try:
            self._server.sendmail(self.email, [original.sender], msg.as_string())
            print(f"Respuesta enviada a {original.sender}")
            return True
        except Exception as e:
            print(f"Error enviando: {e}")
            return False

    def send_email(
        self, to: str | list[str], subject: str, body_html: str, cc: str | list[str] | None = None
    ) -> bool:
        """Envía un correo nuevo (no respuesta)."""
        if not self._server:
            print("No conectado a SMTP")
            return False

        if isinstance(to, str):
            to = [to]
        if isinstance(cc, str):
            cc = [cc]

        msg = MIMEMultipart("alternative")
        msg["From"] = self.email
        msg["To"] = ", ".join(to)
        if cc:
            msg["Cc"] = ", ".join(cc)
        msg["Subject"] = subject

        msg.attach(MIMEText(body_html, "html", "utf-8"))

        recipients = to + (cc or [])
        try:
            self._server.sendmail(self.email, recipients, msg.as_string())
            print(f"Correo enviado a {', '.join(to)}")
            return True
        except Exception as e:
            print(f"Error enviando: {e}")
            return False
