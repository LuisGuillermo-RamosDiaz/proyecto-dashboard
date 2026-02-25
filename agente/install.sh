#!/bin/bash

# Colores para la terminal
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}Iniciando instalación del Agente de Seguridad...${NC}"

# 1. Verificar si es root
if [ "$EUID" -ne 0 ]; then 
  echo -e "${RED}Por favor, ejecuta el script con sudo.${NC}"
  exit
fi

# 2. Definir rutas (seguridad-agente se cambiara a futuro por otro nombre)
INSTALL_DIR="/opt/seguridad-agente"
echo -e "[*] Creando directorio en $INSTALL_DIR..."
mkdir -p $INSTALL_DIR

# 3. Copiar archivos del proyecto
cp -r ./* $INSTALL_DIR/

# 4. Instalar dependencias del sistema
echo -e "[*] Instalando dependencias del sistema (Python3)..."
apt update && apt install -y python3-pip python3-venv

# 5. Crear entorno virtual
echo -e "[*] Configurando entorno virtual de Python..."
python3 -m venv $INSTALL_DIR/venv
$INSTALL_DIR/venv/bin/pip install --upgrade pip
$INSTALL_DIR/venv/bin/pip install -r $INSTALL_DIR/requirements.txt

# Crear el archivo .env de forma interactiva
echo -e "[*] Configurando variables de entorno..."
read -p "Introduce la URL de la API: " api_url
read -p "Introduce la API_KEY del cliente: " api_key

echo "API_URL=$api_url" > $INSTALL_DIR/.env
echo "API_KEY=$api_key" >> $INSTALL_DIR/.env
chown root:root $INSTALL_DIR/.env
chmod 600 $INSTALL_DIR/.env

# 6. Crear el archivo de servicio para Systemd
SERVICE_FILE="/etc/systemd/system/agente-seguridad.service"
echo -e "[*] Configurando servicio de sistema..."

cat <<EOF > $SERVICE_FILE
[Unit]
Description=Agente de Monitoreo de Seguridad e Infraestructura
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=$INSTALL_DIR
ExecStart=$INSTALL_DIR/venv/bin/python $INSTALL_DIR/monitor.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# 7. Activar el servicio
echo -e "[*] Recargando servicios y activando el agente..."
systemctl daemon-reload
systemctl enable agente-seguridad
systemctl start agente-seguridad

echo -e "${GREEN}¡Instalación completada con éxito!${NC}"
echo -e "El agente está corriendo en segundo plano."
echo -e "Puedes ver los logs con: ${GREEN}journalctl -u agente-seguridad -f${NC}"
