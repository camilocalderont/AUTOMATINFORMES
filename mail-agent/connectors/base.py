"""Interfaz abstracta para conectores de correo."""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class EmailMessage:
    """Representación normalizada de un correo."""
    id: str
    subject: str
    sender: str
    sender_name: str
    recipients: list[str]
    date: datetime
    body_text: str
    body_html: str = ""
    folder: str = ""
    is_read: bool = False
    has_attachments: bool = False
    conversation_id: str = ""
    in_reply_to: str = ""
    # Campos de análisis (se llenan después)
    category: str = ""
    module: str = ""
    tags: list[str] = field(default_factory=list)

    def __repr__(self):
        return f"<Email {self.date:%Y-%m-%d} from={self.sender_name} subj='{self.subject[:50]}'>"


class BaseConnector(ABC):
    """Interfaz que deben implementar todos los conectores."""

    @abstractmethod
    def connect(self) -> bool:
        """Establece conexión. Retorna True si exitosa."""
        ...

    @abstractmethod
    def disconnect(self):
        """Cierra conexión limpiamente."""
        ...

    @abstractmethod
    def fetch_emails(
        self,
        folder: str = "INBOX",
        since: datetime | None = None,
        until: datetime | None = None,
        limit: int = 100,
    ) -> list[EmailMessage]:
        """Obtiene correos en un rango de fechas."""
        ...

    @abstractmethod
    def send_reply(
        self,
        original: EmailMessage,
        body_html: str,
    ) -> bool:
        """Envía una respuesta a un correo."""
        ...

    def fetch_sent_emails(
        self,
        since: datetime | None = None,
        until: datetime | None = None,
        limit: int = 100,
    ) -> list[EmailMessage]:
        """Obtiene correos enviados (para contar respuestas)."""
        return self.fetch_emails(
            folder="Sent Items", since=since, until=until, limit=limit
        )
