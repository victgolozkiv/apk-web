# 📱 APK Manager - Gestor Seguro de APKs

Un gestor web simple pero **seguro** para subir y gestionar tus archivos APK. Construido con Flask, diseñado para tu uso personal exclusivamente.

## 🔒 Características de Seguridad

✅ **Contraseñas Hasheadas** - Encriptación segura con Werkzeug  
✅ **Protección CSRF** - Tokens en todos los formularios  
✅ **Cookies Seguras** - HttpOnly, Secure, SameSite Lax  
✅ **Timeout de Sesión** - 1 hora de inactividad automática  
✅ **Validación Estricta** - Solo archivos .apk | 500MB máx  
✅ **Variables de Entorno** - Secretos fuera del código fuente  
✅ **Autenticación Requerida** - Todo acceso requiere login  

## 🚀 Instalación Rápida

```bash
# 1. Navegar al directorio
cd "/home/victor/Escritorio/pagina-web de mis apks"

# 2. Crear entorno virtual
python3 -m venv venv
source venv/bin/activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar secretos (IMPORTANTE)
cp .env.example .env
# Editar .env y cambiar SECRET_KEY

# 5. Ejecutar
python run.py
```

## 🔑 Generar Clave Segura

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

Copia el resultado en `.env` → `SECRET_KEY=`

## 📱 Uso

**Acceso:** http://localhost:5000  
**Usuario:** admin  
**Contraseña:** admin123

### Funcionalidades SOLO de APKs:

- ✅ Subir APKs (.apk)
- ✅ Listar archivos subidos
- ✅ Descargar APKs
- ✅ Eliminar archivos
- ✅ Contador de descargas
- ✅ Control de versiones

## 📁 Estructura

```
.
├── app/
│   ├── __init__.py          # Config Flask + CSRF
│   ├── main.py              # Rutas (login + APKs)
│   ├── utils.py             # Funciones auxiliares
│   └── templates/           # HTML
├── uploads/                 # APKs almacenados
├── users.json               # Usuarios (contraseña hasheada)
├── apks.json                # Metadata APKs
├── requirements.txt         # Dependencias
├── .env                     # Variables de entorno (NO versionar)
└── run.py                   # Ejecutable
```

## 🔐 Configuración en Producción

### 1. **Cambiar contraseña admin**

```bash
python -c "from werkzeug.security import generate_password_hash; print(generate_password_hash('MI_NUEVA_PASS'))"
```

Edita `users.json` y reemplaza el hash en `admin.password`

### 2. **Generar SECRET_KEY**

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

Actualiza en `.env` → `SECRET_KEY=`

### 3. **Usar HTTPS**
s
En producción, **siempre usar HTTPS**. Config en servidor web (Nginx/Apache):

```nginx
# Redirigir HTTP a HTTPS
server {
    listen 80;
    server_name tu-dominio.com;
    return 301 https://$server_name$request_uri;
}
```

### 4. **Variables de Entorno**

Nunca commitar `.env` con secretos. Usar en servidor:

```bash
export SECRET_KEY="tu-clave-segura"
export FLASK_ENV="production"
python run.py
```

## 🛠️ Troubleshooting

**Puerto 5000 ocupado:**
```bash
# Editar run.py y cambiar puerto
app.run(debug=False, host='0.0.0.0', port=5001)
```

**Permisos en carpeta uploads:**
```bash
chmod -R 755 uploads/
```

**Limpiar cache Python:**
```bash
find . -type d -name __pycache__ -exec rm -r {} +
```

**Error CSRF token:**
- Asegúrate que la forma incluye `{{ csrf_token() }}`
- Limpiar cookies del navegador

## 📦 Dependencias

```
Flask==2.3.3           # Framework web
Werkzeug==2.3.7        # Seguridad + hash
Flask-WTF==1.1.1       # CSRF protection
python-dotenv==1.0.0   # Variables de entorno
```

## ⚙️ Configuración Avanzada

### Cambiar tamaño máximo de archivo

En `app/__init__.py`:
```python
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * 1024  # 1 GB
```

### Cambiar timeout de sesión

En `app/__init__.py`:
```python
app.config['PERMANENT_SESSION_LIFETIME'] = 7200  # 2 horas
```

### Deshabilitar debug en producción

En `run.py`:
```python
app.run(debug=False)  # Cambiar a False
```

## 📝 Checklist de Seguridad

- [ ] Cambiar contraseña admin
- [ ] Generar NEW SECRET_KEY  
- [ ] Crear `.env` con SECRET_KEY
- [ ] Usar HTTPS en producción
- [ ] Deshabilitar DEBUG mode
- [ ] Hacer backup de `users.json` y `apks.json`
- [ ] Revisar permisos de archivos (no world-readable)
- [ ] Usar firewall para limitar acceso

## 🚀 Deploy en Producción

### Opción 1: Gunicorn + Nginx

```bash
pip install gunicorn
gunicorn --bind 0.0.0.0:8000 run:app
```

### Opción 2: Docker

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "run.py"]
```

### Opción 3: Heroku

```bash
git push heroku main
```

## 📄 License

Uso personal. Libre para modificar.

---

**Versión:** 2.0 - Solo APKs, Seguridad Mejorada  
**Última actualización:** Marzo 2026  
**Mantenedor:** Tu equipo
