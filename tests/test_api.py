import os
import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

SAMPLE_PDF = os.path.join(os.path.dirname(os.path.dirname(__file__)), "11. EL-1- IPANEMA- 090319-V1 - ALIMENTADORES COMUNALES-Layout7 (2) (1).pdf")

def test_api_root():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "online"

def test_api_upload_and_status():
    assert os.path.exists(SAMPLE_PDF)
    
    with open(SAMPLE_PDF, "rb") as f:
        response = client.post("/api/upload", files={"files": ("sample.pdf", f, "application/pdf")})
        
    assert response.status_code == 200
    jobs = response.json()
    assert len(jobs) == 1
    job_id = jobs[0]["job_id"]
    
    # Check status endpoint
    status_resp = client.get(f"/api/status/{job_id}")
    assert status_resp.status_code == 200
    assert status_resp.json()["job_id"] == job_id
