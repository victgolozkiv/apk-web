from flask import Blueprint, render_template, request, redirect, url_for, session, send_from_directory, flash, current_app
import os
from werkzeug.utils import secure_filename
from app.utils import (
    init_data_files, load_apks, authenticate_user,
    add_apk, delete_apk, increment_download, login_required, change_password
)
import mimetypes
from functools import wraps
from dotenv import load_dotenv
from app.security import log_failed_login, log_file_upload, log_file_delete, get_client_ip

load_dotenv()

bp = Blueprint('main', __name__)

ALLOWED_EXTENSIONS = {'apk'}
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'admin123')  # Se carga desde .env

def admin_required(f):
    """Verificar que el usuario está en sesión admin"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('admin_logged'):
            flash('❌ Acceso denegado. Por favor inicia sesión en admin.', 'error')
            return redirect(url_for('main.admin_login'))
        return f(*args, **kwargs)
    return decorated_function

def allowed_file(filename):
    """Validar que sea un archivo APK"""
    if '.' not in filename:
        return False
    ext = filename.rsplit('.', 1)[1].lower()
    return ext in ALLOWED_EXTENSIONS

@bp.route('/')
def index():
    """Tienda pública - Ver y descargar APKs"""
    apks = load_apks()
    return render_template('shop.html', apks=apks)

@bp.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    """Login admin para acceder al panel de subida - Protección contra fuerza bruta"""
    # Contar intentos fallidos
    intentos = session.get('admin_login_attempts', 0)
    bloqueado = session.get('admin_blocked', False)
    client_ip = get_client_ip()
    
    if bloqueado:
        flash('🚫 Acceso bloqueado. Demasiados intentos fallidos. Intenta más tarde.', 'error')
        return render_template('admin_login.html', bloqueado=True)
    
    if request.method == 'POST':
        password = request.form.get('password', '')
        
        if password == ADMIN_PASSWORD:
            session['admin_logged'] = True
            session['admin_login_attempts'] = 0  # Reset intentos
            session['admin_blocked'] = False
            flash('✅ Acceso al panel admin concedido', 'success')
            return redirect(url_for('main.admin_panel'))
        else:
            # Registrar intento fallido
            log_failed_login(client_ip, '*' * len(password))
            
            # Incrementar intentos fallidos
            intentos += 1
            session['admin_login_attempts'] = intentos
            
            if intentos >= 2:
                session['admin_blocked'] = True
                flash('🚫 ¡BLOQUEADO! 2 intentos fallidos. Tu IP ha sido bloqueada.', 'error')
                return render_template('admin_login.html', bloqueado=True)
            else:
                flash(f'❌ Contraseña incorrecta. Intentos restantes: {2 - intentos}', 'error')
    
    return render_template('admin_login.html', bloqueado=False)

@bp.route('/admin')
@admin_required
def admin_panel():
    """Panel de administración - Subir y gestionar APKs"""
    apks = load_apks()
    return render_template('admin_panel.html', apks=apks)

@bp.route('/dashboard')
def dashboard():
    """Redirige a la tienda pública"""
    return redirect(url_for('main.index'))

@bp.route('/upload', methods=['POST'])
@admin_required
def upload():
    """Subir nuevo APK con validación mejorada y logging"""
    client_ip = get_client_ip()
    
    if 'file' not in request.files:
        flash('❌ Archivo no seleccionado', 'error')
        return redirect(url_for('main.admin_panel'))
    
    file = request.files['file']
    app_name = request.form.get('app_name', '').strip()
    description = request.form.get('description', '').strip()
    version = request.form.get('version', '').strip()
    
    # Validaciones
    if not app_name or not version:
        flash('❌ Nombre de app y versión son requeridos', 'error')
        return redirect(url_for('main.admin_panel'))
    
    if file.filename == '':
        flash('❌ Selecciona un archivo', 'error')
        return redirect(url_for('main.admin_panel'))
    
    # Validar nombre de archivo
    if len(file.filename) > 255:
        flash('❌ El nombre del archivo es demasiado largo', 'error')
        return redirect(url_for('main.admin_panel'))
    
    if not allowed_file(file.filename):
        flash('❌ Solo se permiten archivos .apk', 'error')
        return redirect(url_for('main.admin_panel'))
    
    # Validar tamaño
    file.seek(0, os.SEEK_END)
    file_size = file.tell()
    file.seek(0)
    
    if file_size == 0:
        flash('❌ El archivo está vacío', 'error')
        return redirect(url_for('main.admin_panel'))
    
    if file_size > 500 * 1024 * 1024:  # 500 MB
        flash('❌ El archivo excede el límite de 500 MB', 'error')
        return redirect(url_for('main.admin_panel'))
    
    # Guardar archivo
    try:
        filename = secure_filename(file.filename)
        import time
        filename = f"{int(time.time())}_{filename}"
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Agregar a la lista
        add_apk(filename, description, version, app_name)
        
        # Registrar subida
        log_file_upload(filename, file_size, client_ip)
        flash(f'✅ APK "{app_name}" subido correctamente', 'success')
    except Exception as e:
        flash(f'❌ Error al subir archivo: {str(e)}', 'error')
    
    return redirect(url_for('main.admin_panel'))

@bp.route('/delete/<int:apk_id>')
@admin_required
def delete(apk_id):
    """Eliminar APK"""
    client_ip = get_client_ip()
    apks = load_apks()
    apk_to_delete = next((apk for apk in apks if apk['id'] == apk_id), None)
    
    if apk_to_delete:
        try:
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], apk_to_delete['filename'])
            if os.path.exists(filepath):
                os.remove(filepath)
            delete_apk(apk_id)
            
            # Registrar eliminación
            log_file_delete(apk_to_delete['filename'], client_ip)
            flash(f'✅ APK eliminado correctamente', 'success')
        except Exception as e:
            flash(f'❌ Error al eliminar: {str(e)}', 'error')
    else:
        flash('❌ APK no encontrado', 'error')
    
    return redirect(url_for('main.admin_panel'))

@bp.route('/download/<int:apk_id>')
def download(apk_id):
    """Descargar APK - acceso público"""
    apks = load_apks()
    apk = next((apk for apk in apks if apk['id'] == apk_id), None)
    
    if apk:
        increment_download(apk_id)
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], apk['filename'])
        
        if os.path.exists(filepath):
            return send_from_directory(current_app.config['UPLOAD_FOLDER'], apk['filename'])
    
    flash('❌ Archivo no encontrado', 'error')
    return redirect(url_for('main.index'))

@bp.route('/admin/logout')
def admin_logout():
    """Cerrar sesión admin"""
    session.pop('admin_logged', None)
    flash('✅ Sesión admin cerrada', 'success')
    return redirect(url_for('main.index'))

@bp.route('/login', methods=['GET', 'POST'])
def login():
    """Redirige al admin login"""
    return redirect(url_for('main.admin_login'))

@bp.route('/logout')
def logout():
    """Redirect to admin logout"""
    return redirect(url_for('main.admin_logout'))
