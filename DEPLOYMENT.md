# 🚀 Guía de Despliegue en Producción

## Pre-requisitos
- Servidor con Linux (Ubuntu 20.04+ recomendado)
- Python 3.8+
- Dominio propio
- SSH access

## Paso 1: Instalación del Servidor

### 1.1 Preparar el servidor
```bash
# Actualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar dependencias
sudo apt install -y python3-pip python3-venv nginx certbot python3-certbot-nginx supervisor git
```

### 1.2 Clonar el proyecto
```bash
cd /home/usuario
git clone <tu-repo-aqui> apks-store
cd apks-store
```

### 1.3 Crear entorno virtual
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Paso 2: Configuración de Seguridad

### 2.1 Editar archivo `.env` **IMPORTANTE**
```bash
nano .env
```

Reemplazar:
```
SECRET_KEY=<genera-una-clave-nueva-segura>
ADMIN_PASSWORD=<tu-contraseña-segura>
```

Para generar claves seguras:
```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 2.2 Permisos de archivos
```bash
chmod 600 .env
chmod 700 logs/
chmod 700 uploads/
```

## Paso 3: Configuración de NGINX

### 3.1 Crear archivo de configuración
```bash
sudo nano /etc/nginx/sites-available/apks-store
```

**Contenido:**
```nginx
server {
    server_name tu-dominio.com;
    
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    location /uploads {
        alias /home/usuario/apks-store/uploads;
        expires 30d;
    }
}
```

### 3.2 Habilitar sitio
```bash
sudo ln -s /etc/nginx/sites-available/apks-store /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## Paso 4: SSL/HTTPS con Let's Encrypt

```bash
sudo certbot --nginx -d tu-dominio.com
sudo systemctl enable certbot.timer
```

## Paso 5: Ejecutar la aplicación con Gunicorn

### 5.1 Instalar Gunicorn
```bash
pip install gunicorn
```

### 5.2 Crear archivo de servicio
```bash
sudo nano /etc/systemd/system/apks-store.service
```

**Contenido:**
```ini
[Unit]
Description=APK Store Flask Application
After=network.target

[Service]
User=www-data
WorkingDirectory=/home/usuario/apks-store
Environment="PATH=/home/usuario/apks-store/venv/bin"
ExecStart=/home/usuario/apks-store/venv/bin/gunicorn --workers 4 --bind 127.0.0.1:5000 run:app
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### 5.3 Iniciar servicio
```bash
sudo systemctl daemon-reload
sudo systemctl start apks-store
sudo systemctl enable apks-store
```

## Paso 6: Monitoreo y Logs

### Ver logs
```bash
sudo journalctl -u apks-store -f
tail -f logs/security.log
```

### Status
```bash
sudo systemctl status apks-store
```

## Seguridad en Producción

✅ **Lo que hemos configurado:**
- HTTPS/SSL con certificado válido
- Headers de seguridad HTTP
- Contraseña fuerte para admin
- Protección contra fuerza bruta
- Logging de intentos fallidos
- Archivo `.env` protegido
- Rate limiting
- CSRF protection

⚠️ **Recomendaciones adicionales:**
- Configurar backups automáticos de `/uploads`
- Monitorear logs regularmente
- Actualizar dependencias regularmente: `pip list --outdated`
- Usar un firewall: `sudo ufw enable`
- Limpiar logs old: `find logs -mtime +30 -delete`

## Restaurar desde backup

```bash
# Backup de APKs
tar -czf backup-apks-$(date +%Y%m%d).tar.gz uploads/

# Backup de DB
cp apks.json backups/apks-$(date +%Y%m%d).json
```

## Troubleshooting

### Error: Port 5000 already in use
```bash
lsof -i :5000
kill -9 <PID>
```

### Error: Permission denied
```bash
sudo chown -R www-data:www-data /home/usuario/apks-store
chmod 755 /home/usuario/apks-store
```

### HTTPS no funciona
```bash
sudo certbot renew --dry-run
sudo systemctl restart nginx
```

---

**¿Preguntas?** Revisa los logs:
```bash
sudo journalctl -u apks-store -n 100
```
