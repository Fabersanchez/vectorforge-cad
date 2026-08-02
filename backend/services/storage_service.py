import os
import json
import zipfile
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any

from backend.config import settings
from backend.utils.logger import logger

HISTORY_FILE = settings.BASE_DIR / "history.json"

class StorageService:
    """
    Manages uploaded PDFs, generated DXF outputs, batch ZIP archives, and persistent history state.
    """

    def __init__(self):
        self.jobs: Dict[str, Dict[str, Any]] = {}
        self._load_history()

    def _load_history(self):
        if HISTORY_FILE.exists():
            try:
                with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    for item in data:
                        if item.get("stats") and "initial_counts" in item["stats"]:
                            item["stats"]["original_counts"] = item["stats"].pop("initial_counts")
                        self.jobs[item["job_id"]] = item
            except Exception as e:
                logger.error(f"Error loading history file: {e}")

    def _save_history(self):
        try:
            items = list(self.jobs.values())
            with open(HISTORY_FILE, "w", encoding="utf-8") as f:
                json.dump(items, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Error saving history file: {e}")

    def create_job(self, original_filename: str) -> str:
        job_id = str(uuid.uuid4())[:8]
        safe_filename = f"{job_id}_{original_filename.replace(' ', '_')}"
        upload_path = str(settings.UPLOAD_DIR / safe_filename)
        
        dxf_filename = f"{Path(original_filename).stem}.dxf"
        output_dxf_path = str(settings.OUTPUT_DIR / f"{job_id}_{dxf_filename}")

        job_data = {
            "job_id": job_id,
            "original_filename": original_filename,
            "upload_path": upload_path,
            "dxf_filename": dxf_filename,
            "output_dxf_path": output_dxf_path,
            "status": "pending",
            "progress": 0,
            "dxf_version": settings.DEFAULT_DXF_VERSION,
            "stats": None,
            "error": None,
            "created_at": datetime.now().isoformat()
        }
        self.jobs[job_id] = job_data
        self._save_history()
        return job_id

    def update_job_status(self, job_id: str, status: str, progress: int = 100,
                          stats: Optional[Dict] = None, error: Optional[str] = None):
        if job_id in self.jobs:
            self.jobs[job_id]["status"] = status
            self.jobs[job_id]["progress"] = progress
            if stats:
                self.jobs[job_id]["stats"] = stats
            if error:
                self.jobs[job_id]["error"] = error
            self._save_history()

    def get_job(self, job_id: str) -> Optional[Dict[str, Any]]:
        return self.jobs.get(job_id)

    def get_all_jobs(self) -> List[Dict[str, Any]]:
        return sorted(self.jobs.values(), key=lambda x: x.get("created_at", ""), reverse=True)

    def clear_history(self):
        self.jobs.clear()
        if HISTORY_FILE.exists():
            try:
                os.remove(HISTORY_FILE)
            except Exception as e:
                logger.error(f"Error removing history file: {e}")

    def create_batch_zip(self, job_ids: List[str]) -> Optional[str]:
        batch_id = str(uuid.uuid4())[:8]
        zip_filename = f"batch_dxf_{batch_id}.zip"
        zip_path = str(settings.OUTPUT_DIR / zip_filename)

        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            for jid in job_ids:
                job = self.get_job(jid)
                if job and job.get("status") == "completed":
                    dxf_path = job.get("output_dxf_path")
                    if dxf_path and os.path.exists(dxf_path):
                        zipf.write(dxf_path, arcname=job.get("dxf_filename"))

        return zip_path if os.path.exists(zip_path) else None

storage_service = StorageService()
