# 🔐 Panel Admin - Acceso Seguro

## Información de Acceso

**URL del Panel Admin:**
```
http://localhost:5000/admin/login
```

**Contraseña:** Guardada en `.env`

La contraseña está almacenada de forma **segura** en:
```
.env
ADMIN_PASSWORD=...
```

## Cómo Acceder

1. Ve a `/admin/login`
2. Ingresa la contraseña desde el archivo `.env`
3. Accede al panel de administración

## Seguridad

✅ La contraseña está en `.env` (ignorado en Git)
✅ No se expone en el código
✅ El link es discreto (solo emoji en navbar)
✅ Solo accesible si tienes la contraseña exacta

## Para Cambiar la Contraseña

Edita el archivo `.env`:
```
ADMIN_PASSWORD=tu_nueva_contraseña_aqui
```

Luego reinicia la aplicación.

---

**IMPORTANTE:** No compartas el archivo `.env` públicamente. Mantén tu contraseña segura.
