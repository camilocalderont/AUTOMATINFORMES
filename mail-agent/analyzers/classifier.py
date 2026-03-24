"""
Clasificador de correos para el bot de respuesta automática.

Clasifica correos en categorías accionables:
- password_reset: Solicitudes de reseteo de contraseña
- user_data_request: Solicitudes de datos de usuario
- bug_report: Reportes de errores en PANDORA
- feature_request: Solicitudes de nuevas funcionalidades
- access_request: Solicitudes de acceso/permisos
- support_question: Preguntas de soporte general
- informational: Correos informativos (no requieren acción)
- escalation: Requiere escalación humana
"""

import re
from dataclasses import dataclass
from enum import Enum

from connectors.base import EmailMessage


class EmailCategory(str, Enum):
    PASSWORD_RESET = "password_reset"
    USER_DATA_REQUEST = "user_data_request"
    BUG_REPORT = "bug_report"
    FEATURE_REQUEST = "feature_request"
    ACCESS_REQUEST = "access_request"
    SUPPORT_QUESTION = "support_question"
    INFORMATIONAL = "informational"
    ESCALATION = "escalation"


@dataclass
class ClassificationResult:
    category: EmailCategory
    confidence: float  # 0.0 - 1.0
    reason: str
    auto_respondable: bool
    suggested_action: str
    extracted_data: dict  # datos extraídos relevantes


# ── Reglas de clasificación basadas en patrones ──────────────

CLASSIFICATION_RULES: list[dict] = [
    {
        "category": EmailCategory.PASSWORD_RESET,
        "patterns": [
            r"contrase[ñn]a",
            r"password",
            r"reset(ear)?",
            r"no\s+pued[eo]\s+(?:ingres|entr|acced)",
            r"olvid[éeó]\s+(?:mi\s+)?(?:clave|contrase)",
            r"bloqueado",
            r"cambio\s+de\s+(?:clave|contrase)",
        ],
        "auto_respondable": True,
        "action": "Verificar usuario en BD y resetear contraseña",
    },
    {
        "category": EmailCategory.USER_DATA_REQUEST,
        "patterns": [
            r"datos\s+del?\s+usuario",
            r"(?:cu[aá]l|dame|env[ií]a)\s+(?:es\s+)?(?:mi|el|su)\s+(?:usuario|login|correo)",
            r"informaci[oó]n\s+del?\s+(?:usuario|cuenta|perfil)",
            r"credenciales",
        ],
        "auto_respondable": True,
        "action": "Consultar datos del usuario en PANDORA y enviar info",
    },
    {
        "category": EmailCategory.ACCESS_REQUEST,
        "patterns": [
            r"(?:solicito|necesito|requiero)\s+(?:acceso|permiso|rol)",
            r"asign(?:ar|ación)\s+(?:de\s+)?(?:rol|perfil|permiso)",
            r"habili?tar\s+(?:acceso|módulo|usuario)",
            r"nuevo\s+usuario",
            r"crear\s+(?:cuenta|usuario)",
        ],
        "auto_respondable": False,
        "action": "Requiere validación con el supervisor / admin funcional",
    },
    {
        "category": EmailCategory.BUG_REPORT,
        "patterns": [
            r"error\s+(?:en|al|cuando)",
            r"no\s+(?:funciona|carga|abre|guarda|genera)",
            r"falla\s+(?:en|al|cuando)",
            r"se\s+(?:cae|bloquea|congela|cierra)",
            r"pantalla\s+(?:en\s+)?blanco",
            r"(?:sale|aparece)\s+(?:un\s+)?error",
            r"bug",
        ],
        "auto_respondable": False,
        "action": "Registrar incidencia y solicitar capturas/pasos para reproducir",
    },
    {
        "category": EmailCategory.FEATURE_REQUEST,
        "patterns": [
            r"(?:se\s+)?podr[ií]a\s+(?:agregar|añadir|incluir|modificar)",
            r"solicitud\s+de\s+(?:mejora|cambio|desarrollo)",
            r"(?:nuevo|nueva)\s+(?:funcionalidad|requerimiento|campo|reporte)",
            r"requeri?miento\s+(?:funcional|nuevo)",
        ],
        "auto_respondable": False,
        "action": "Registrar requerimiento y priorizar",
    },
    {
        "category": EmailCategory.INFORMATIONAL,
        "patterns": [
            r"(?:les?\s+)?inform[oa](?:mos)?(?:\s+que)?",
            r"para\s+su\s+(?:conocimiento|información)",
            r"se\s+(?:les?\s+)?comunica",
            r"adjunt[oa]\s+(?:el|la|los)",
        ],
        "auto_respondable": False,
        "action": "Solo lectura, no requiere respuesta",
    },
]


class EmailClassifier:
    """Clasificador basado en reglas con extracción de datos."""

    def classify(self, email: EmailMessage) -> ClassificationResult:
        """Clasifica un correo y extrae datos relevantes."""
        text = f"{email.subject} {email.body_text[:1000]}".lower()

        best_match = None
        best_score = 0

        for rule in CLASSIFICATION_RULES:
            score = 0
            for pattern in rule["patterns"]:
                matches = re.findall(pattern, text, re.IGNORECASE)
                score += len(matches)

            if score > best_score:
                best_score = score
                best_match = rule

        if best_match and best_score > 0:
            confidence = min(best_score / 3, 1.0)  # Normalizar
            extracted = self._extract_data(email, best_match["category"])

            return ClassificationResult(
                category=best_match["category"],
                confidence=confidence,
                reason=f"Coincidencia con {best_score} patrón(es) de {best_match['category'].value}",
                auto_respondable=best_match["auto_respondable"],
                suggested_action=best_match["action"],
                extracted_data=extracted,
            )

        return ClassificationResult(
            category=EmailCategory.SUPPORT_QUESTION,
            confidence=0.3,
            reason="No coincide con patrones específicos, clasificado como soporte general",
            auto_respondable=False,
            suggested_action="Revisar manualmente y responder",
            extracted_data={},
        )

    def _extract_data(self, email: EmailMessage, category: EmailCategory) -> dict:
        """Extrae datos relevantes según la categoría."""
        text = f"{email.subject} {email.body_text[:2000]}"
        data = {}

        if category in (EmailCategory.PASSWORD_RESET, EmailCategory.USER_DATA_REQUEST):
            # Intentar extraer cédula/documento
            cedula = re.findall(r'\b\d{6,10}\b', text)
            if cedula:
                data["posible_documento"] = cedula[0]

            # Intentar extraer nombre de usuario
            user_match = re.search(
                r'(?:usuario|login|user)[\s:]+["\']?(\w+)["\']?',
                text,
                re.IGNORECASE,
            )
            if user_match:
                data["usuario_mencionado"] = user_match.group(1)

            # Extraer correo si es diferente al remitente
            emails = re.findall(r'[\w.+-]+@[\w-]+\.[\w.-]+', text)
            other_emails = [e for e in emails if e.lower() != email.sender.lower()]
            if other_emails:
                data["correos_mencionados"] = other_emails

        elif category == EmailCategory.BUG_REPORT:
            # Extraer módulo mencionado
            from analyzers.support_stats import PANDORA_MODULES
            for module, keywords in PANDORA_MODULES.items():
                if any(kw in text.lower() for kw in keywords):
                    data["modulo_afectado"] = module
                    break

        return data

    def classify_batch(
        self, emails: list[EmailMessage]
    ) -> list[tuple[EmailMessage, ClassificationResult]]:
        """Clasifica un lote de correos."""
        results = []
        for email in emails:
            result = self.classify(email)
            email.category = result.category.value
            results.append((email, result))
        return results

    def print_classification(self, email: EmailMessage, result: ClassificationResult):
        """Imprime clasificación formateada."""
        from rich.console import Console
        from rich.panel import Panel

        console = Console()

        color = {
            EmailCategory.PASSWORD_RESET: "yellow",
            EmailCategory.USER_DATA_REQUEST: "cyan",
            EmailCategory.BUG_REPORT: "red",
            EmailCategory.ACCESS_REQUEST: "magenta",
            EmailCategory.SUPPORT_QUESTION: "blue",
            EmailCategory.INFORMATIONAL: "dim",
            EmailCategory.ESCALATION: "bold red",
        }.get(result.category, "white")

        auto = "✅ AUTO" if result.auto_respondable else "🧑 MANUAL"
        conf = f"{'●' * int(result.confidence * 5)}{'○' * (5 - int(result.confidence * 5))}"

        text = (
            f"[bold]De:[/] {email.sender_name} <{email.sender}>\n"
            f"[bold]Asunto:[/] {email.subject}\n"
            f"[bold]Categoría:[/] [{color}]{result.category.value}[/]\n"
            f"[bold]Confianza:[/] {conf} ({result.confidence:.0%})\n"
            f"[bold]Respuesta:[/] {auto}\n"
            f"[bold]Acción:[/] {result.suggested_action}"
        )

        if result.extracted_data:
            text += f"\n[bold]Datos extraídos:[/] {result.extracted_data}"

        console.print(Panel(text, title=f"📧 {email.date:%Y-%m-%d %H:%M}"))
