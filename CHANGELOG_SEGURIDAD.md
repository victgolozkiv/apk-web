# 🔒 CAMBIOS DE SEGURIDAD - APK Manager v2.0

Fecha: Marzo 2026  
Cambios realizados: Simplificación a SOLO APKs + Seguridad Mejorada

---

## ✅ Mejoras de Seguridad Implementadas

### 1. **Contraseñas Hasheadas** 🔐
- **Antes:** Contraseñas en texto plano en `users.json`
- **Ahora:** Hashing seguro con Werkzeug
- **Archivo:** `app/utils.py`
- **Impacto:** No se pueden recuperar contraseñas ni leyendo el archivo

### 2. **Protección CSRF** 🛡️
- **Antes:** Sin protección contra ataques CSRF
- **Ahora:** Tokens CSRF automáticos en formularios
- **Librería:** Flask-WTF
- **Uso:** `{{ csrf_token() }}` en formularios

### 3. **Cookies Seguras** 🍪
- **Antes:** Cookies sin protección
- **Ahora:** 
  - `SESSION_COOKIE_SECURE = True` (HTTPS)
  - `SESSION_COOKIE_HTTPONLY = True` (no accesible desde JS)
  - `SESSION_COOKIE_SAMESITE = 'Lax'` (anti-CSRF)
  
### 4. **Timeout de Sesión** ⏱️
- **Antes:** Sesiones sin límite de tiempo
- **Ahora:** `PERMANENT_SESSION_LIFETIME = 3600` (1 hora)
- **Resultado:** Sesiones se cierran automáticamente

### 5. **Variables de Entorno** 🔑
- **Antes:** `SECRET_KEY` hardcodeado en el código
- **Ahora:** Cargado de `.env` con `python-dotenv`
- **Archivo:** `.env` (NO incluido en Git)
- **Seguridad:** Secretos NO en repositorio

### 6. **Validación Estricta de Archivos** 📦
- ✅ Solo permite `.apk`
- ✅ Valida que archivo no esté vacío
- ✅ Límite 500MB por archivo
- ✅ Filename sanitizado con `secure_filename()`

### 7. **Autenticación Obligatoria** 🔑
- **Antes:** Página pública visible sin login
- **Ahora:** TODAS las rutas requieren autenticación
- **Excepto:** `/login` (POST/GET)
- **Decorador:** `@login_required`

---

## 🗑️ Funcionalidades Removidas

### Login/Register Sistema Simplificado
- ❌ Removido registro de usuarios (solo admin)
- ❌ Removido acceso público a APKs
- ❌ Removida página `index.html` pública
- ❌ Removida página `register.html`
- ✅ Solo login + dashboard privado

---

## 📁 Cambios en Archivos

### `app/__init__.py` ✏️
```python
✅ Agregado Flask-WTF para CSRF
✅ Agregado python-dotenv para .env
✅ Configuración de cookies seguras
✅ Timeout de sesión (3600 seg)
✅ Carga SECRET_KEY desde .env
```

### `app/utils.py` ✏️
```python
✅ Agregada función generate_password_hash()
✅ Agregada función check_password_hash()
✅ Removida función register_user()
✅ Contraseñas hasheadas en init_data_files()
✅ Agregada función change_password()
```

### `app/main.py` ✏️
```python
✅ Removida ruta /register
✅ Removida ruta /index pública
✅ Rera / redirige a /login
✅ Todas rutas requieren login
✅ Mejor validación de archivos
✅ Mejor manejo de errores con flash()
✅ Agregada protección CSRF en formularios
```

### `app/templates/login.html` ✏️
```html
✅ Removido enlace a registro
✅ Simplificado interfaz
✅ Mejor mensajes de seguridad
```

### `app/templates/dashboard.html` ✏️
```html
✅ Agregado {{ csrf_token() }} en formulario
✅ Mejor UI/UX
✅ Información de seguridad
✅ Contador de APKs
```

### `app/templates/base.html` ✏️
```html
✅ Mejor navbar
✅ Mejor estilos de seguridad
✅ Indicadores de sesión activa
```

### `requirements.txt` ✏️
```
Flask-WTF==1.1.1          ← NUEVA (CSRF)
python-dotenv==1.0.0      ← NUEVA (Env vars)
```

### `README.md` ✏️
```markdown
✅ Reescrito enfocado en seguridad
✅ Guía completa de instalación
✅ Checklist de seguridad
✅ Deploy en producción
```

### `.env.example` ✏️ (NUEVO)
```bash
SECRET_KEY=tu-clave-segura
DEBUG=False
FLASK_ENV=production
```

---

## 🚀 Pasos para Usar

### Instalación Inicial
```bash
cd "/home/victor/Escritorio/pagina-web de mis apks"
source venv/bin/activate
pip install -r requirements.txt
```

### Configurar Seguridad
```bash
# 1. Generar clave segura
python -c "import secrets; print(secrets.token_hex(32))"

# 2. Crear .env
cp .env.example .env

# 3. Editar .env y pegar la clave
nano .env
# Cambiar SECRET_KEY=...
```

### Cambiar Contraseña Admin
```bash
# Generar hash de nueva contraseña
python -c "from werkzeug.security import generate_password_hash; print(generate_password_hash('tuNuevaContraseña'))"

# Editar users.json y reemplazar el hash en admin.password
nano users.json
```

### Ejecutar Aplicación
```bash
python run.py
# Acceso en http://localhost:5000
```

---

## 🔒 Checklist de Seguridad ANTES de Producción

- [ ] Cambiar contraseña admin
- [ ] Generar NEW SECRET_KEY
- [ ] Crear `.env` con SECRET_KEY
- [ ] NO compartir `.env` en Git
- [ ] Usar HTTPS/SSL en producción
- [ ] Cambiar DEBUG=False
- [ ] Usar Gunicorn en lugar de Flask dev server
- [ ] Configurar firewall
- [ ] Hacer backup de users.json y apks.json

---

## 🔐 Mejoras Implementadas Resumen

| Característica | Antes | Después |
|---|---|---|
| Contraseñas | Texto plano ❌ | Hasheadas ✅ |
| CSRF | No ❌ | Sí ✅ |
| Cookies | Inseguras ❌ | Seguras ✅ |
| Sesión | Sin límite ❌ | 1 hora ✅ |
| Secretos | Hardcoded ❌ | .env ✅ |
| Registro | Público ❌ | Removido ✅ |
| Acceso | Público ❌ | Solo admin ✅ |
| Archivos | Sin validar ❌ | Validados ✅ |

---

## 📚 Referencias de Seguridad

- [Werkzeug Security](https://werkzeug.palletsprojects.com/security/)
- [Flask-WTF Documentation](https://flask-wtf.readthedocs.io/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Flask Security Best Practices](https://flask.palletsprojects.com/security/)

---

## ❓ Preguntas Frecuentes

**P: ¿Puedo agregar más usuarios?**  
R: Sí, edita `users.json` manualmente con hashes. O crea una ruta admin para hacerlo.

**P: ¿Los APKs están seguros?**  
R: Sí, solo accesibles tras login. Nombres sanitizados y validados.

**P: ¿Puedo cambiar el tamaño máximo?**  
R: Sí, en `app/__init__.py` → `MAX_CONTENT_LENGTH`

**P: ¿Necesito HTTPS?**  
R: Recomendado. En test local OK, en producción obligatorio.

**P: ¿Qué pasa si pierdo la contraseña?**  
R: Edita `users.json`, genera nuevo hash y reemplaza.

---

**¡Tu proyecto está ahora seguro y enfocado SOLO en APKs! 🔒📱**

Puedes comenzar a usarlo inmediatamente con el usuario admin/admin123.
