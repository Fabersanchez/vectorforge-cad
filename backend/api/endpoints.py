import os
import shutil
from typing import List, Optional
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse, JSONResponse

from backend.config import settings
from backend.services.storage_service import storage_service
from backend.services.preview_service import preview_service
from backend.converter.engine import engine
from backend.schemas.request_response import (
    ConversionOptionsSchema, ConversionJobResponse, BatchConversionResponse,
    HistoryItemResponse, ConvertRequestSchema, BatchDownloadRequestSchema
)
from backend.utils.logger import logger

router = APIRouter()

@router.post("/upload", response_model=List[ConversionJobResponse])
async def upload_files(files: List[UploadFile] = File(...)):
    """
    Upload one or multiple CAD Vector PDF files for conversion.
    """
    responses = []
    for file in files:
        if not file.filename.lower().endswith(".pdf"):
            raise HTTPException(status_code=400, detail=f"File '{file.filename}' is not a PDF.")

        job_id = storage_service.create_job(file.filename)
        job_data = storage_service.get_job(job_id)

        # Save uploaded file
        upload_path = job_data["upload_path"]
        with open(upload_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        logger.info(f"File uploaded: {file.filename} -> job_id: {job_id}")

        responses.append(ConversionJobResponse(
            job_id=job_id,
            filename=file.filename,
            status="pending",
            progress=0,
            dxf_download_url=f"/api/download/{job_id}",
            created_at=job_data["created_at"]
        ))

    return responses


def _process_conversion_task(job_id: str, options: ConversionOptionsSchema):
    """Background task function to process conversion without blocking API."""
    job = storage_service.get_job(job_id)
    if not job:
        return

    try:
        storage_service.update_job_status(job_id, "processing", progress=25)
        
        pdf_path = job["upload_path"]
        dxf_path = job["output_dxf_path"]

        result = engine.process_file(pdf_path, dxf_path, options)
        
        storage_service.update_job_status(
            job_id,
            status="completed",
            progress=100,
            stats=result["stats"]
        )
        logger.info(f"Conversion job {job_id} completed successfully.")
    except Exception as e:
        logger.exception(f"Conversion job {job_id} failed: {e}")
        storage_service.update_job_status(
            job_id,
            status="failed",
            progress=100,
            error=str(e)
        )


@router.post("/convert")
async def convert_files(
    payload: ConvertRequestSchema,
    background_tasks: BackgroundTasks
):
    """
    Trigger conversion for one or more job IDs with specified options.
    """
    valid_jobs = []
    for jid in payload.job_ids:
        job = storage_service.get_job(jid)
        if job:
            valid_jobs.append(jid)
            background_tasks.add_task(_process_conversion_task, jid, payload.options)

    if not valid_jobs:
        raise HTTPException(status_code=404, detail="No valid pending jobs found.")

    return {"message": f"Conversion started for {len(valid_jobs)} files.", "job_ids": valid_jobs}


@router.get("/status/{job_id}", response_model=ConversionJobResponse)
async def get_job_status(job_id: str):
    """Check progress & status of a specific conversion job."""
    job = storage_service.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    # Normalize stats dict: migrate old key name if needed
    raw_stats = job.get("stats")
    if isinstance(raw_stats, dict) and "initial_counts" in raw_stats:
        raw_stats = dict(raw_stats)
        raw_stats["original_counts"] = raw_stats.pop("initial_counts")

    return ConversionJobResponse(
        job_id=job["job_id"],
        filename=job["original_filename"],
        status=job["status"],
        progress=job["progress"],
        dxf_download_url=f"/api/download/{job_id}" if job["status"] == "completed" else None,
        stats=raw_stats,
        error=job.get("error"),
        created_at=job["created_at"]
    )


@router.get("/preview/{job_id}")
async def get_job_preview(job_id: str):
    """
    Generates side-by-side preview: PDF image base64 & vector SVG render.
    """
    job = storage_service.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    pdf_path = job["upload_path"]
    dxf_path = job["output_dxf_path"]

    pdf_image_data = ""
    svg_vector_data = ""

    if os.path.exists(pdf_path):
        try:
            pdf_image_data = preview_service.generate_pdf_preview_base64(pdf_path, 0)
        except Exception as e:
            logger.error(f"Failed to generate PDF preview: {e}")

    # Generate vector preview
    try:
        from backend.converter.extractor import PDFVectorExtractor
        ext = PDFVectorExtractor(extract_text=True)
        geom = ext.extract_geometry(pdf_path, 0)
        svg_vector_data = preview_service.generate_vector_svg(geom)
    except Exception as e:
        logger.error(f"Failed to generate vector SVG preview: {e}")

    return {
        "job_id": job_id,
        "filename": job["original_filename"],
        "pdf_image": pdf_image_data,
        "svg_vector": svg_vector_data
    }


@router.get("/download/{job_id}")
async def download_file(job_id: str):
    """Download converted DXF file."""
    job = storage_service.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    dxf_path = job["output_dxf_path"]
    if not os.path.exists(dxf_path):
        raise HTTPException(status_code=404, detail="DXF file not available for download")

    return FileResponse(
        path=dxf_path,
        filename=job["dxf_filename"],
        media_type="application/dxf"
    )


@router.post("/batch-download")
async def batch_download(payload: BatchDownloadRequestSchema):
    """Download multiple DXF files as a ZIP archive."""
    zip_path = storage_service.create_batch_zip(payload.job_ids)
    if not zip_path or not os.path.exists(zip_path):
        raise HTTPException(status_code=400, detail="Unable to create ZIP archive for requested jobs.")

    return FileResponse(
        path=zip_path,
        filename=os.path.basename(zip_path),
        media_type="application/zip"
    )


@router.get("/history", response_model=List[HistoryItemResponse])
async def get_history():
    """Retrieve full history of conversion jobs."""
    jobs = storage_service.get_all_jobs()
    history = []
    for j in jobs:
        history.append(HistoryItemResponse(
            job_id=j["job_id"],
            original_name=j["original_filename"],
            dxf_name=j["dxf_filename"],
            status=j["status"],
            dxf_version=j.get("dxf_version", settings.DEFAULT_DXF_VERSION),
            stats=j.get("stats"),
            created_at=j["created_at"]
        ))
    return history


@router.delete("/history")
async def clear_history():
    """Clear conversion history."""
    storage_service.clear_history()
    return {"message": "History cleared successfully."}
