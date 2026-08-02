import pytest
from backend.converter.optimizer import GeometryOptimizer
from backend.models.conversion import ParsedGeometryContainer, LineEntity, Point2D

def test_optimizer_deduplication():
    container = ParsedGeometryContainer()
    # Add duplicate line segments (forward and reverse)
    container.lines.append(LineEntity(start=Point2D(0, 0), end=Point2D(10, 0)))
    container.lines.append(LineEntity(start=Point2D(10, 0), end=Point2D(0, 0))) # Reverse duplicate
    container.lines.append(LineEntity(start=Point2D(0, 0), end=Point2D(10, 0))) # Duplicate

    optimizer = GeometryOptimizer(snap_tolerance=0.0001, remove_duplicates=True, join_segments=True)
    opt_container, stats = optimizer.optimize(container)

    assert stats["original_counts"]["lines"] == 3
    assert opt_container.total_entities() == 1
    assert stats["optimization_percentage"] > 0

def test_optimizer_segment_joining():
    container = ParsedGeometryContainer()
    # 3 consecutive collinear segments: (0,0)->(10,0), (10,0)->(20,0), (20,0)->(30,0)
    container.lines.append(LineEntity(start=Point2D(0, 0), end=Point2D(10, 0)))
    container.lines.append(LineEntity(start=Point2D(10, 0), end=Point2D(20, 0)))
    container.lines.append(LineEntity(start=Point2D(20, 0), end=Point2D(30, 0)))

    optimizer = GeometryOptimizer(snap_tolerance=0.0001, remove_duplicates=True, join_segments=True)
    opt_container, stats = optimizer.optimize(container)

    # Collinear segments merged into a single line from (0,0) to (30,0)
    assert len(opt_container.lines) == 1
    line = opt_container.lines[0]
    assert line.start.x == 0.0 and line.start.y == 0.0
    assert line.end.x == 30.0 and line.end.y == 0.0
