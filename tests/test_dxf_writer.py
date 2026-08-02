import os
import pytest
import ezdxf
from backend.converter.dxf_writer import DXFWriter
from backend.models.conversion import ParsedGeometryContainer, LineEntity, CircleEntity, Point2D

SUPPORTED_VERSIONS = ["R12", "R14", "2000", "2004", "2007", "2010", "2013", "2018"]

@pytest.mark.parametrize("version", SUPPORTED_VERSIONS)
def test_dxf_writer_all_versions(tmp_path, version):
    container = ParsedGeometryContainer()
    container.lines.append(LineEntity(start=Point2D(0, 0), end=Point2D(100, 100)))
    container.circles.append(CircleEntity(center=Point2D(50, 50), radius=25))

    out_file = str(tmp_path / f"test_{version}.dxf")
    writer = DXFWriter(version=version)
    writer.write(container, out_file)

    assert os.path.exists(out_file)
    assert os.path.getsize(out_file) > 0

    # Verify generated file can be opened by ezdxf
    doc = ezdxf.readfile(out_file)
    assert doc is not None
