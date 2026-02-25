import os
import psutil
import json
import time
import socket
import logging
import requests
from datetime import datetime
from dotenv import load_dotenv

# --- METADATOS DEL SCRIPT ---
__version__ = "1.0.0"
__author__ = "Dev"

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
load_dotenv()

class SecurityAgent:
    """
    Agente encargado de la recolección de telemetría y seguridad.
    """

    def __init__(self, config_path="config.json"):
        self.hostname = socket.gethostname()
        self.api_url = os.getenv('API_URL')
        self.api_key = os.getenv('API_KEY')
        self.config = self._load_config(config_path)
        self.local_ip = self._get_internal_ip()

    def _load_config(self, path):
        """Carga servicios a monitorear desde un archivo externo."""
        try:
            with open(path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            # Lista genérica por defecto si no hay config.json
            return {"monitored_services": ["sshd", "nginx", "mysql"]}

    def _get_internal_ip(self):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.connect(("8.8.8.8", 80))
                return s.getsockname()[0]
        except Exception:
            return "127.0.0.1"

    def _get_security_metrics(self):
        """Analiza conexiones de red y usuarios activos."""
        connections = []
        for conn in psutil.net_connections(kind='inet'):
            if conn.status == 'ESTABLISHED' and conn.raddr:
                if conn.raddr.ip != '127.0.0.1':
                    connections.append({
                        "remote": f"{conn.raddr.ip}:{conn.raddr.port}",
                        "pid": conn.pid
                    })
        
        return {
            "active_connections": connections,
            "logged_users": [u.name for u in psutil.users()]
        }

    def collect_and_send(self):
        """Construye el payload y lo transmite a la API."""
        payload = {
            "version": __version__,
            "host": self.hostname,
            "ip": self.local_ip,
            "timestamp": datetime.utcnow().isoformat(),
            "security": self._get_security_metrics(),
            "resources": {
                "cpu": psutil.cpu_percent(),
                "ram": psutil.virtual_memory().percent
            }
        }

        if not self.api_url:
            # Si no hay API, mostramos el JSON en consola para debug
            print(json.dumps(payload, indent=2))
            return

        try:
            headers = {"Authorization": f"Bearer {self.api_key}"}
            response = requests.post(self.api_url, json=payload, headers=headers, timeout=10)
            logging.info(f"Datos enviados. Status: {response.status_code}")
        except Exception as e:
            logging.error(f"Error de conexión: {e}")

    def run(self, interval=60):
        logging.info(f"Agente v{__version__} iniciado.")
        while True:
            self.collect_and_send()
            time.sleep(interval)

if __name__ == "__main__":
    agent = SecurityAgent()
    agent.run(interval=30)
