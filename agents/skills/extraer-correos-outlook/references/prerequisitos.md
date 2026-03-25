# Prerequisitos — Outlook MCP (Azure AD)

Requieren accion del admin de IT de la entidad.

## Pasos

1. Registro de aplicacion en Azure AD del tenant de la entidad
2. Permisos delegados: `Mail.Read`
3. Admin consent otorgado

## Variables en `.env`

```
{ENTIDAD}_TENANT_ID=<tenant-id>
{ENTIDAD}_CLIENT_ID=<client-id>
{ENTIDAD}_CLIENT_SECRET=<client-secret>
```

## Troubleshooting

- Si Azure AD no es viable (IT no coopera): informar al usuario que debe mantener el flujo manual de exportar PDF desde Outlook. El fallback en `generar-soportes-correo` se encargara de buscar el PDF.
