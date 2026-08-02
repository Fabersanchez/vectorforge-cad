# Plataforma Profesional de Conversión PDF Vectorial → DXF

Plataforma empresarial de alta precisión para la conversión directa de planos y diseños en formato PDF vectorial (exportados desde AutoCAD, Civil 3D, Revit, SolidWorks e Inventor) a archivos DXF editables.

---

## 🚀 Características Principales

* **Reconstrucción Geométrica Completa**: Extracción directa de entidades `LINE`, `POLYLINE`, `LWPOLYLINE`, `ARC`, `CIRCLE`, `SPLINE`, `ELLIPSE`, `TEXT` y `MTEXT`.
* **Optimizador Automático de Geometría**:
  * Eliminación de líneas duplicadas y solapamientos en sentido inverso.
  * Encadenamiento de segmentos continuos en `LWPOLYLINE`.
  * Depuración de vértices colineales y ajuste flotante (tolerance snapping).
* **Soporte Multiversión DXF**: Exportación compatible con DXF R12, R14, 2000, 2004, 2007, 2010, 2013 y 2018.
* **Interfaz de Usuario Estilo SaaS Moderno**:
  * Tema oscuro con Glassmorphic Design, efectos HSL y animaciones fluidas con Framer Motion.
  * Zonas Drag & Drop interactivo con carga individual y por lotes.
  * Vista previa comparativa en tiempo real: Render de página PDF vs Render de geometría DXF en formato SVG vectorial.
  * Descarga individual y exportación masiva en archivo ZIP.
  * Panel de estadísticas y métricas geométricas.
  * Registro persistente del historial de conversiones.
* **Docker & Despliegue en Producción**: Orquestación lista para ejecutarse mediante `docker compose up`.

---

## 🛠️ Tecnologías Utilizadas

### Backend
* **Python 3.11 / 3.12**
* **FastAPI**: REST API asíncrona de alto rendimiento.
* **PyMuPDF (`fitz`)**: Extracción matemática de trayectorias vectoriales y renderizado de páginas.
* **ezdxf**: Generación precisa de archivos DXF con capas y tablas de colores.
* **Shapely & NumPy**: Operaciones de geometría computacional y simplificación topológica.
* **Pydantic v2**: Validación estricta de esquemas.

### Frontend
* **Next.js 14 / React 18 / TypeScript**
* **Tailwind CSS**: Diseño glassmorphic moderno.
* **Framer Motion**: Micro-animaciones.
* **React Dropzone**: Subida interactiva de archivos.

---

## 📂 Estructura del Proyecto

```
.
├── backend/
│   ├── api/             # Endpoints y controladores REST
│   ├── converter/       # Extractor vector PyMuPDF, Optimizador Shapely y DXFWriter
│   ├── models/          # Modelos de datos geométricos internos
│   ├── schemas/         # Esquemas Pydantic API
│   ├── services/        # Servicios de vista previa y almacenamiento
│   ├── utils/           # Loggers y herramientas de conversión RGB/ACI
│   ├── uploads/         # Archivos PDF temporales
│   ├── outputs/         # Archivos DXF generados y ZIPs
│   ├── config.py        # Configuración centralizada
│   └── main.py          # Punto de entrada FastAPI
├── frontend/
│   ├── src/
│   │   ├── app/         # Next.js App Router (Dashboard)
│   │   ├── components/  # Dropzone, ConfigPanel, FileCard, PreviewModal, etc.
│   │   ├── services/    # Cliente de API Axios
│   │   └── types/       # Definiciones de TypeScript
├── tests/               # Pruebas unitarias pytest
├── docker/              # Dockerfiles de Frontend y Backend
└── docker-compose.yml   # Orquestador Docker
```

---

## 🏃 Inicio Rápido

### Usando Docker (Recomendado)
```bash
docker compose up --build
```
* **Frontend**: `http://localhost:3000`
* **API Backend**: `http://localhost:8000`
* **Documentación Swagger**: `http://localhost:8000/docs`

### Ejecución Local sin Docker

#### 1. Backend FastAPI:
```bash
cd backend
pip install -r requirements.txt
python -m uvicorn backend.main:app --reload --port 8000
```

#### 2. Frontend Next.js:
```bash
cd frontend
npm install
npm run dev
```

---

## 🧪 Pruebas Unitarias

Para ejecutar la suite completa de pruebas unitarias:
```bash
python -m pytest tests/ -v
```

---

## 📄 Licencia

Proyecto Institucional Profesional — Todos los derechos reservados.
