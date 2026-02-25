#Proyecto de Monitoreo

Repositorio central para la infraestructura, agente de monitoreo y despliegue del Dashboard de Seguridad.

## Guía de Inicio Rápido (Para el Equipo de Desarrollo)

### Requisitos previos
1. Tener instalado [Docker Desktop](https://www.docker.com/products/docker-desktop/).
2. Clonar este repositorio en tu computadora.

### ¿Cómo levantar la Base de Datos Local?
Abre tu terminal en la carpeta principal de este proyecto y ejecuta:
`docker-compose up -d`

**Credenciales locales (no de producción) para conectar el Backend: **
* **Host:** `localhost`
* **Puerto:** `3308` (Mapeado al 3306 interno)
* **Usuario:** `db_admin`
* **Contraseña:** `9f8c7b6A5!2d#4`
* **Base de datos:** `dashboard_db`

**Visualizar la BD graficamente: **
Entra en tu navegador a: `http://localhost:8081`
* **Usuario:** `root`
* **Contraseña:** `9f8c7b6A5!2d#4`
