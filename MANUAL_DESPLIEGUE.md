# Manual de Despliegue en Producción (Docker)

Este documento guía el proceso de despliegue en entornos de producción utilizando Docker y Docker Compose.

---

## 🐳 Despliegue con Docker Compose

La plataforma está completamente contenedorizada mediante multi-stage builds optimizados.

### 1. Construcción y Puesta en Marcha
Ejecute el siguiente comando en el directorio raíz del proyecto:

```bash
docker compose up -d --build
```

Este comando:
* Construirá la imagen del Backend Python con PyMuPDF, ezdxf, Shapely y NumPy.
* Construirá la versión de producción optimizada del Frontend Next.js.
* Iniciará los servicios expuestos en los puertos:
  * **Frontend**: `http://localhost:3000`
  * **Backend API**: `http://localhost:8000`

### 2. Verificación del Estado de Contenedores
```bash
docker compose ps
```

### 3. Inspección de Logs en Tiempo Real
```bash
docker compose logs -f
```

### 4. Detener los Servicios
```bash
docker compose down
```

---

## 🌐 Configuración de Proxy Inverso (Nginx Recomendado)

En servidores de producción con dominio de internet y certificado SSL/TLS (HTTPS), configure Nginx como proxy inverso:

```nginx
server {
    listen 80;
    server_name cadconverter.midominio.com;

    location / {
        proxy_pass http://127.0.0.1:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /api/ {
        proxy_pass http://127.0.0.1:8000/api/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        client_max_body_size 100M;
    }
}
```
