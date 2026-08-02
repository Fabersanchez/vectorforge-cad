import fitz
import base64
from typing import Dict, Any
from backend.models.conversion import ParsedGeometryContainer
from backend.utils.logger import logger

class PreviewService:
    """
    Renders visual previews for PDF original page and converted vector SVG geometry.
    """

    def generate_pdf_preview_base64(self, pdf_path: str, page_num: int = 0) -> str:
        """Renders PDF page to PNG base64 data URL."""
        doc = fitz.open(pdf_path)
        if page_num < 0 or page_num >= len(doc):
            page_num = 0
        page = doc[page_num]
        pix = page.get_pixmap(dpi=120)
        img_bytes = pix.tobytes("png")
        doc.close()
        encoded = base64.b64encode(img_bytes).decode("utf-8")
        return f"data:image/png;base64,{encoded}"

    def generate_vector_svg(self, container: ParsedGeometryContainer, width: int = 800, height: int = 600) -> str:
        """Generates an SVG string representation of the parsed geometry container."""
        # Find bounding box
        all_pts = []
        for line in container.lines:
            all_pts.extend([line.start, line.end])
        for poly in container.polylines:
            all_pts.extend(poly.points)
        for arc in container.arcs:
            all_pts.append(arc.center)
        for circle in container.circles:
            all_pts.append(circle.center)
        for text in container.texts:
            all_pts.append(text.position)

        if not all_pts:
            return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}"><text x="50%" y="50%" fill="#888" text-anchor="middle">No Geometry Found</text></svg>'

        min_x = min(p.x for p in all_pts)
        max_x = max(p.x for p in all_pts)
        min_y = min(p.y for p in all_pts)
        max_y = max(p.y for p in all_pts)

        w = max_x - min_x or 100.0
        h = max_y - min_y or 100.0
        margin = max(w, h) * 0.05
        vb_x = min_x - margin
        vb_y = min_y - margin
        vb_w = w + 2 * margin
        vb_h = h + 2 * margin

        svg_parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb_x:.2f} {-vb_y - vb_h:.2f} {vb_w:.2f} {vb_h:.2f}" style="background-color: #0d1117; width: 100%; height: 100%;">'
        ]

        # Draw lines
        for line in container.lines:
            # SVG y is inverted relative to CAD
            svg_parts.append(
                f'<line x1="{line.start.x:.2f}" y1="{-line.start.y:.2f}" x2="{line.end.x:.2f}" y2="{-line.end.y:.2f}" stroke="#00f0ff" stroke-width="0.8" />'
            )

        # Draw polylines
        for poly in container.polylines:
            pts_str = " ".join([f"{p.x:.2f},{-p.y:.2f}" for p in poly.points])
            svg_parts.append(
                f'<polyline points="{pts_str}" fill="none" stroke="#7000ff" stroke-width="0.8" />'
            )

        # Draw circles
        for circle in container.circles:
            svg_parts.append(
                f'<circle cx="{circle.center.x:.2f}" cy="{-circle.center.y:.2f}" r="{circle.radius:.2f}" fill="none" stroke="#00ff66" stroke-width="0.8" />'
            )

        # Draw arcs
        for arc in container.arcs:
            svg_parts.append(
                f'<circle cx="{arc.center.x:.2f}" cy="{-arc.center.y:.2f}" r="{arc.radius:.2f}" fill="none" stroke="#ff007f" stroke-width="0.8" stroke-dasharray="2,2" />'
            )

        # Draw texts
        for text in container.texts:
            safe_txt = text.text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            svg_parts.append(
                f'<text x="{text.position.x:.2f}" y="{-text.position.y:.2f}" fill="#ffffff" font-size="{max(text.height, 8):.1f}" font-family="sans-serif">{safe_txt}</text>'
            )

        svg_parts.append('</svg>')
        return "".join(svg_parts)

preview_service = PreviewService()
