# Power Automate - Configuración para exportar correos

## Cómo funciona

```
Power Automate (M365)            OneDrive (sync auto)           Python (local)
┌──────────────────────┐    ┌────────────────────────┐    ┌────────────────────┐
│ Lee correos de       │    │ MailExport/            │    │ main.py lee JSON   │
│ Outlook via API      │───>│   pandora/             │───>│ del disco local    │
│ (tú ya tienes        │    │     inbox_*.json       │    │ (sin auth, sin API)│
│  permisos como       │    │     sent_*.json        │    │                    │
│  usuario)            │    │   personal/          │    │ Clasifica, genera  │
│                      │    │     inbox_*.json       │    │ estadísticas       │
│ Guarda como JSON     │    │     sent_*.json        │    │                    │
│ en OneDrive          │    │                        │    │ Responde via SMTP  │
└──────────────────────┘    └────────────────────────┘    └────────────────────┘
```

**main.py NO se conecta a ningún servidor para leer.** Solo lee archivos `.json` del disco que OneDrive sincroniza.

## Prerrequisitos

- Cuenta M365 con licencia (ya la tienes como contratista)
- Acceso a https://make.powerautomate.com (gratis con M365)
- OneDrive sincronizado en tu Mac

## Estructura de carpetas en OneDrive

```
OneDrive-UAECD/
└── MailExport/
    ├── pandora/           ← correos del buzón compartido
    │   ├── inbox_2026-03-10.json
    │   └── sent_2026-03-10.json
    └── personal/        ← correos del buzón personal
        ├── inbox_2026-03-10.json
        └── sent_2026-03-10.json
```

---

## Flujos necesarios (4 en total)

| # | Nombre | Tipo | Carpeta destino |
|---|--------|------|-----------------|
| 1 | Exportar Inbox Pandora | Programado (diario) | `/MailExport/pandora/` |
| 2 | Exportar Sent Pandora | Programado (diario) | `/MailExport/pandora/` |
| 3 | Exportar Inbox personal | Programado (diario) | `/MailExport/personal/` |
| 4 | Exportar Sent personal | Programado (diario) | `/MailExport/personal/` |

Opcionalmente: Flujo 5 "Monitor en tiempo real" para el bot.

---

## Flujo 1: Exportar Inbox Pandora (buzón compartido)

1. Ve a https://make.powerautomate.com
2. **"+ Crear"** > **"Flujo de nube programado"**
3. Nombre: `Exportar Inbox Pandora`
4. Frecuencia: **1 día**
5. Click **"Crear"**

### Acciones

**Acción 1: Inicializar variable**
- Nombre: `correos`
- Tipo: `Matriz` (Array)
- Valor: `[]`

**Acción 2: Obtener correos electrónicos (V3)**
- Carpeta: `Inbox`
- Click en **"Parámetros avanzados"** > **"Mostrar todo"**
- **Dirección de buzón original**: `buzón-compartido@entidad.gov.co`
- Acceder solo a los mensajes no leídos: `No`
- Incluir datos adjuntos: `No`
- Superior: `200`
- (Los demás filtros déjalos vacíos)

> **IMPORTANTE**: "Dirección de buzón original" es lo que hace que lea
> del buzón compartido en vez de tu buzón personal.

**Acción 3: Aplicar a cada uno**
- Seleccionar salida: click en `body/value` de "Obtener correos electrónicos (V3)"
- Dentro, agregar: **"Anexar a variable de matriz"**
  - Nombre: `correos`
  - Valor: click en "Vista de código" del campo valor y pegar:

```json
{
  "id": "@{items('Aplicar_a_cada_uno')?['id']}",
  "subject": "@{items('Aplicar_a_cada_uno')?['subject']}",
  "from": "@{items('Aplicar_a_cada_uno')?['from']}",
  "from_name": "@{items('Aplicar_a_cada_uno')?['from']}",
  "to": "@{items('Aplicar_a_cada_uno')?['toRecipients']}",
  "date": "@{items('Aplicar_a_cada_uno')?['receivedDateTime']}",
  "body": "@{items('Aplicar_a_cada_uno')?['body']}",
  "is_read": @{items('Aplicar_a_cada_uno')?['isRead']},
  "has_attachments": @{items('Aplicar_a_cada_uno')?['hasAttachments']},
  "conversation_id": "@{items('Aplicar_a_cada_uno')?['conversationId']}",
  "importance": "@{items('Aplicar_a_cada_uno')?['importance']}"
}
```

> **NOTA**: Un solo campo `body` con el cuerpo completo del correo.
> No usar `bodyPreview` (trunca a 255 chars) ni `body_html` separado.
> Python usa `body` para clasificación, estadísticas y el bot.

**Acción 4: Crear archivo (OneDrive para la Empresa)**
- Ruta de carpeta: `/MailExport/pandora`
- Nombre: `inbox_@{formatDateTime(utcNow(), 'yyyy-MM-dd')}.json`
- Contenido: seleccionar la variable `correos`

---

## Flujo 2: Exportar Sent Pandora

Idéntico al Flujo 1, con estos cambios:
- Nombre: `Exportar Sent Pandora`
- Carpeta de correos: `Sent Items`
- Dirección de buzón original: `buzón-compartido@entidad.gov.co`
- Nombre archivo: `sent_@{formatDateTime(utcNow(), 'yyyy-MM-dd')}.json`
- Ruta: `/MailExport/pandora`

---

## Flujo 3: Exportar Inbox personal

Idéntico al Flujo 1, con estos cambios:
- Nombre: `Exportar Inbox personal`
- **SIN** "Dirección de buzón original" (usa tu buzón personal directamente)
- Nombre archivo: `inbox_@{formatDateTime(utcNow(), 'yyyy-MM-dd')}.json`
- Ruta: `/MailExport/personal`

---

## Flujo 4: Exportar Sent personal

Idéntico al Flujo 3 pero:
- Nombre: `Exportar Sent personal`
- Carpeta: `Sent Items`
- Nombre archivo: `sent_@{formatDateTime(utcNow(), 'yyyy-MM-dd')}.json`
- Ruta: `/MailExport/personal`

---

## Flujo 5 (Opcional): Monitor en tiempo real para bot

Para que el bot responda correos nuevos del buzón compartido en tiempo real.

1. **"+ Crear"** > **"Flujo de nube automatizado"**
2. Trigger: **"Cuando llega un correo nuevo a un buzón compartido (V2)"**
   - Dirección de buzón original: `buzón-compartido@entidad.gov.co`
   - Carpeta: `Inbox`

**Acción: Crear archivo (OneDrive)**
- Ruta: `/MailExport/pandora`
- Nombre: `live_@{triggerOutputs()?['body/id']}.json`
- Contenido:

```json
[{
  "id": "@{triggerOutputs()?['body/id']}",
  "subject": "@{triggerOutputs()?['body/subject']}",
  "from": "@{triggerOutputs()?['body/from']}",
  "from_name": "@{triggerOutputs()?['body/from']}",
  "to": "@{triggerOutputs()?['body/toRecipients']}",
  "date": "@{triggerOutputs()?['body/receivedDateTime']}",
  "body": "@{triggerOutputs()?['body/body']}",
  "is_read": false,
  "has_attachments": @{triggerOutputs()?['body/hasAttachments']},
  "conversation_id": "@{triggerOutputs()?['body/conversationId']}"
}]
```

El conector Python lee todos los `*.json` de la carpeta, así que cada archivo
`live_*.json` se procesa automáticamente junto con los exports programados.

---

## Uso desde Python

```bash
cd mail-agent
source .venv/bin/activate

# Buzón pandora (por defecto)
python main.py test-connection
python main.py read --days 30
python main.py stats --days 30
python main.py classify --days 7

# Buzón personal (explícito)
python main.py -m personal test-connection
python main.py -m personal read --days 30
python main.py -m personal stats --days 30

# Bot de respuesta para pandora
python main.py -m pandora bot --interval 300
```

La opción `-m` (o `--mailbox`) cambia el perfil. Cada perfil apunta a su
subcarpeta de JSON y sus credenciales SMTP.

---

## Costos

- **Power Automate gratis**: Incluido con licencia M365
- **Límites gratis**: 750 ejecuciones/día
- **OneDrive**: Ya incluido, los JSON pesan KB (sin body_html)
- **No se necesita licencia Premium** (solo conectores estándar: Outlook + OneDrive)

---

## Troubleshooting

### Los archivos no aparecen en Mac
1. Verifica que OneDrive está corriendo (ícono en barra de menú)
2. Verifica la carpeta en OneDrive web: https://uaecd-my.sharepoint.com/
3. Si la sincronización está pausada, click derecho en el ícono > Reanudar

### "Dirección de buzón original" no aparece
En "Obtener correos electrónicos (V3)":
1. Click en "Parámetros avanzados"
2. Click en el dropdown "Mostrando X de 13"
3. Click en "Mostrar todo"
4. Busca "Dirección de buzón original" en la lista

### El JSON tiene formato diferente
El conector Python es flexible. Soporta:
- Array: `[{...}, {...}]`
- Respuesta cruda de Graph API con campo `value`
- Archivos individuales por correo (`live_*.json`)
