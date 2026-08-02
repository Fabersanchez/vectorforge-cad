import os
from pathlib import Path
from typing import Dict, Any, Tuple

from backend.converter.extractor import PDFVectorExtractor
from backend.converter.optimizer import GeometryOptimizer
from backend.converter.dxf_writer import DXFWriter
from backend.models.conversion import ParsedGeometryContainer
from backend.schemas.request_response import ConversionOptionsSchema
from backend.utils.logger import logger

class ConversionEngine:
    """
    Unified CAD Vector PDF to DXF Conversion Orchestrator.
    """

    def process_file(self, pdf_path: str, output_dxf_path: str, options: ConversionOptionsSchema) -> Dict[str, Any]:
        logger.info(f"Starting conversion for {pdf_path} -> {output_dxf_path} with options: {options.model_dump()}")
        
        # 1. Extraction
        extractor = PDFVectorExtractor(extract_text=options.extract_text)
        raw_geometry = extractor.extract_geometry(pdf_path, page_number=0)

        # 2. Optimization
        optimizer = GeometryOptimizer(
            snap_tolerance=options.snap_tolerance,
            remove_duplicates=options.remove_duplicates,
            join_segments=options.join_segments
        )
        optimized_geometry, opt_stats = optimizer.optimize(raw_geometry)

        # 3. DXF Generation
        writer = DXFWriter(version=options.dxf_version)
        writer.write(optimized_geometry, output_dxf_path)

        # File size calculation
        orig_size = os.path.getsize(pdf_path) if os.path.exists(pdf_path) else 0
        output_size = os.path.getsize(output_dxf_path) if os.path.exists(output_dxf_path) else 0

        opt_stats["original_file_size_bytes"] = orig_size
        opt_stats["output_file_size_bytes"] = output_size

        return {
            "dxf_path": output_dxf_path,
            "geometry": optimized_geometry,
            "stats": opt_stats
        }

engine = ConversionEngine()
