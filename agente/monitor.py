import psutil
import json
import time
import socket
# import requests # Descomentar cuando la API exista

# Configuraciones base
SERVER_NAME = socket.gethostname()
API_URL = "http://localhost:8080/api/metricas"
API_KEY = "sk_prod_9f8c7b6A52d4_monitor" # Llave de seguridad simulada

# Lista de servicios críticos que queremos vigilar
SERVICIOS_CLAVE = ["mysql", "docker", "nginx", "sshd", "apache2"]

def verificar_servicios():
    """Verifica si los procesos críticos están corriendo"""
    estado_servicios = {servicio: False for servicio in SERVICIOS_CLAVE}
    
    # Iterar sobre todos los procesos activos de forma ligera
    for proc in psutil.process_iter(['name']):
        try:
            nombre_proceso = proc.info['name'].lower()
            for servicio in SERVICIOS_CLAVE:
                # Si el nombre del proceso contiene nuestra palabra clave, está activo
                if servicio in nombre_proceso:
                    estado_servicios[servicio] = True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
            
    return estado_servicios

def recolectar_metricas():
    # 1. Recolectar salud general
    uso_cpu = psutil.cpu_percent(interval=1)
    uso_ram = psutil.virtual_memory().percent
    
    # 2. Recolectar estado de servicios
    servicios_activos = verificar_servicios()
    
    # 3. Empaquetar todo en el JSON
    payload = {
        "servidor": SERVER_NAME,
        "cpu_percent": uso_cpu,
        "ram_percent": uso_ram,
        "servicios": servicios_activos,
        "timestamp": time.time()
    }
    
    print("\n[+] Métricas recolectadas:")
    print(json.dumps(payload, indent=2))
    
    # --- LA PARTE DE SEGURIDAD (Lista para tu Backend) ---
    # headers = {
    #     "Authorization": f"Bearer {API_KEY}",
    #     "Content-Type": "application/json"
    # }
    
    # try:
    #     response = requests.post(API_URL, json=payload, headers=headers)
    #     if response.status_code == 200 or response.status_code == 201:
    #         print("[OK] Datos enviados con éxito al SOC.")
    #     else:
    #         print(f"[ERROR] El servidor rechazó los datos. Código: {response.status_code}")
    # except Exception as e:
    #     print("[!] Error de conexión:", e)

if __name__ == "__main__":
    print(f"Iniciando Agente de Seguridad AegisOps en [{SERVER_NAME}]...")
    print("Modo: Transmisión segura activada (Push)")
    
    while True:
        recolectar_metricas()
        time.sleep(10)
