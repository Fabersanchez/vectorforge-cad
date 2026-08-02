import os
import pytest
from backend.converter.extractor import PDFVectorExtractor
from backend.models.conversion import ParsedGeometryContainer

# Path to workspace sample PDF
SAMPLE_PDF = os.path.join(os.path.dirname(os.path.dirname(__file__)), "11. EL-1- IPANEMA- 090319-V1 - ALIMENTADORES COMUNALES-Layout7 (2) (1).pdf")

def test_extractor_sample_pdf():
    assert os.path.exists(SAMPLE_PDF), f"Sample PDF missing at {SAMPLE_PDF}"
    
    extractor = PDFVectorExtractor(extract_text=True)
    container = extractor.extract_geometry(SAMPLE_PDF, page_number=0)

    assert isinstance(container, ParsedGeometryContainer)
    assert container.total_entities() > 0
    counts = container.entity_counts()
    print("Sample PDF Entity Counts:", counts)
    assert counts["total"] > 0
