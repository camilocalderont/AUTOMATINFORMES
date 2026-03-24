"""Factory para crear el conector apropiado según configuración."""

from config import Config
from connectors.base import BaseConnector, EmailMessage


def create_connector(cfg: Config) -> BaseConnector:
    """Crea el conector según CONNECTION_METHOD en .env"""
    method = cfg.connection_method.lower()

    if method == "graph":
        from connectors.graph_connector import GraphConnector
        return GraphConnector(cfg)
    elif method == "imap_oauth":
        from connectors.imap_connector import ImapConnector
        return ImapConnector(cfg, use_oauth=True)
    elif method == "imap_basic":
        from connectors.imap_connector import ImapConnector
        return ImapConnector(cfg, use_oauth=False)
    elif method == "powerautomate":
        from connectors.powerautomate_connector import PowerAutomateConnector
        return PowerAutomateConnector(
            export_folder=cfg.active_export_folder,
            smtp_host=cfg.smtp_host,
            smtp_port=cfg.smtp_port,
            smtp_email=cfg.active_smtp_email,
            smtp_password=cfg.active_smtp_password,
        )
    elif method == "smtp":
        from connectors.smtp_connector import SmtpConnector
        return SmtpConnector(
            host=cfg.smtp_host,
            port=cfg.smtp_port,
            email=cfg.active_smtp_email,
            password=cfg.active_smtp_password,
        )
    else:
        raise ValueError(
            f"CONNECTION_METHOD '{method}' no válido. "
            f"Usa: graph, imap_oauth, imap_basic, powerautomate, smtp"
        )


__all__ = ["create_connector", "BaseConnector", "EmailMessage"]
