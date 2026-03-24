"""
Analizador de estadísticas de soporte para informes de pago.

Extrae de los correos:
- Cantidad de correos respondidos vs recibidos
- Módulos PANDORA más soportados
- Distribución por entidad (IDARTES, IDT, SDMujer, UAECD)
- Tiempos de respuesta promedio
"""

import re
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timedelta

import pandas as pd

from connectors.base import EmailMessage


# ── Módulos conocidos de PANDORA ─────────────────────────────
PANDORA_MODULES = {
    "contratación": ["contrat", "contrato", "cdp", "crp", "solicitud de contrat"],
    "presupuesto": ["presupuest", "pac", "rubro", "apropiación", "cdp", "crp"],
    "nómina": ["nómina", "nomina", "liquidación", "prestacion"],
    "inventarios": ["inventario", "almacén", "almacen", "activo fijo"],
    "tesorería": ["tesorer", "pago", "orden de pago", "giro"],
    "contabilidad": ["contab", "balance", "causación"],
    "talento humano": ["talento", "funcionario", "vinculación", "planta"],
    "correspondencia": ["correspond", "radicado", "radicación"],
    "paa": ["paa", "plan anual de adquisiciones"],
    "reportes": ["reporte", "informe", "consulta", "exportar"],
    "usuarios": ["usuario", "contraseña", "password", "acceso", "perfil", "rol"],
    "general": [],  # catch-all
}

ENTITIES = {
    "IDARTES": ["idartes"],
    "IDT": ["idt", "turismo"],
    "SDMujer": ["sdmujer", "mujer", "secretaría de la mujer"],
    "UAECD": ["uaecd", "catastro"],
}


@dataclass
class SupportStats:
    """Resultado del análisis de soporte."""
    period_start: datetime
    period_end: datetime
    total_received: int = 0
    total_replied: int = 0
    module_counts: dict[str, int] = field(default_factory=dict)
    entity_counts: dict[str, int] = field(default_factory=dict)
    daily_volume: dict[str, int] = field(default_factory=dict)
    avg_response_hours: float = 0.0
    top_requesters: list[tuple[str, int]] = field(default_factory=list)
    unresponded: list[EmailMessage] = field(default_factory=list)


class SupportAnalyzer:
    """Analiza correos de soporte para generar estadísticas."""

    def __init__(self, user_email: str):
        self.user_email = user_email.lower()

    def analyze(
        self,
        inbox_emails: list[EmailMessage],
        sent_emails: list[EmailMessage],
        period_start: datetime,
        period_end: datetime,
    ) -> SupportStats:
        """Análisis completo de correos de soporte."""
        stats = SupportStats(
            period_start=period_start,
            period_end=period_end,
            total_received=len(inbox_emails),
            total_replied=self._count_replies(inbox_emails, sent_emails),
        )

        # Clasificar por módulo
        module_counter = Counter()
        for email in inbox_emails:
            module = self._detect_module(email)
            email.module = module
            module_counter[module] += 1
        stats.module_counts = dict(module_counter.most_common())

        # Clasificar por entidad
        entity_counter = Counter()
        for email in inbox_emails:
            entity = self._detect_entity(email)
            entity_counter[entity] += 1
        stats.entity_counts = dict(entity_counter.most_common())

        # Volumen diario
        daily = Counter()
        for email in inbox_emails:
            day_key = email.date.strftime("%Y-%m-%d")
            daily[day_key] += 1
        stats.daily_volume = dict(sorted(daily.items()))

        # Top solicitantes
        requesters = Counter(e.sender_name or e.sender for e in inbox_emails)
        stats.top_requesters = requesters.most_common(10)

        # Correos sin responder
        replied_conversations = {
            e.in_reply_to or e.conversation_id for e in sent_emails
        }
        stats.unresponded = [
            e for e in inbox_emails
            if (e.conversation_id not in replied_conversations
                and e.id not in replied_conversations)
        ]

        # Tiempo de respuesta promedio
        stats.avg_response_hours = self._calc_avg_response_time(
            inbox_emails, sent_emails
        )

        return stats

    def _detect_module(self, email: EmailMessage) -> str:
        """Detecta el módulo PANDORA mencionado en el correo."""
        text = f"{email.subject} {email.body_text[:500]}".lower()

        scores = {}
        for module, keywords in PANDORA_MODULES.items():
            if module == "general":
                continue
            score = sum(1 for kw in keywords if kw in text)
            if score > 0:
                scores[module] = score

        if scores:
            return max(scores, key=scores.get)
        return "general"

    def _detect_entity(self, email: EmailMessage) -> str:
        """Detecta la entidad (IDARTES, IDT, etc.) del correo."""
        text = f"{email.sender} {email.subject} {email.body_text[:300]}".lower()

        for entity, keywords in ENTITIES.items():
            if any(kw in text for kw in keywords):
                return entity

        # Intentar por dominio de correo
        domain = email.sender.split("@")[-1].lower() if "@" in email.sender else ""
        for entity, keywords in ENTITIES.items():
            if any(kw in domain for kw in keywords):
                return entity

        return "Otra"

    def _count_replies(
        self,
        inbox: list[EmailMessage],
        sent: list[EmailMessage],
    ) -> int:
        """Cuenta cuántos correos recibidos tienen respuesta."""
        # Simplificación: contar correos enviados que son respuestas (Re:)
        replies = [
            e for e in sent
            if e.subject.lower().startswith("re:")
            or e.in_reply_to
        ]
        return len(replies)

    def _calc_avg_response_time(
        self,
        inbox: list[EmailMessage],
        sent: list[EmailMessage],
    ) -> float:
        """Calcula tiempo promedio de respuesta en horas."""
        # Mapear correos recibidos por conversation_id
        received_by_conv = {}
        for e in inbox:
            key = e.conversation_id or e.id
            if key not in received_by_conv:
                received_by_conv[key] = e.date

        response_times = []
        for sent_email in sent:
            conv_key = sent_email.conversation_id or sent_email.in_reply_to
            if conv_key in received_by_conv:
                delta = sent_email.date - received_by_conv[conv_key]
                if timedelta(0) < delta < timedelta(days=7):
                    response_times.append(delta.total_seconds() / 3600)

        return sum(response_times) / len(response_times) if response_times else 0.0

    def to_dataframe(self, stats: SupportStats) -> dict[str, pd.DataFrame]:
        """Convierte estadísticas a DataFrames para reportes."""
        dfs = {}

        # Resumen general
        dfs["resumen"] = pd.DataFrame([{
            "Período": f"{stats.period_start:%Y-%m-%d} a {stats.period_end:%Y-%m-%d}",
            "Correos recibidos": stats.total_received,
            "Correos respondidos": stats.total_replied,
            "Tasa de respuesta": (
                f"{stats.total_replied / max(stats.total_received, 1) * 100:.1f}%"
            ),
            "Tiempo promedio respuesta (hrs)": f"{stats.avg_response_hours:.1f}",
        }])

        # Por módulo
        dfs["modulos"] = pd.DataFrame(
            list(stats.module_counts.items()),
            columns=["Módulo", "Cantidad"],
        )

        # Por entidad
        dfs["entidades"] = pd.DataFrame(
            list(stats.entity_counts.items()),
            columns=["Entidad", "Cantidad"],
        )

        # Top solicitantes
        dfs["solicitantes"] = pd.DataFrame(
            stats.top_requesters,
            columns=["Solicitante", "Cantidad"],
        )

        # Volumen diario
        dfs["diario"] = pd.DataFrame(
            list(stats.daily_volume.items()),
            columns=["Fecha", "Cantidad"],
        )

        return dfs

    def print_report(self, stats: SupportStats):
        """Imprime reporte formateado en consola."""
        from rich.console import Console
        from rich.table import Table

        console = Console()

        console.print(
            f"\n[bold]📊 REPORTE DE SOPORTE PANDORA[/bold]"
            f"\n   Período: {stats.period_start:%Y-%m-%d} → {stats.period_end:%Y-%m-%d}\n"
        )

        # Resumen
        table = Table(title="Resumen General")
        table.add_column("Métrica")
        table.add_column("Valor", justify="right")
        table.add_row("Correos recibidos", str(stats.total_received))
        table.add_row("Correos respondidos", str(stats.total_replied))
        rate = stats.total_replied / max(stats.total_received, 1) * 100
        table.add_row("Tasa de respuesta", f"{rate:.1f}%")
        table.add_row("Tiempo promedio respuesta", f"{stats.avg_response_hours:.1f} hrs")
        console.print(table)

        # Módulos
        if stats.module_counts:
            table = Table(title="\nMódulos más soportados")
            table.add_column("Módulo")
            table.add_column("Solicitudes", justify="right")
            table.add_column("Porcentaje", justify="right")
            for mod, count in stats.module_counts.items():
                pct = count / max(stats.total_received, 1) * 100
                table.add_row(mod.capitalize(), str(count), f"{pct:.1f}%")
            console.print(table)

        # Entidades
        if stats.entity_counts:
            table = Table(title="\nPor Entidad")
            table.add_column("Entidad")
            table.add_column("Solicitudes", justify="right")
            for ent, count in stats.entity_counts.items():
                table.add_row(ent, str(count))
            console.print(table)

        # Top solicitantes
        if stats.top_requesters:
            table = Table(title="\nTop 10 Solicitantes")
            table.add_column("Nombre")
            table.add_column("Solicitudes", justify="right")
            for name, count in stats.top_requesters[:10]:
                table.add_row(name, str(count))
            console.print(table)
