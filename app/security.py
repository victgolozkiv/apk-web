import logging
import os
from datetime import datetime
from flask import request, g

# Configurar logging de seguridad
security_logger = logging.getLogger('security')
handler = logging.FileHandler('logs/security.log')
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
security_logger.addHandler(handler)
security_logger.setLevel(logging.WARNING)

def log_failed_login(ip, password_attempt):
    """Registrar intentos fallidos de login admin"""
    security_logger.warning(f'FAILED_ADMIN_LOGIN - IP: {ip} - Time: {datetime.now()}')

def log_file_upload(filename, size, user_ip):
    """Registrar subidas de archivos"""
    security_logger.info(f'FILE_UPLOADED - {filename} ({size} bytes) - IP: {user_ip}')

def log_file_delete(filename, user_ip):
    """Registrar eliminación de archivos"""
    security_logger.info(f'FILE_DELETED - {filename} - IP: {user_ip}')

def get_client_ip():
    """Obtener IP real del cliente (considerando proxies)"""
    if request.environ.get('HTTP_CF_CONNECTING_IP'):
        return request.environ.get('HTTP_CF_CONNECTING_IP')
    elif request.environ.get('HTTP_X_FORWARDED_FOR'):
        return request.environ.get('HTTP_X_FORWARDED_FOR').split(',')[0]
    return request.remote_addr
