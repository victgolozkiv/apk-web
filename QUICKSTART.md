# ⚡ QUICKSTART - APK Manager

## 🚀 Comienza en 30 segundos

### 1️⃣ Instalar (primera vez)
```bash
cd "/home/victor/Escritorio/pagina-web de mis apks"
source venv/bin/activate
pip install -r requirements.txt
```

### 2️⃣ Configurar (primera vez)
```bash
# Generar clave segura
python -c "import secrets; print(secrets.token_hex(32))"

# Copiar resultado y crear .env
cp .env.example .env
nano .env  # Pega la clave en SECRET_KEY=
```

### 3️⃣ Ejecutar
```bash
python run.py
```

### 4️⃣ Acceder
- **URL:** http://localhost:5000
- **Usuario:** admin
- **Contraseña:** admin123

---

## 📱 ¿Qué puedo hacer?

✅ **Subir APKs** - Botón "🚀 Subir APK"  
✅ **Descargar** - Botón "⬇️ Descargar"  
✅ **Eliminar** - Botón "🗑️ Eliminar"  
✅ **Ver descargas** - Contador en tabla  

---

## 🔧 Cambiar Contraseña

```bash
# Generar hash
python -c "from werkzeug.security import generate_password_hash; print(generate_password_hash('MiNuevaPass123'))"

# Editar users.json, copiar hash en admin.password
nano users.json
```

---

## ⚠️ IMPORTANTE

1. **Cambiar contraseña admin** (no uses admin123)
2. **Generar SECRET_KEY** (ver paso 2)
3. **Hacer backup** de users.json y apks.json
4. **Usar HTTPS** en producción

---

## 🆘 Problemas Comunes

**Puerto 5000 en uso:**
```bash
# Editar run.py y cambiar port=5001
```

**Error de módulo:**
```bash
pip install -r requirements.txt
```

**Permisos en uploads:**
```bash
chmod -R 755 uploads/
```

---

## 📚 Documentación Completa

Ver `README.md` para configuración avanzada.

---

**¡Listo! Ya puedes subir tus APKs de forma segura! 🔒📱**
todo se hizo con IA
