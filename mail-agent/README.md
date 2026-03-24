# PANDORA Mail Agent

Agente automatizado para lectura, análisis y respuesta de correos corporativos de Outlook/M365.

## Casos de Uso

1. **Informes de Pago**: Lee correos de soporte, extrae estadísticas por módulo, cuenta respuestas.
2. **Bot de Respuesta Automática**: Interpreta correos entrantes, clasifica por tipo (reset password, datos de usuario, soporte técnico) y sugiere/ejecuta respuestas automáticas.

## Métodos de Conexión

| Método | Leer | Enviar | Requiere Admin | Estado |
|--------|------|--------|----------------|--------|
| **Power Automate + SMTP** | JSON via OneDrive | SMTP directo | No | **RECOMENDADO** |
| **SMTP solo** | No | SMTP directo | No | Solo envío |
| Graph API + Device Code | Graph API | Graph API | Sí | Bloqueado por org |
| IMAP + OAuth2 | IMAP | No (+ SMTP) | Sí | Bloqueado por org |
| IMAP + Basic Auth | IMAP | No (+ SMTP) | - | Deshabilitado por Microsoft |

### Cómo funciona Power Automate + SMTP

```
Power Automate (M365)          Python (local)
┌─────────────────────┐        ┌──────────────────────────┐
│ Trigger: programado │        │                          │
│ o nuevo correo      │        │  PowerAutomateConnector   │
│                     │        │  (lee JSON de OneDrive)   │
│ Obtener correos     │──JSON──│                          │
│ Guardar en OneDrive │  sync  │  SupportAnalyzer         │
│                     │        │  (estadísticas)           │
│                     │        │                          │
│                     │        │  EmailClassifier          │
│                     │        │  (categoriza correos)     │
│                     │        │                          │
│                     │  SMTP  │  SmtpConnector            │
│                     │◄───────│  (envía respuestas)       │
└─────────────────────┘        └──────────────────────────┘
```

## Instalación

```bash
cd mail-agent
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Configuración

```bash
cp .env.example .env
# Editar .env con tus credenciales SMTP y ruta de OneDrive
```

### Configurar Power Automate (lectura de correos)

Ver **[POWER_AUTOMATE_SETUP.md](POWER_AUTOMATE_SETUP.md)** para instrucciones paso a paso.

## Uso

```bash
source .venv/bin/activate

# Probar conexión (SMTP + lectura de JSON)
python main.py test-connection

# Probar solo SMTP
python main.py test-smtp
python main.py test-smtp --to correo@prueba.com  # envía correo de prueba

# Leer correos exportados
python main.py read --days 30

# Estadísticas de soporte (módulos, respuestas, tiempos)
python main.py stats --days 30
python main.py stats --days 30 --export-csv

# Clasificar correos
python main.py classify --days 7
python main.py classify --days 7 --unread-only

# Bot de respuesta automática
python main.py bot --interval 300           # semi-automático (pide confirmación)
python main.py bot --interval 300 --auto    # full automático
```

## Estructura del Proyecto

```
mail-agent/
├── main.py                           # CLI principal (click)
├── config.py                         # Configuración desde .env
├── connectors/
│   ├── __init__.py                   # Factory: create_connector()
│   ├── base.py                       # Interfaz abstracta + EmailMessage
│   ├── smtp_connector.py             # SMTP (envío - FUNCIONAL)
│   ├── powerautomate_connector.py    # Lee JSON de OneDrive + SMTP
│   ├── graph_connector.py            # Microsoft Graph API (requiere admin)
│   └── imap_connector.py            # IMAP (bloqueado en M365)
├── analyzers/
│   ├── __init__.py
│   ├── support_stats.py              # Estadísticas por módulo/entidad
│   └── classifier.py                 # Clasificador de correos
├── responders/
│   ├── __init__.py
│   ├── auto_responder.py             # Motor de respuestas automáticas
│   └── templates.py                  # Templates HTML de respuesta
├── .env                              # Credenciales (gitignored)
├── .env.example                      # Template de configuración
├── requirements.txt
├── POWER_AUTOMATE_SETUP.md           # Guía de configuración Power Automate
└── README.md
```

## Resultados de pruebas de conectividad

Probado el 2026-03-09 con `buzón-compartido@entidad.gov.co`:

| Protocolo | Resultado |
|-----------|-----------|
| SMTP (smtp.office365.com:587) | LOGIN EXITOSO |
| IMAP (outlook.office365.com:993) | LOGIN failed |
| EWS (exchangelib autodiscover) | Invalid credentials |
| Graph API | Requiere admin consent |
