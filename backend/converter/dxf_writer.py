import ezdxf
from ezdxf.enums import TextEntityAlignment
from typing import Dict
from backend.models.conversion import ParsedGeometryContainer
from backend.utils.color_utils import rgb_to_aci
from backend.utils.logger import logger

VERSION_MAP: Dict[str, str] = {
    "R12": "R12",
    "R14": "R12",   # ezdxf handles R14 export using R12 standard structure
    "2000": "R2000",
    "2004": "R2004",
    "2007": "R2007",
    "2010": "R2010",
    "2013": "R2013",
    "2018": "R2018"
}

class DXFWriter:
    """
    DXF Document Builder using ezdxf.
    Supports versions: R12, R14, 2000, 2004, 2007, 2010, 2013, 2018.
    """

    def __init__(self, version: str = "2018"):
        ezdxf_version = VERSION_MAP.get(version.upper(), "R2018")
        self.doc = ezdxf.new(dxfversion=ezdxf_version)
        self.msp = self.doc.modelspace()
        self.version_str = ezdxf_version
        self._setup_layers()

    def _setup_layers(self):
        """Pre-configure standard CAD layers."""
        layers = ["0", "GEOMETRY", "TEXT", "DIMENSIONS", "ANNOTATION"]
        for layer_name in layers:
            if layer_name not in self.doc.layers:
                self.doc.layers.add(layer_name)

    def write(self, container: ParsedGeometryContainer, output_path: str):
        logger.info(f"Writing DXF (Version {self.version_str}) with {container.total_entities()} entities to {output_path}")

        # 1. Add Lines
        for line in container.lines:
            aci_color = rgb_to_aci(line.color)
            self.msp.add_line(
                start=line.start.to_tuple(),
                end=line.end.to_tuple(),
                dxfattribs={
                    "layer": line.layer or "0",
                    "color": aci_color
                }
            )

        # 2. Add Polylines
        for poly in container.polylines:
            pts = [p.to_tuple() for p in poly.points]
            aci_color = rgb_to_aci(poly.color)
            if self.version_str == "R12":
                self.msp.add_polyline2d(
                    pts,
                    dxfattribs={
                        "layer": poly.layer or "0",
                        "color": aci_color,
                        "flags": 1 if poly.is_closed else 0
                    }
                )
            else:
                self.msp.add_lwpolyline(
                    pts,
                    format="xy",
                    dxfattribs={
                        "layer": poly.layer or "0",
                        "color": aci_color,
                        "flags": 1 if poly.is_closed else 0
                    }
                )

        # 3. Add Arcs
        for arc in container.arcs:
            aci_color = rgb_to_aci(arc.color)
            self.msp.add_arc(
                center=arc.center.to_tuple(),
                radius=arc.radius,
                start_angle=arc.start_angle,
                end_angle=arc.end_angle,
                dxfattribs={
                    "layer": arc.layer or "0",
                    "color": aci_color
                }
            )

        # 4. Add Circles
        for circle in container.circles:
            aci_color = rgb_to_aci(circle.color)
            self.msp.add_circle(
                center=circle.center.to_tuple(),
                radius=circle.radius,
                dxfattribs={
                    "layer": circle.layer or "0",
                    "color": aci_color
                }
            )

        # 5. Add Ellipses
        for ellipse in container.ellipses:
            aci_color = rgb_to_aci(ellipse.color)
            if self.version_str != "R12":
                self.msp.add_ellipse(
                    center=ellipse.center.to_tuple(),
                    major_axis=ellipse.major_axis.to_tuple(),
                    ratio=ellipse.ratio,
                    start_param=ellipse.start_param,
                    end_param=ellipse.end_param,
                    dxfattribs={
                        "layer": ellipse.layer or "0",
                        "color": aci_color
                    }
                )

        # 6. Add Splines
        for spline in container.splines:
            aci_color = rgb_to_aci(spline.color)
            pts = [p.to_tuple() for p in spline.control_points]
            if len(pts) >= 2:
                if self.version_str == "R12":
                    # Fallback to 2D polyline for R12
                    self.msp.add_polyline2d(pts, dxfattribs={"layer": spline.layer or "0", "color": aci_color})
                else:
                    try:
                        self.msp.add_spline(fit_points=pts, dxfattribs={"layer": spline.layer or "0", "color": aci_color})
                    except Exception:
                        self.msp.add_lwpolyline(pts, format="xy", dxfattribs={"layer": spline.layer or "0", "color": aci_color})

        # 7. Add Text / MText
        for text in container.texts:
            aci_color = rgb_to_aci(text.color)
            layer_name = text.layer or "TEXT"
            if text.is_mtext and self.version_str != "R12":
                mtext = self.msp.add_mtext(
                    text.text,
                    dxfattribs={
                        "layer": layer_name,
                        "color": aci_color,
                        "char_height": max(text.height, 1.0)
                    }
                )
                mtext.set_location(insert=text.position.to_tuple(), rotation=text.rotation)
            else:
                txt_entity = self.msp.add_text(
                    text.text,
                    dxfattribs={
                        "layer": layer_name,
                        "color": aci_color,
                        "height": max(text.height, 1.0),
                        "rotation": text.rotation
                    }
                )
                txt_entity.set_placement(text.position.to_tuple(), align=TextEntityAlignment.LEFT)

        # Save DXF file
        self.doc.saveas(output_path)
        logger.info(f"Successfully saved DXF file to {output_path}")
