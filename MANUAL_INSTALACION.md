# Manual de Instalación y Configuración

Este manual describe el procedimiento paso a paso para la instalación del entorno de desarrollo y ejecución de la plataforma de conversión PDF Vectorial a DXF.

---

## 📋 Requisitos Previos

Asegúrese de contar con las siguientes herramientas instaladas en su sistema:

1. **Python 3.11 o superior** (`python --version`)
2. **Node.js v18.0 o superior** y **npm v9.0 o superior** (`node -v`, `npm -v`)
3. **Docker y Docker Compose** (opcional para despliegue en contenedores)
4. **Git**

---

## 🛠️ Instalación del Backend (Python FastAPI)

1. Navegue al directorio raíz del proyecto:
   ```bash
   cd "Señor Huber"
   ```

2. Se recomienda crear un entorno virtual de Python:
   ```bash
   python -m venv venv
   ```
   * En Windows:
     ```bash
     venv\Scripts\activate
     ```
   * En Linux/macOS:
     ```bash
     source venv/bin/activate
     ```

3. Instale las dependencias necesarias:
   ```bash
   pip install -r backend/requirements.txt
   ```

4. Verifique la instalación ejecutando las pruebas unitarias:
   ```bash
   python -m pytest tests/ -v
   ```

5. Inicie el servidor de desarrollo Backend:
   ```bash
   python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
   ```
   La API estará accesible en `http://localhost:8000` y la documentación interactiva en `http://localhost:8000/docs`.

---

## 💻 Instalación del Frontend (Next.js & React)

1. En una nueva terminal, navegue a la carpeta frontend:
   ```bash
   cd frontend
   ```

2. Instale las dependencias de Node.js:
   ```bash
   npm install
   ```

3. Inicie el servidor de desarrollo de Next.js:
   ```bash
   npm run dev
   ```

4. Abra su navegador e ingrese a `http://localhost:3000`.

---

## 🔧 Variables de Entorno (Opcional)

Si requiere personalizar puertos o configuraciones, cree un archivo `.env` en `backend/` con las siguientes variables:

```env
PROJECT_NAME="PDF to DXF Professional Converter"
MAX_FILE_SIZE_MB=100
DEFAULT_DXF_VERSION="2018"
CORS_ORIGINS=["http://localhost:3000","http://127.0.0.1:3000"]
```
