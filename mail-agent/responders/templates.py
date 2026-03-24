"""
Templates de respuesta automática para el bot de correo.

Cada template recibe datos extraídos del correo y genera HTML.
Puedes personalizar los templates según las necesidades de cada entidad.
"""

from analyzers.classifier import EmailCategory

# ── Templates HTML ───────────────────────────────────────────

TEMPLATES: dict[EmailCategory, str] = {
    EmailCategory.PASSWORD_RESET: """
<p>Cordial saludo {sender_name},</p>

<p>Hemos recibido su solicitud de restablecimiento de contraseña.</p>

<p>Se ha realizado el reseteo de la contraseña para el usuario
<strong>{usuario}</strong>. La nueva contraseña temporal es:</p>

<p style="font-size: 16px; font-weight: bold; color: #2563eb;
   background: #eff6ff; padding: 10px; border-radius: 4px;">
    {nueva_password}
</p>

<p><strong>Importante:</strong></p>
<ul>
    <li>Al ingresar por primera vez, el sistema le solicitará cambiar la contraseña.</li>
    <li>La contraseña debe tener mínimo 8 caracteres, incluir mayúsculas,
        minúsculas, números y un carácter especial.</li>
    <li>Por seguridad, no comparta su contraseña con terceros.</li>
</ul>

<p>Si presenta algún inconveniente, no dude en contactarnos.</p>

<p>Cordialmente,<br>
<strong>Mesa de Ayuda - PANDORA</strong><br>
{entity}</p>
""",

    EmailCategory.USER_DATA_REQUEST: """
<p>Cordial saludo {sender_name},</p>

<p>En atención a su solicitud, a continuación se relacionan los datos
del usuario consultado:</p>

<table style="border-collapse: collapse; width: 100%; margin: 10px 0;">
    <tr style="background: #f1f5f9;">
        <td style="padding: 8px; border: 1px solid #e2e8f0; font-weight: bold;">
            Usuario
        </td>
        <td style="padding: 8px; border: 1px solid #e2e8f0;">
            {usuario}
        </td>
    </tr>
    <tr>
        <td style="padding: 8px; border: 1px solid #e2e8f0; font-weight: bold;">
            Nombre completo
        </td>
        <td style="padding: 8px; border: 1px solid #e2e8f0;">
            {nombre_completo}
        </td>
    </tr>
    <tr style="background: #f1f5f9;">
        <td style="padding: 8px; border: 1px solid #e2e8f0; font-weight: bold;">
            Correo
        </td>
        <td style="padding: 8px; border: 1px solid #e2e8f0;">
            {correo}
        </td>
    </tr>
    <tr>
        <td style="padding: 8px; border: 1px solid #e2e8f0; font-weight: bold;">
            Perfil / Rol
        </td>
        <td style="padding: 8px; border: 1px solid #e2e8f0;">
            {perfil}
        </td>
    </tr>
    <tr style="background: #f1f5f9;">
        <td style="padding: 8px; border: 1px solid #e2e8f0; font-weight: bold;">
            Estado
        </td>
        <td style="padding: 8px; border: 1px solid #e2e8f0;">
            {estado}
        </td>
    </tr>
</table>

<p>Si requiere información adicional o alguna modificación, por favor
indíquenos.</p>

<p>Cordialmente,<br>
<strong>Mesa de Ayuda - PANDORA</strong><br>
{entity}</p>
""",

    EmailCategory.BUG_REPORT: """
<p>Cordial saludo {sender_name},</p>

<p>Hemos recibido su reporte y lo hemos registrado con el siguiente detalle:</p>

<ul>
    <li><strong>Módulo afectado:</strong> {modulo}</li>
    <li><strong>Descripción:</strong> {descripcion}</li>
    <li><strong>Estado:</strong> En revisión</li>
</ul>

<p>Para agilizar la atención, le solicitamos amablemente:</p>
<ol>
    <li>Capturas de pantalla del error</li>
    <li>Pasos exactos para reproducir el problema</li>
    <li>Navegador y sistema operativo utilizados</li>
</ol>

<p>Le informaremos una vez se tenga la solución.</p>

<p>Cordialmente,<br>
<strong>Mesa de Ayuda - PANDORA</strong><br>
{entity}</p>
""",

    EmailCategory.ACCESS_REQUEST: """
<p>Cordial saludo {sender_name},</p>

<p>Hemos recibido su solicitud de acceso/permisos.</p>

<p>Para procesar esta solicitud requerimos:</p>
<ol>
    <li>Aprobación por escrito del jefe inmediato o supervisor del contrato</li>
    <li>Especificar el módulo y rol requerido</li>
    <li>Número de documento de identidad del usuario</li>
</ol>

<p>Una vez recibida la autorización, procederemos con la asignación
en un plazo de 1 día hábil.</p>

<p>Cordialmente,<br>
<strong>Mesa de Ayuda - PANDORA</strong><br>
{entity}</p>
""",
}


def render_template(
    category: EmailCategory,
    data: dict,
) -> str | None:
    """Renderiza un template con los datos proporcionados."""
    template = TEMPLATES.get(category)
    if not template:
        return None

    # Valores por defecto para evitar KeyError
    defaults = {
        "sender_name": "usuario",
        "usuario": "N/A",
        "nueva_password": "Temporal2025*",
        "entity": "",
        "nombre_completo": "N/A",
        "correo": "N/A",
        "perfil": "N/A",
        "estado": "Activo",
        "modulo": "Por identificar",
        "descripcion": "Reportado por correo electrónico",
    }
    defaults.update(data)

    try:
        return template.format(**defaults)
    except KeyError as e:
        print(f"⚠️ Falta variable en template: {e}")
        return template
