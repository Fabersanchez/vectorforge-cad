# Guía para Desarrolladores

Esta guía describe los principios de arquitectura, patrones de diseño y flujo de trabajo para desarrolladores interesados en extender o mantener el motor de conversión PDF Vectorial a DXF.

---

## 🏛️ Arquitectura y Principios SOLID

El proyecto sigue una arquitectura desacoplada orientada a servicios:

1. **Single Responsibility Principle (SRP)**:
   * `PDFVectorExtractor`: Única responsabilidad de parsear instrucciones vectoriales PyMuPDF e inverting la coordenada Y para CAD.
   * `GeometryOptimizer`: Única responsabilidad de simplificación topológica (Shapely + NumPy).
   * `DXFWriter`: Única responsabilidad de mapeo de entidades a estructuras ezdxf y guardado por versión.
   * `StorageService`: Única responsabilidad del ciclo de vida de archivos y persistencia JSON.

2. **Open/Closed Principle (OCP)**:
   * Para añadir soporte a un nuevo formato de salida (ej. SVG, DWG, IGES), extienda la interfaz del generador sin modificar el extractor central.

---

## 📐 Algoritmos Clave

### Inversión del Sistema de Coordenadas
PDF utiliza el origen `(0,0)` en la esquina superior izquierda (Y crece hacia abajo). CAD utiliza el origen `(0,0)` en la esquina inferior izquierda (Y crece hacia arriba).
$$\text{Y}_{\text{CAD}} = \text{AltoPágina}_{\text{PDF}} - \text{Y}_{\text{PDF}}$$

### Optimización y Reducción de Líneas Duplicadas
Se implementó un hash canónico para cada segmento independientemente del sentido de recorrido:
$$\text{SegmentKey} = (\min(P_1, P_2), \max(P_1, P_2), \text{Capa})$$

### Fusión de Segmentos Continuos (LineMerge)
Utiliza estructuras `LineString` y `MultiLineString` de `Shapely` para reconstruir secuencias de segmentos en polígonos `LWPOLYLINE` eficientes.

---

## 🧪 Ejecución de Pruebas y Cobertura

Para agregar nuevas pruebas unitarias:
1. Añada archivos de prueba en `tests/`.
2. Ejecute `python -m pytest tests/ --cov=backend` para medir la cobertura del código.
