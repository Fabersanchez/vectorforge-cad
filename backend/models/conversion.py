from dataclasses import dataclass, field
from typing import List, Tuple, Optional, Dict, Any

@dataclass
class Point2D:
    x: float
    y: float

    def to_tuple(self) -> Tuple[float, float]:
        return (self.x, self.y)

@dataclass
class LineEntity:
    start: Point2D
    end: Point2D
    color: Tuple[float, float, float] = (1.0, 1.0, 1.0)
    width: float = 0.1
    layer: str = "0"

@dataclass
class PolylineEntity:
    points: List[Point2D]
    is_closed: bool = False
    color: Tuple[float, float, float] = (1.0, 1.0, 1.0)
    width: float = 0.1
    layer: str = "0"

@dataclass
class ArcEntity:
    center: Point2D
    radius: float
    start_angle: float  # In degrees
    end_angle: float    # In degrees
    color: Tuple[float, float, float] = (1.0, 1.0, 1.0)
    layer: str = "0"

@dataclass
class CircleEntity:
    center: Point2D
    radius: float
    color: Tuple[float, float, float] = (1.0, 1.0, 1.0)
    layer: str = "0"

@dataclass
class EllipseEntity:
    center: Point2D
    major_axis: Point2D
    ratio: float
    start_param: float = 0.0
    end_param: float = 6.283185307179586
    color: Tuple[float, float, float] = (1.0, 1.0, 1.0)
    layer: str = "0"

@dataclass
class SplineEntity:
    control_points: List[Point2D]
    degree: int = 3
    color: Tuple[float, float, float] = (1.0, 1.0, 1.0)
    layer: str = "0"

@dataclass
class TextEntity:
    text: str
    position: Point2D
    height: float
    rotation: float = 0.0  # In degrees
    font_name: str = "ARIAL"
    color: Tuple[float, float, float] = (1.0, 1.0, 1.0)
    layer: str = "TEXT"
    is_mtext: bool = False

@dataclass
class ParsedGeometryContainer:
    lines: List[LineEntity] = field(default_factory=list)
    polylines: List[PolylineEntity] = field(default_factory=list)
    arcs: List[ArcEntity] = field(default_factory=list)
    circles: List[CircleEntity] = field(default_factory=list)
    ellipses: List[EllipseEntity] = field(default_factory=list)
    splines: List[SplineEntity] = field(default_factory=list)
    texts: List[TextEntity] = field(default_factory=list)

    def total_entities(self) -> int:
        return (len(self.lines) + len(self.polylines) + len(self.arcs) +
                len(self.circles) + len(self.ellipses) + len(self.splines) +
                len(self.texts))

    def entity_counts(self) -> Dict[str, int]:
        return {
            "lines": len(self.lines),
            "polylines": len(self.polylines),
            "arcs": len(self.arcs),
            "circles": len(self.circles),
            "ellipses": len(self.ellipses),
            "splines": len(self.splines),
            "texts": len(self.texts),
            "total": self.total_entities()
        }
