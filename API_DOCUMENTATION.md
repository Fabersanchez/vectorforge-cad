# Documentación de la API REST

La API REST del conversor PDF Vectorial a DXF está construida sobre FastAPI y ofrece documentación interactiva Swagger OpenAPI disponible en `/docs`.

---

## 📌 Base URL

```
http://localhost:8000/api
```

---

## 🚀 Endpoints

### 1. Subir Archivo(s) PDF
* **Endpoint**: `POST /upload`
* **Content-Type**: `multipart/form-data`
* **Parámetros**: `files` (Lista de archivos PDF vectoriales)
* **Respuesta Ejemplo**:
  ```json
  [
    {
      "job_id": "a1b2c3d4",
      "filename": "plano_electrico.pdf",
      "status": "pending",
      "progress": 0,
      "dxf_download_url": "/api/download/a1b2c3d4",
      "created_at": "2026-08-02T15:30:00"
    }
  ]
  ```

---

### 2. Iniciar Conversión
* **Endpoint**: `POST /convert`
* **Content-Type**: `application/json`
* **Query Params**: `job_ids` (Lista de IDs de trabajo)
* **Body**:
  ```json
  {
    "dxf_version": "2018",
    "snap_tolerance": 0.0001,
    "remove_duplicates": true,
    "join_segments": true,
    "extract_text": true
  }
  ```
* **Respuesta**:
  ```json
  {
    "message": "Conversion started for 1 files.",
    "job_ids": ["a1b2c3d4"]
  }
  ```

---

### 3. Consultar Estado de Trabajo
* **Endpoint**: `GET /status/{job_id}`
* **Respuesta**:
  ```json
  {
    "job_id": "a1b2c3d4",
    "filename": "plano_electrico.pdf",
    "status": "completed",
    "progress": 100,
    "dxf_download_url": "/api/download/a1b2c3d4",
    "stats": {
      "original_counts": { "lines": 450, "total": 450 },
      "optimized_counts": { "lines": 120, "polylines": 45, "total": 165 },
      "optimization_percentage": 63.33,
      "execution_time_seconds": 0.42
    }
  }
  ```

---

### 4. Vista Previa Comparativa
* **Endpoint**: `GET /preview/{job_id}`
* **Respuesta**:
  ```json
  {
    "job_id": "a1b2c3d4",
    "filename": "plano_electrico.pdf",
    "pdf_image": "data:image/png;base64,...",
    "svg_vector": "<svg xmlns=..."
  }
  ```

---

### 5. Descargar Archivo DXF
* **Endpoint**: `GET /download/{job_id}`
* **Respuesta**: Archivo `.dxf` binario con cabecera `application/dxf`.

---

### 6. Descargar Lote en ZIP
* **Endpoint**: `POST /batch-download`
* **Body**: `["a1b2c3d4", "e5f6g7h8"]`
* **Respuesta**: Archivo `.zip` binario con todos los archivos DXF.

---

### 7. Historial y Limpieza
* `GET /history`: Retorna la lista de todos los trabajos realizados.
* `DELETE /history`: Limpia el historial persistente.
