"""
Conector IMAP para Outlook/M365.

Soporta dos modos:
- OAuth2 (XOAUTH2): Usa token de MSAL para autenticarse
- Basic Auth: Usuario/contraseña directa (probablemente bloqueado en M365)

⚠️ NOTA: Muchas organizaciones M365 deshabilitan IMAP.
Si ves "LOGIN failed" o "AUTHENTICATE failed", usa GraphConnector.
"""

import email
import imaplib
import ssl
from datetime import datetime
from email.header import decode_header
from email.utils import parsedate_to_datetime

import msal
from bs4 import BeautifulSoup
import html2text

from config import Config
from connectors.base import BaseConnector, EmailMessage


class ImapConnector(BaseConnector):
    """Conector IMAP con soporte OAuth2 y Basic Auth."""

    def __init__(self, cfg: Config, use_oauth: bool = True):
        self.cfg = cfg
        self.use_oauth = use_oauth
        self._conn: imaplib.IMAP4_SSL | None = None
        self._token: str = ""

    # ── Conexión ─────────────────────────────────────────────

    def connect(self) -> bool:
        try:
            ctx = ssl.create_default_context()
            self._conn = imaplib.IMAP4_SSL(
                self.cfg.imap_server, self.cfg.imap_port, ssl_context=ctx
            )

            if self.use_oauth:
                return self._connect_oauth()
            else:
                return self._connect_basic()

        except Exception as e:
            print(f"❌ Error de conexión IMAP: {e}")
            if "LOGIN failed" in str(e) or "AUTHENTICATE failed" in str(e):
                print("\n💡 Tu organización probablemente tiene IMAP deshabilitado.")
                print("   Usa CONNECTION_METHOD=graph en tu .env")
            return False

    def _connect_oauth(self) -> bool:
        """Autenticación IMAP con OAuth2 (XOAUTH2)."""
        app = msal.PublicClientApplication(
            client_id=self.cfg.azure_client_id,
            authority=self.cfg.graph_authority,
        )

        # Scope para IMAP es diferente al de Graph
        scopes = ["https://outlook.office365.com/IMAP.AccessAsUser.All"]

        # Intentar silent primero
        accounts = app.get_accounts()
        result = None
        if accounts:
            result = app.acquire_token_silent(scopes, account=accounts[0])

        if not result or "access_token" not in result:
            flow = app.initiate_device_flow(scopes=scopes)
            if "user_code" not in flow:
                print(f"❌ Error en device flow: {flow}")
                return False

            print(f"\n🔐 Abre {flow['verification_uri']} e ingresa: {flow['user_code']}")
            result = app.acquire_token_by_device_flow(flow)

        if "access_token" not in result:
            print(f"❌ Error OAuth: {result.get('error_description')}")
            return False

        self._token = result["access_token"]

        # Construir string XOAUTH2
        user = self.cfg.imap_email
        auth_string = f"user={user}\x01auth=Bearer {self._token}\x01\x01"

        try:
            self._conn.authenticate("XOAUTH2", lambda _: auth_string.encode())
            print("✅ Conectado via IMAP + OAuth2")
            return True
        except Exception as e:
            print(f"❌ XOAUTH2 falló: {e}")
            return False

    def _connect_basic(self) -> bool:
        """Autenticación IMAP básica (usuario/contraseña)."""
        try:
            self._conn.login(self.cfg.imap_email, self.cfg.imap_password)
            print("✅ Conectado via IMAP + Basic Auth")
            return True
        except Exception as e:
            print(f"❌ Login básico falló: {e}")
            return False

    def disconnect(self):
        if self._conn:
            try:
                self._conn.logout()
            except Exception:
                pass
            self._conn = None

    # ── Lectura de correos ───────────────────────────────────

    def fetch_emails(
        self,
        folder: str = "INBOX",
        since: datetime | None = None,
        until: datetime | None = None,
        limit: int = 100,
    ) -> list[EmailMessage]:
        if not self._conn:
            print("❌ No conectado")
            return []

        # Seleccionar carpeta
        status, _ = self._conn.select(f'"{folder}"', readonly=True)
        if status != "OK":
            print(f"❌ No se pudo abrir carpeta: {folder}")
            return []

        # Construir búsqueda IMAP
        criteria = []
        if since:
            criteria.append(f'SINCE {since.strftime("%d-%b-%Y")}')
        if until:
            criteria.append(f'BEFORE {until.strftime("%d-%b-%Y")}')

        search_str = " ".join(criteria) if criteria else "ALL"

        status, msg_ids = self._conn.search(None, search_str)
        if status != "OK":
            return []

        ids = msg_ids[0].split()
        # Tomar los más recientes
        ids = ids[-limit:]
        ids.reverse()

        messages = []
        for mid in ids:
            status, msg_data = self._conn.fetch(mid, "(RFC822)")
            if status != "OK":
                continue

            raw = msg_data[0][1]
            msg = email.message_from_bytes(raw)
            parsed = self._parse_email(msg, mid.decode())
            if parsed:
                messages.append(parsed)

        return messages

    def _parse_email(self, msg: email.message.Message, uid: str) -> EmailMessage | None:
        """Parsea un email MIME a EmailMessage."""
        try:
            subject = self._decode_header(msg.get("Subject", ""))
            from_raw = msg.get("From", "")
            sender_name, sender_addr = email.utils.parseaddr(from_raw)
            sender_name = self._decode_header(sender_name) or sender_addr

            date = parsedate_to_datetime(msg.get("Date", ""))

            body_text, body_html = self._extract_body(msg)

            recipients = [
                email.utils.parseaddr(r)[1]
                for r in (msg.get("To", "")).split(",")
            ]

            return EmailMessage(
                id=uid,
                subject=subject,
                sender=sender_addr,
                sender_name=sender_name,
                recipients=recipients,
                date=date,
                body_text=body_text,
                body_html=body_html,
                conversation_id=msg.get("Thread-Index", ""),
                in_reply_to=msg.get("In-Reply-To", ""),
            )
        except Exception as e:
            print(f"⚠️ Error parseando email {uid}: {e}")
            return None

    def _decode_header(self, header: str) -> str:
        """Decodifica headers con encoding."""
        if not header:
            return ""
        parts = decode_header(header)
        decoded = []
        for part, charset in parts:
            if isinstance(part, bytes):
                decoded.append(part.decode(charset or "utf-8", errors="replace"))
            else:
                decoded.append(part)
        return " ".join(decoded)

    def _extract_body(self, msg: email.message.Message) -> tuple[str, str]:
        """Extrae texto y HTML del cuerpo del correo."""
        text_body = ""
        html_body = ""

        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                if content_type == "text/plain":
                    text_body = part.get_payload(decode=True).decode(
                        part.get_content_charset() or "utf-8", errors="replace"
                    )
                elif content_type == "text/html":
                    html_body = part.get_payload(decode=True).decode(
                        part.get_content_charset() or "utf-8", errors="replace"
                    )
        else:
            payload = msg.get_payload(decode=True)
            if payload:
                content = payload.decode(
                    msg.get_content_charset() or "utf-8", errors="replace"
                )
                if msg.get_content_type() == "text/html":
                    html_body = content
                    h = html2text.HTML2Text()
                    h.ignore_links = False
                    text_body = h.handle(content)
                else:
                    text_body = content

        if html_body and not text_body:
            h = html2text.HTML2Text()
            h.ignore_links = False
            text_body = h.handle(html_body)

        return text_body, html_body

    # ── Envío de respuestas ──────────────────────────────────

    def send_reply(self, original: EmailMessage, body_html: str) -> bool:
        """IMAP no envía correos. Se necesitaría SMTP adicional."""
        print("⚠️ IMAP no soporta envío. Usa GraphConnector para respuestas.")
        print("   Alternativa: configurar SMTP con smtplib")
        return False
