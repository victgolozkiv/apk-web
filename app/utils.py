import json
import os
from datetime import datetime
from functools import wraps
from flask import session, redirect, url_for
from werkzeug.security import check_password_hash, generate_password_hash

USERS_FILE = 'users.json'
APKS_FILE = 'apks.json'

def init_data_files():
    """Inicializar archivos JSON si no existen"""
    if not os.path.exists(USERS_FILE):
        # Crear usuario admin con contraseña hasheada
        default_users = {
            "admin": {
                "password": generate_password_hash("admin123"),
                "username": "admin"
            }
        }
        with open(USERS_FILE, 'w') as f:
            json.dump(default_users, f, indent=2)
        print("✅ Usuario admin creado. Contraseña: admin123")
        print("⚠️  CAMBIAR CONTRASEÑA AL INICIAR: http://localhost:5000")
    
    if not os.path.exists(APKS_FILE):
        with open(APKS_FILE, 'w') as f:
            json.dump([], f)

def load_users():
    """Cargar usuarios desde JSON"""
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, 'r') as f:
        return json.load(f)

def save_users(users):
    """Guardar usuarios en JSON"""
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=2)

def load_apks():
    """Cargar APKs desde JSON"""
    if not os.path.exists(APKS_FILE):
        return []
    with open(APKS_FILE, 'r') as f:
        return json.load(f)

def save_apks(apks):
    """Guardar APKs en JSON"""
    with open(APKS_FILE, 'w') as f:
        json.dump(apks, f, indent=2)

def login_required(f):
    """Decorador para rutas que necesitan autenticación"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('main.login'))
        return f(*args, **kwargs)
    return decorated_function

def authenticate_user(username, password):
    """Verificar credenciales del usuario con hash"""
    users = load_users()
    if username in users:
        user = users[username]
        if check_password_hash(user['password'], password):
            return True
    return False

def change_password(username, new_password):
    """Cambiar contraseña del usuario"""
    users = load_users()
    if username in users:
        users[username]['password'] = generate_password_hash(new_password)
        save_users(users)
        return True
    return False

def add_apk(filename, description, version, app_name):
    """Agregar nuevo APK a la lista"""
    apks = load_apks()
    apk = {
        "id": len(apks) + 1,
        "filename": filename,
        "app_name": app_name,
        "description": description,
        "version": version,
        "upload_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "downloads": 0
    }
    apks.append(apk)
    save_apks(apks)
    return apk

def delete_apk(apk_id):
    """Eliminar APK"""
    apks = load_apks()
    apks = [apk for apk in apks if apk['id'] != apk_id]
    save_apks(apks)

def increment_download(apk_id):
    """Incrementar contador de descargas"""
    apks = load_apks()
    for apk in apks:
        if apk['id'] == apk_id:
            apk['downloads'] += 1
            break
    save_apks(apks)
