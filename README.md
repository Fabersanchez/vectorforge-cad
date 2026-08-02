<div align="center">

# VectorForge CAD

### Engineering Precision. Modern Simplicity.

**Professional PDF Vector → DXF Conversion Platform**

Convert vector PDF drawings exported from AutoCAD®, Civil 3D®, Revit®, Inventor® and SolidWorks® into editable DXF files with enterprise-grade precision.

---

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi)
![Next.js](https://img.shields.io/badge/Next.js-14-black?logo=next.js)
![React](https://img.shields.io/badge/React-18-61DAFB?logo=react)
![TypeScript](https://img.shields.io/badge/TypeScript-5-3178C6?logo=typescript)
![TailwindCSS](https://img.shields.io/badge/TailwindCSS-3-38BDF8?logo=tailwind-css)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?logo=docker)
![DXF](https://img.shields.io/badge/DXF-R12--2018-success)

</div>

---

# Overview

VectorForge CAD is an enterprise-grade web application that converts vector PDF engineering drawings into editable DXF files while preserving geometry, structure and CAD compatibility.

Unlike conventional PDF converters that rely on rasterization, VectorForge CAD extracts vector entities directly from mathematical paths, reconstructing CAD geometry with high precision.

The platform is intended for engineering companies, architects, surveyors, electrical designers, mechanical designers and CAD professionals.

---

# Features

| Feature | Description |
|----------|-------------|
| Vector PDF Extraction | Direct extraction of vector entities from CAD-exported PDFs |
| Geometry Reconstruction | Rebuilds CAD geometry with high precision |
| Geometry Optimizer | Removes duplicates, merges segments and simplifies geometry |
| DXF Export | Supports DXF R12, R14, 2000, 2004, 2007, 2010, 2013 and 2018 |
| SVG Preview | Real-time PDF and DXF comparison |
| Batch Conversion | Convert multiple files simultaneously |
| ZIP Export | Download all converted files in a single archive |
| Conversion History | Persistent conversion history |
| REST API | High-performance asynchronous FastAPI backend |
| Docker Ready | One-command deployment |

---

# Supported CAD Entities

VectorForge CAD reconstructs the following entities:

- LINE
- POLYLINE
- LWPOLYLINE
- ARC
- CIRCLE
- ELLIPSE
- SPLINE
- TEXT
- MTEXT

---

# Geometry Optimization

The optimization engine performs automatic cleanup before DXF generation.

### Automatic duplicate removal

Removes duplicated and reversed segments.

### Polyline reconstruction

Connects continuous segments into optimized LWPOLYLINE entities.

### Floating point correction

Automatically snaps nearby vertices using configurable tolerances.

### Collinear simplification

Eliminates unnecessary intermediate vertices.

### Geometry validation

Repairs invalid entities before DXF export.

---

# User Interface

Modern SaaS-inspired interface featuring:

- Dark Theme
- Glassmorphism UI
- Responsive Dashboard
- Drag & Drop Upload
- Batch Upload
- Real-time Progress
- Animated Components
- SVG Preview
- Download Manager
- Conversion History

---

# Technology Stack

| Layer | Technology |
|---------|------------|
| Backend | FastAPI |
| Language | Python 3.11 |
| Frontend | Next.js 14 |
| UI | React 18 |
| Styling | Tailwind CSS |
| Animations | Framer Motion |
| PDF Engine | PyMuPDF |
| CAD Engine | ezdxf |
| Geometry | Shapely |
| Numerical Computing | NumPy |
| Validation | Pydantic v2 |
| Containers | Docker |

---

# Project Structure

```text
vectorforge-cad/

├── backend/
│   ├── api/
│   ├── converter/
│   ├── models/
│   ├── schemas/
│   ├── services/
│   ├── utils/
│   ├── config.py
│   └── main.py
│
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   ├── components/
│   │   ├── services/
│   │   └── types/
│
├── docker/
│
├── tests/
│
├── docker-compose.yml
│
└── README.md
```

---

# System Architecture

```text
                   VectorForge CAD

             ┌───────────────────────┐
             │     Next.js Frontend  │
             └───────────┬───────────┘
                         │
                    REST API
                         │
             ┌───────────▼───────────┐
             │    FastAPI Backend    │
             └───────────┬───────────┘
                         │
      ┌──────────────────┼──────────────────┐
      │                  │                  │
      ▼                  ▼                  ▼
  PyMuPDF         Geometry Engine      DXF Writer
      │                  │                  │
      └──────────────────┼──────────────────┘
                         ▼
                 Optimized DXF Output
```

---

# Quick Start

## Clone Repository

```bash
git clone https://github.com/Fabersanchez/vectorforge-cad.git

cd vectorforge-cad
```

---

## Docker Deployment

```bash
docker compose up --build
```

Frontend

```
http://localhost:3000
```

Backend API

```
http://localhost:8000
```

Swagger Documentation

```
http://localhost:8000/docs
```

---

# Local Installation

## Backend

```bash
cd backend

pip install -r requirements.txt

uvicorn backend.main:app --reload
```

---

## Frontend

```bash
cd frontend

npm install

npm run dev
```

---

# Running Tests

```bash
pytest tests -v
```

---

# Roadmap

## Version 1.0

- PDF → DXF Conversion
- Batch Processing
- SVG Preview
- Docker Deployment

---

## Version 2.0

- DWG Support
- AI Geometry Repair
- OCR Layer Detection
- Cloud Storage

---

## Version 3.0

- SaaS Platform
- Team Workspaces
- Public API
- AutoCAD Plugin
- Revit Plugin

---

# Performance Goals

- High-precision vector extraction
- Fast asynchronous processing
- Large engineering drawing support
- Optimized DXF generation
- Low memory footprint

---

# Future Features

- DWG Export
- SVG Export
- AI Geometry Repair
- Cloud Conversion
- Conversion API
- User Authentication
- Project Management
- Enterprise Dashboard

---

# Contributing

Contributions are welcome.

Please open an Issue before submitting a Pull Request for major changes.

---

# License

Copyright © 2026 VectorForge CAD.

All Rights Reserved.

---

<div align="center">

### Engineering Precision. Modern Simplicity.

**Built for engineers. Designed for precision.**

</div>
