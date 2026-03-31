# ✅ Checklist de Seguridad para Producción

## ANTES DE DESPLEGAR

- [ ] Cambiar `SECRET_KEY` en `.env` (ejecutar: `python3 -c "import secrets; print(secrets.token_urlsafe(32))"`)
- [ ] Cambiar `ADMIN_PASSWORD` en `.env` (contraseña unica y fuerte)
- [ ] Crear carpeta `logs/` con permisos 700
- [ ] Crear carpeta `uploads/` con permisos 700
- [ ] Hacer `.env` read-only: `chmod 600 .env`
- [ ] Agregar `.env` a `.gitignore` (ya está agregado)

## DESPLIEGUE EN SERVIDOR

- [ ] HTTPS habilitado con SSL válido (Let's Encrypt)
- [ ] Nginx configurado como reverse proxy
- [ ] Gunicorn ejecutándose con múltiples workers
- [ ] Firewall habilitado: `sudo ufw enable`
- [ ] Puerto SSH cambiar a no-estándar (ej: 2222)
- [ ] SSH keys configuradas, sin password login

## SEGURIDAD DE APLICACIÓN

✅ **YA IMPLEMENTADO:**
- [x] Contraseña admin segura (~200 caracteres)
- [x] Protección contra fuerza bruta (máximo 2 intentos)
- [x] Logging de intentos fallidos
- [x] Headers de seguridad HTTP (HSTS, X-Frame-Options, CSP, etc)
- [x] CSRF protection (Flask-WTF)
- [x] Session management seguro (HTTPONLY, SAMESITE=Strict)
- [x] Validación de archivos (extensión, tamaño, nombre)
- [x] Límite de tamaño (500 MB)
- [x] Acceso admin oculto (sin enlace visible)
- [x] Configuración en `.env` (no en código)

## MONITOREO CONTINUO

- [ ] Revisar logs de seguridad regularmente: `tail -f logs/security.log`
- [ ] Monitorear uso de disk: `df -h uploads/`
- [ ] Configurar alertas de errores
- [ ] Backups diarios de `/uploads` y `apks.json`
- [ ] Rotación de logs (limpiar cada 30 días)

## MANTENIMIENTO

- [ ] Actualizar dependencias cada mes: `pip list --outdated`
- [ ] Cambiar contraseña admin cada 6 meses
- [ ] Revisar archivos de logs para actividad sospechosa
- [ ] Validar certificado SSL expira: `certbot certificates`
- [ ] Testear procesos de recuperación de backup mensualmente

## ENDPOINTS PÚBLICOS

- `GET /` - Tienda pública (lista de APKs)
- `GET /download/<id>` - Descargar APK (público)

## ENDPOINTS ADMIN (PROTEGIDOS)

- `GET/POST /admin/login` - Login (protegido por contraseña)
- `GET /admin` - Panel admin (requiere sesión)
- `POST /upload` - Subir APK (requiere sesión)
- `GET /delete/<id>` - Eliminar APK (requiere sesión)
- `GET /admin/logout` - Cerrar sesión

## RESPUESTA A INCIDENTES

### Si se compromete la contraseña:
1. Cambiar en `.env`
2. Reiniciar aplicación: `sudo systemctl restart apks-store`
3. Revisar logs: `grep FAILED_ADMIN_LOGIN logs/security.log`
4. Exportar/validar todos los APKs subidos recientemente

### Si detectas acceso no autorizado:
1. Detener la aplicación: `sudo systemctl stop apks-store`
2. Crear backup: `tar -czf emergency-backup.tar.gz uploads/ apks.json`
3. Revisar logs de acceso
4. Cambiar credenciales y actualizar en `.env`
5. Reiniciar: `sudo systemctl start apks-store`

---

**Última revisión:** 30 de Marzo de 2026
**Versión de seguridad:** 1.0
