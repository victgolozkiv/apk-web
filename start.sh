#!/bin/bash

# Script para iniciar MisAPKs

echo "📱 Iniciando MisAPKs..."
echo ""

# Verificar si existe venv
if [ ! -d "venv" ]; then
    echo "📦 Creando entorno virtual..."
    python3 -m venv venv
fi

echo "🔄 Activando entorno virtual..."
source venv/bin/activate

echo "📥 Instalando dependencias..."
pip install -r requirements.txt > /dev/null 2>&1

echo ""
echo "✅ ¡Todo listo!"
echo ""
echo "🚀 Iniciando servidor..."
echo "🌐 Abre tu navegador en: http://localhost:5000"
echo "👤 Usuario: admin"
echo "🔐 Contraseña: admin123"
echo ""
echo "Presiona Ctrl+C para detener el servidor."
echo ""

python run.py
