import fitz  # PyMuPDF
import math
import numpy as np
from typing import List, Tuple, Optional
from backend.models.conversion import (
    Point2D, LineEntity, PolylineEntity, ArcEntity, CircleEntity,
    SplineEntity, TextEntity, ParsedGeometryContainer
)
from backend.utils.logger import logger

class PDFVectorExtractor:
    """
    High-precision vector geometry & text extractor using PyMuPDF (fitz).
    Inverts Y-axis to convert PDF coordinates (top-left origin) to CAD coordinates (bottom-left origin).
    """

    def __init__(self, extract_text: bool = True):
        self.extract_text = extract_text

    def extract_geometry(self, pdf_path: str, page_number: int = 0) -> ParsedGeometryContainer:
        container = ParsedGeometryContainer()
        doc = fitz.open(pdf_path)
        
        if page_number < 0 or page_number >= len(doc):
            page_number = 0
            
        page = doc[page_number]
        page_height = page.rect.height

        # 1. Extract Vector Drawing Paths
        drawings = page.get_drawings()
        for path in drawings:
            color = self._parse_color(path.get("color"))
            stroke_width = path.get("width", 0.1)
            layer = path.get("layer", "0") or "0"
            
            items = path.get("items", [])
            current_points: List[Point2D] = []

            for item in items:
                cmd = item[0]
                
                if cmd == "m":  # Move to
                    if len(current_points) > 1:
                        self._add_polyline_or_lines(container, current_points, color, stroke_width, layer)
                    p = self._to_cad_point(item[1], page_height)
                    current_points = [p]

                elif cmd == "l":  # Line to
                    p1 = self._to_cad_point(item[1], page_height)
                    p2 = self._to_cad_point(item[2], page_height)
                    
                    if not current_points:
                        current_points.append(p1)
                    current_points.append(p2)

                elif cmd == "re":  # Rectangle
                    rect = item[1]
                    x0, y0, x1, y1 = rect.x0, rect.y0, rect.x1, rect.y1
                    p0 = self._to_cad_point(fitz.Point(x0, y0), page_height)
                    p1 = self._to_cad_point(fitz.Point(x1, y0), page_height)
                    p2 = self._to_cad_point(fitz.Point(x1, y1), page_height)
                    p3 = self._to_cad_point(fitz.Point(x0, y1), page_height)
                    
                    rect_poly = PolylineEntity(
                        points=[p0, p1, p2, p3, p0],
                        is_closed=True,
                        color=color,
                        width=stroke_width,
                        layer=layer
                    )
                    container.polylines.append(rect_poly)

                elif cmd == "c":  # Cubic Bezier Curve (c, p1, p2, p3, p4)
                    p1 = self._to_cad_point(item[1], page_height)
                    p2 = self._to_cad_point(item[2], page_height)
                    p3 = self._to_cad_point(item[3], page_height)
                    p4 = self._to_cad_point(item[4], page_height)

                    # Try circle/arc fitting or approximate as smooth adaptive polyline / spline
                    arc = self._try_fit_arc(p1, p2, p3, p4, color, layer)
                    if arc:
                        container.arcs.append(arc)
                    else:
                        spline_pts = self._sample_cubic_bezier(p1, p2, p3, p4)
                        container.splines.append(SplineEntity(
                            control_points=[p1, p2, p3, p4],
                            color=color,
                            layer=layer
                        ))
                        # Also add sampled points to polylines for high compatibility
                        container.polylines.append(PolylineEntity(
                            points=spline_pts,
                            is_closed=False,
                            color=color,
                            width=stroke_width,
                            layer=layer
                        ))

            if len(current_points) > 1:
                self._add_polyline_or_lines(container, current_points, color, stroke_width, layer)

        # 2. Extract Text Elements
        if self.extract_text:
            self._extract_text(page, page_height, container)

        doc.close()
        logger.info(f"Extracted geometry: {container.entity_counts()}")
        return container

    def _to_cad_point(self, pt: fitz.Point, page_height: float) -> Point2D:
        """Converts PyMuPDF point to CAD coordinate system (invert Y)."""
        return Point2D(x=round(float(pt.x), 4), y=round(float(page_height - pt.y), 4))

    def _parse_color(self, color_tuple) -> Tuple[float, float, float]:
        if not color_tuple:
            return (1.0, 1.0, 1.0)
        if isinstance(color_tuple, (list, tuple)):
            if len(color_tuple) == 3:
                return (float(color_tuple[0]), float(color_tuple[1]), float(color_tuple[2]))
            elif len(color_tuple) == 1:
                c = float(color_tuple[0])
                return (c, c, c)
        return (1.0, 1.0, 1.0)

    def _add_polyline_or_lines(self, container: ParsedGeometryContainer, points: List[Point2D],
                               color: Tuple[float, float, float], width: float, layer: str):
        if len(points) == 2:
            container.lines.append(LineEntity(
                start=points[0], end=points[1], color=color, width=width, layer=layer
            ))
        elif len(points) > 2:
            is_closed = (abs(points[0].x - points[-1].x) < 1e-3 and abs(points[0].y - points[-1].y) < 1e-3)
            container.polylines.append(PolylineEntity(
                points=points, is_closed=is_closed, color=color, width=width, layer=layer
            ))

    def _sample_cubic_bezier(self, p1: Point2D, p2: Point2D, p3: Point2D, p4: Point2D, num_samples: int = 16) -> List[Point2D]:
        pts = []
        for t in np.linspace(0, 1, num_samples):
            inv_t = 1.0 - t
            x = (inv_t**3 * p1.x + 3 * inv_t**2 * t * p2.x +
                 3 * inv_t * t**2 * p3.x + t**3 * p4.x)
            y = (inv_t**3 * p1.y + 3 * inv_t**2 * t * p2.y +
                 3 * inv_t * t**2 * p3.y + t**3 * p4.y)
            pts.append(Point2D(x=round(float(x), 4), y=round(float(y), 4)))
        return pts

    def _try_fit_arc(self, p1: Point2D, p2: Point2D, p3: Point2D, p4: Point2D,
                     color: Tuple[float, float, float], layer: str) -> Optional[ArcEntity]:
        # Check if curve looks like a circular arc using midpoint circle test
        mid_t = 0.5
        mx = 0.125 * p1.x + 0.375 * p2.x + 0.375 * p3.x + 0.125 * p4.x
        my = 0.125 * p1.y + 0.375 * p2.y + 0.375 * p3.y + 0.125 * p4.y
        pmid = Point2D(x=mx, y=my)
        
        # 3 points circle center
        ax, ay = p1.x, p1.y
        bx, by = pmid.x, pmid.y
        cx, cy = p4.x, p4.y
        
        d = 2 * (ax * (by - cy) + bx * (cy - ay) + cx * (ay - by))
        if abs(d) < 1e-5:
            return None
            
        ux = ((ax*ax + ay*ay)*(by - cy) + (bx*bx + by*by)*(cy - ay) + (cx*cx + cy*cy)*(ay - by)) / d
        uy = ((ax*ax + ay*ay)*(cx - bx) + (bx*bx + by*by)*(ax - cx) + (cx*cx + cy*cy)*(bx - ax)) / d
        center = Point2D(x=round(ux, 4), y=round(uy, 4))
        
        r1 = math.hypot(ax - ux, ay - uy)
        r2 = math.hypot(bx - ux, by - uy)
        r3 = math.hypot(cx - ux, cy - uy)
        
        # Check if radii match within 1.5% error
        if max(abs(r1 - r2), abs(r2 - r3)) / (r1 + 1e-6) < 0.015:
            start_angle = math.degrees(math.atan2(ay - uy, ax - ux)) % 360
            end_angle = math.degrees(math.atan2(cy - uy, cx - ux)) % 360
            return ArcEntity(
                center=center,
                radius=round(r1, 4),
                start_angle=round(start_angle, 2),
                end_angle=round(end_angle, 2),
                color=color,
                layer=layer
            )
        return None

    def _extract_text(self, page: fitz.Page, page_height: float, container: ParsedGeometryContainer):
        text_dict = page.get_text("dict", flags=fitz.TEXT_PRESERVE_WHITESPACE)
        for block in text_dict.get("blocks", []):
            if block.get("type") == 0:  # Text block
                for line in block.get("lines", []):
                    dir_x, dir_y = line.get("dir", (1, 0))
                    rotation = math.degrees(math.atan2(-dir_y, dir_x)) % 360
                    
                    for span in line.get("spans", []):
                        text_str = span.get("text", "").strip()
                        if not text_str:
                            continue
                            
                        bbox = span.get("bbox")  # (x0, y0, x1, y1)
                        height = span.get("size", 10.0)
                        font_name = span.get("font", "ARIAL")
                        color_int = span.get("color", 0)
                        
                        r = ((color_int >> 16) & 255) / 255.0
                        g = ((color_int >> 8) & 255) / 255.0
                        b = (color_int & 255) / 255.0
                        
                        # Invert y coordinate for CAD
                        x0 = bbox[0]
                        y0 = page_height - bbox[3]  # Baseline bottom
                        
                        container.texts.append(TextEntity(
                            text=text_str,
                            position=Point2D(x=round(x0, 4), y=round(y0, 4)),
                            height=round(height, 2),
                            rotation=round(rotation, 2),
                            font_name=font_name,
                            color=(r, g, b),
                            layer="TEXT",
                            is_mtext=len(text_str) > 30 or "\n" in text_str
                        ))
