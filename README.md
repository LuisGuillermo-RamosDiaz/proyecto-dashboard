# Plataforma web multiempresa para el monitoreo de servidores y la detección automática de incidentes de ciberseguridad

Sistema integral diseñado para la recolección de telemetría, análisis de salud de infraestructura y alertamiento temprano ante anomalías de red. La arquitectura se basa en un modelo de agentes distribuidos que reportan a un nodo central de monitoreo.

## Estructura del Repositorio (Monorepo)

La organización de archivos se divide por responsabilidades técnicas para evitar conflictos en el despliegue:

* **`/agente`**: Código fuente del recolector en Python, entorno virtual y script de instalación automatizada.
* **`/backend`**: Directorio para la implementación del servidor de API y lógica de negocio.
* **`/frontend`**: Espacio para la interfaz de usuario y visualización de datos.
* **`/database`**: Definición del esquema relacional y procedimientos iniciales.

---

## 🔧 Especificaciones por Área

### 1. Área de Base de Datos (DB)
Se debe asegurar la integridad del esquema antes de cualquier prueba de conexión.
* **Tarea**: Ejecutar el archivo `database/init.sql` para crear la estructura de tablas requerida.
* **Ambiente local**: Utilizar el archivo `docker-compose.yml` localizado en la raíz para levantar la instancia de MySQL.
* **Parámetros de conexión**:
    * **Host**: `localhost` (Puerto externo: `3308`).
    * **Usuario**: `db_admin`.
    * **Base de datos**: `dashboard_db`.
    * **Gestión**: Acceso vía phpMyAdmin en `http://localhost:8081`.

### 2. Área de Backend (API)
El servidor debe funcionar como puente entre el agente y la persistencia de datos.
* **Tarea**: Desarrollar un endpoint de tipo **POST** que reciba el JSON de telemetría.
* **Seguridad**: Implementar validación obligatoria del encabezado `Authorization: Bearer <API_KEY>`.
* **Procesamiento**: El agente enviará datos de CPU, RAM e incidentes de red; estos deben ser mapeados a la tabla `metrics` o similar definida en el esquema.
* **Configuración**: Utilizar `backend/.env.example` como base para las variables de entorno.

### 3. Área de Frontend (Dashboard)
Desarrollo de la capa de presentación para el cliente final.
* **Tarea**: Implementar el panel de control utilizando la tecnología definida (React Native/Web).
* **Visualización**: Consumir los datos históricos de la base de datos para generar gráficas de rendimiento y listados de alertas de seguridad detectadas por el agente.
* **Estructura**: El código debe alojarse exclusivamente dentro del directorio `/frontend`.

---

## 🛡️4. espliegue del Agente (DevOps)

El agente de seguridad se despliega mediante un script interactivo que garantiza la persistencia como servicio del sistema.

**Instrucciones de instalación:**
1.  Acceder al servidor objetivo.
2.  Ejecutar el instalador: `sudo ./agente/install.sh`.
3.  Proporcionar la **URL de la API** y la **API_KEY** cuando el script lo solicite.

El script creará un archivo `.env` restringido (permisos `600`) y activará un servicio en `systemd` que se reiniciará automáticamente ante fallos.

---
