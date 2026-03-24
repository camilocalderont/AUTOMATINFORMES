"""Configuración centralizada desde variables de entorno."""

import os
from dataclasses import dataclass, field
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# Base de exportación de Power Automate
_PA_BASE = os.getenv(
    "POWERAUTOMATE_EXPORT_FOLDER",
    str(Path.home() / "Library/CloudStorage/OneDrive-UnidadAdministrativaEspecialDeCatastroDistrital/MailExport"),
)

# Perfiles de buzón disponibles
MAILBOX_PROFILES = {
    "pandora": {
        "export_folder": os.path.join(_PA_BASE, "pandora"),
        "smtp_email": os.getenv("SMTP_EMAIL_PANDORA", os.getenv("SMTP_EMAIL", os.getenv("MAIL_USERNAME", ""))),
        "smtp_password": os.getenv("SMTP_PASSWORD_PANDORA", os.getenv("SMTP_PASSWORD", os.getenv("MAIL_PASSWORD", ""))),
        "description": "Buzón compartido de la entidad",
    },
    "personal": {
        "export_folder": os.path.join(_PA_BASE, "personal"),
        "smtp_email": os.getenv("SMTP_EMAIL_PERSONAL", ""),
        "smtp_password": os.getenv("SMTP_PASSWORD_PERSONAL", ""),
        "description": "Buzón personal del contratista",
    },
}


@dataclass
class Config:
    # Método de conexión: powerautomate | smtp | graph | imap_oauth | imap_basic
    connection_method: str = os.getenv("CONNECTION_METHOD", "powerautomate")

    # Perfil activo (pandora | personal)
    mailbox: str = os.getenv("MAILBOX", "pandora")

    # Graph API
    azure_client_id: str = os.getenv("AZURE_CLIENT_ID", "")
    azure_tenant_id: str = os.getenv("AZURE_TENANT_ID", "")
    graph_scopes: list[str] = field(default_factory=lambda: os.getenv(
        "GRAPH_SCOPES", "Mail.Read,Mail.Send"
    ).split(","))

    # IMAP
    imap_server: str = os.getenv("IMAP_SERVER", "outlook.office365.com")
    imap_port: int = int(os.getenv("IMAP_PORT", "993"))
    imap_email: str = os.getenv("IMAP_EMAIL", "")
    imap_password: str = os.getenv("IMAP_PASSWORD", "")

    # SMTP base (se puede sobreescribir por perfil)
    smtp_host: str = os.getenv("SMTP_HOST", os.getenv("MAIL_HOST", "smtp.office365.com"))
    smtp_port: int = int(os.getenv("SMTP_PORT", os.getenv("MAIL_PORT", "587")))
    smtp_email: str = os.getenv("SMTP_EMAIL", os.getenv("MAIL_USERNAME", ""))
    smtp_password: str = os.getenv("SMTP_PASSWORD", os.getenv("MAIL_PASSWORD", ""))

    # Power Automate base
    powerautomate_export_folder: str = _PA_BASE

    # General
    mail_folder: str = os.getenv("MAIL_FOLDER", "INBOX")
    user_email: str = os.getenv("USER_EMAIL", os.getenv("MAIL_USERNAME", ""))

    # Bot
    auto_respond: bool = os.getenv("AUTO_RESPOND", "false").lower() == "true"
    auto_respond_categories: list[str] = field(default_factory=lambda: os.getenv(
        "AUTO_RESPOND_CATEGORIES", "password_reset,user_data_request"
    ).split(","))

    # Anthropic (opcional)
    anthropic_api_key: str = os.getenv("ANTHROPIC_API_KEY", "")

    @property
    def active_profile(self) -> dict:
        return MAILBOX_PROFILES.get(self.mailbox, MAILBOX_PROFILES["pandora"])

    @property
    def active_export_folder(self) -> str:
        return self.active_profile["export_folder"]

    @property
    def active_smtp_email(self) -> str:
        return self.active_profile.get("smtp_email") or self.smtp_email

    @property
    def active_smtp_password(self) -> str:
        return self.active_profile.get("smtp_password") or self.smtp_password

    @property
    def graph_authority(self) -> str:
        return f"https://login.microsoftonline.com/{self.azure_tenant_id}"

    @property
    def graph_scope_urls(self) -> list[str]:
        return [f"https://graph.microsoft.com/{s.strip()}" for s in self.graph_scopes]


config = Config()
