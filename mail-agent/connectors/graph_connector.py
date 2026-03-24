"""
Conector Microsoft Graph API con Device Code Flow.

Este es el método RECOMENDADO para entornos corporativos M365 donde:
- No tienes permisos de admin para registrar apps con admin consent
- IMAP está deshabilitado
- Necesitas permisos delegados (actúas como tú mismo)

El Device Code Flow funciona así:
1. La app genera un código temporal
2. Tú vas a https://microsoft.com/devicelogin e ingresas el código
3. Te autorizas con tu cuenta corporativa
4. La app recibe un token OAuth2

NO requiere admin consent para permisos delegados como Mail.Read y Mail.Send.
"""

import json
import time
from datetime import datetime, timezone
from pathlib import Path

import msal
import requests
from bs4 import BeautifulSoup
import html2text

from config import Config
from connectors.base import BaseConnector, EmailMessage

# Cache de tokens para no pedir login cada vez
TOKEN_CACHE_FILE = Path.home() / ".pandora_mail_token_cache.json"
GRAPH_BASE = "https://graph.microsoft.com/v1.0"


class GraphConnector(BaseConnector):
    """Conector usando Microsoft Graph API + Device Code Flow."""

    def __init__(self, cfg: Config):
        self.cfg = cfg
        self._token: str = ""
        self._cache = msal.SerializableTokenCache()
        self._app: msal.PublicClientApplication | None = None
        self._load_cache()

    # ── Cache de tokens ──────────────────────────────────────

    def _load_cache(self):
        if TOKEN_CACHE_FILE.exists():
            self._cache.deserialize(TOKEN_CACHE_FILE.read_text())

    def _save_cache(self):
        if self._cache.has_state_changed:
            TOKEN_CACHE_FILE.write_text(self._cache.serialize())

    # ── Conexión ─────────────────────────────────────────────

    def connect(self) -> bool:
        """Obtiene token via device code flow o cache."""
        self._app = msal.PublicClientApplication(
            client_id=self.cfg.azure_client_id,
            authority=self.cfg.graph_authority,
            token_cache=self._cache,
        )

        scopes = self.cfg.graph_scope_urls

        # Intentar token desde cache (silent)
        accounts = self._app.get_accounts()
        if accounts:
            result = self._app.acquire_token_silent(scopes, account=accounts[0])
            if result and "access_token" in result:
                self._token = result["access_token"]
                self._save_cache()
                print("✅ Conectado con token en cache (sin login necesario)")
                return True

        # Device code flow
        flow = self._app.initiate_device_flow(scopes=scopes)
        if "user_code" not in flow:
            print(f"❌ Error iniciando device flow: {flow}")
            return False

        print("\n" + "=" * 60)
        print("🔐 AUTENTICACIÓN REQUERIDA")
        print("=" * 60)
        print(f"1. Abre: {flow['verification_uri']}")
        print(f"2. Ingresa el código: {flow['user_code']}")
        print(f"3. Autoriza con tu cuenta corporativa")
        print("=" * 60)
        print("Esperando autorización...\n")

        result = self._app.acquire_token_by_device_flow(flow)

        if "access_token" in result:
            self._token = result["access_token"]
            self._save_cache()
            print("✅ Autenticación exitosa!")
            return True

        print(f"❌ Error de autenticación: {result.get('error_description', result)}")
        return False

    def disconnect(self):
        self._token = ""

    # ── Headers ──────────────────────────────────────────────

    @property
    def _headers(self) -> dict:
        return {
            "Authorization": f"Bearer {self._token}",
            "Content-Type": "application/json",
        }

    # ── Lectura de correos ───────────────────────────────────

    def fetch_emails(
        self,
        folder: str = "INBOX",
        since: datetime | None = None,
        until: datetime | None = None,
        limit: int = 100,
    ) -> list[EmailMessage]:
        """Obtiene correos via Graph API con paginación."""

        # Mapeo de nombres de carpeta comunes
        folder_map = {
            "INBOX": "Inbox",
            "Sent Items": "SentItems",
            "SENT": "SentItems",
            "Drafts": "Drafts",
        }
        graph_folder = folder_map.get(folder, folder)

        # Construir filtro OData
        filters = []
        if since:
            filters.append(
                f"receivedDateTime ge {since.strftime('%Y-%m-%dT%H:%M:%SZ')}"
            )
        if until:
            filters.append(
                f"receivedDateTime le {until.strftime('%Y-%m-%dT%H:%M:%SZ')}"
            )

        params = {
            "$top": min(limit, 50),  # Graph API max por página
            "$orderby": "receivedDateTime desc",
            "$select": (
                "id,subject,from,toRecipients,receivedDateTime,"
                "body,isRead,hasAttachments,conversationId,"
                "internetMessageHeaders"
            ),
        }
        if filters:
            params["$filter"] = " and ".join(filters)

        url = f"{GRAPH_BASE}/me/mailFolders/{graph_folder}/messages"
        messages: list[EmailMessage] = []

        while url and len(messages) < limit:
            resp = requests.get(url, headers=self._headers, params=params)

            if resp.status_code == 401:
                print("⚠️ Token expirado, reconectando...")
                if self.connect():
                    resp = requests.get(url, headers=self._headers, params=params)
                else:
                    break

            if resp.status_code != 200:
                print(f"❌ Error {resp.status_code}: {resp.text[:200]}")
                break

            data = resp.json()

            for msg in data.get("value", []):
                email = self._parse_graph_message(msg)
                messages.append(email)

            # Paginación
            url = data.get("@odata.nextLink")
            params = {}  # nextLink ya incluye los params

        return messages[:limit]

    def _parse_graph_message(self, msg: dict) -> EmailMessage:
        """Convierte un mensaje de Graph API a EmailMessage."""
        from_data = msg.get("from", {}).get("emailAddress", {})
        recipients = [
            r.get("emailAddress", {}).get("address", "")
            for r in msg.get("toRecipients", [])
        ]

        body_html = msg.get("body", {}).get("content", "")
        body_text = self._html_to_text(body_html)

        # Extraer In-Reply-To de headers
        in_reply_to = ""
        for header in msg.get("internetMessageHeaders", []):
            if header.get("name", "").lower() == "in-reply-to":
                in_reply_to = header.get("value", "")
                break

        return EmailMessage(
            id=msg.get("id", ""),
            subject=msg.get("subject", "(Sin asunto)"),
            sender=from_data.get("address", ""),
            sender_name=from_data.get("name", ""),
            recipients=recipients,
            date=datetime.fromisoformat(
                msg.get("receivedDateTime", "").replace("Z", "+00:00")
            ),
            body_text=body_text,
            body_html=body_html,
            is_read=msg.get("isRead", False),
            has_attachments=msg.get("hasAttachments", False),
            conversation_id=msg.get("conversationId", ""),
            in_reply_to=in_reply_to,
        )

    def _html_to_text(self, html_content: str) -> str:
        """Convierte HTML a texto limpio."""
        if not html_content:
            return ""
        h = html2text.HTML2Text()
        h.ignore_links = False
        h.ignore_images = True
        h.body_width = 0
        return h.handle(html_content).strip()

    # ── Envío de respuestas ──────────────────────────────────

    def send_reply(self, original: EmailMessage, body_html: str) -> bool:
        """Envía respuesta a un correo usando Graph API."""
        url = f"{GRAPH_BASE}/me/messages/{original.id}/reply"

        payload = {
            "message": {
                "toRecipients": [
                    {
                        "emailAddress": {
                            "address": original.sender,
                            "name": original.sender_name,
                        }
                    }
                ],
            },
            "comment": body_html,
        }

        resp = requests.post(url, headers=self._headers, json=payload)

        if resp.status_code == 202:
            print(f"✅ Respuesta enviada a {original.sender}")
            return True

        print(f"❌ Error enviando respuesta: {resp.status_code} {resp.text[:200]}")
        return False

    # ── Utilidades ───────────────────────────────────────────

    def get_me(self) -> dict:
        """Verifica la conexión obteniendo el perfil del usuario."""
        resp = requests.get(f"{GRAPH_BASE}/me", headers=self._headers)
        return resp.json() if resp.status_code == 200 else {}
