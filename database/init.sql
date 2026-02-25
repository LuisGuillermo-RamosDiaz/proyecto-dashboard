CREATE DATABASE IF NOT EXISTS monitor_db;
USE monitor_db;

CREATE TABLE IF NOT EXISTS metrics (
    id INT AUTO_INCREMENT PRIMARY KEY,
    hostname VARCHAR(100),
    cpu_usage DECIMAL(5,2),
    ram_usage DECIMAL(5,2),
    security_events JSON, -- Aqui se guarda lo programado en monitor.py
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
