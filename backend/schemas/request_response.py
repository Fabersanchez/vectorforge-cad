from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class ConversionOptionsSchema(BaseModel):
    dxf_version: str = Field("2018", description="DXF version (R12, R14, 2000, 2004, 2007, 2010, 2013, 2018)")
    snap_tolerance: float = Field(0.0001, description="Point snapping tolerance in mm")
    remove_duplicates: bool = Field(True, description="Remove duplicate lines and overlapping segments")
    join_segments: bool = Field(True, description="Join consecutive lines into LWPOLYLINE")
    extract_text: bool = Field(True, description="Extract and convert PDF text elements")

class ConvertRequestSchema(BaseModel):
    job_ids: List[str]
    options: ConversionOptionsSchema

class BatchDownloadRequestSchema(BaseModel):
    job_ids: List[str]

class EntityCountsSchema(BaseModel):
    lines: int = 0
    polylines: int = 0
    arcs: int = 0
    circles: int = 0
    ellipses: int = 0
    splines: int = 0
    texts: int = 0
    total: int = 0

class OptimizationStatsSchema(BaseModel):
    original_counts: EntityCountsSchema
    optimized_counts: EntityCountsSchema
    optimization_percentage: float = 0.0
    execution_time_seconds: float = 0.0
    original_file_size_bytes: int = 0
    output_file_size_bytes: int = 0

class ConversionJobResponse(BaseModel):
    job_id: str
    filename: str
    status: str  # "pending", "processing", "completed", "failed"
    progress: int = 0
    dxf_download_url: Optional[str] = None
    stats: Optional[OptimizationStatsSchema] = None
    error: Optional[str] = None
    created_at: str

class BatchConversionResponse(BaseModel):
    batch_id: str
    total_files: int
    zip_download_url: Optional[str] = None
    jobs: List[ConversionJobResponse]

class HistoryItemResponse(BaseModel):
    job_id: str
    original_name: str
    dxf_name: str
    status: str
    dxf_version: str
    stats: Optional[OptimizationStatsSchema] = None
    created_at: str
