import time
import math
from typing import List, Dict, Tuple, Set
import numpy as np
from shapely.geometry import LineString, MultiLineString, Point
from shapely.ops import linemerge

from backend.models.conversion import (
    ParsedGeometryContainer, LineEntity, PolylineEntity, ArcEntity,
    CircleEntity, EllipseEntity, SplineEntity, TextEntity, Point2D
)
from backend.utils.logger import logger

class GeometryOptimizer:
    """
    Automatic CAD Geometry Optimizer:
    1. Removes duplicate lines and reverse-direction overlaps.
    2. Merges connected line segments into continuous LWPOLYLINEs using Shapely linemerge.
    3. Removes zero-length segments and redundant collinear points.
    4. Snaps nearly identical endpoints within configurable tolerance (e.g., 0.0001 mm).
    """

    def __init__(self, snap_tolerance: float = 0.0001, remove_duplicates: bool = True, join_segments: bool = True):
        self.snap_tolerance = snap_tolerance
        self.remove_duplicates = remove_duplicates
        self.join_segments = join_segments

    def optimize(self, container: ParsedGeometryContainer) -> Tuple[ParsedGeometryContainer, Dict]:
        start_time = time.time()
        initial_counts = container.entity_counts()

        optimized = ParsedGeometryContainer()
        optimized.arcs = container.arcs
        optimized.circles = container.circles
        optimized.ellipses = container.ellipses
        optimized.splines = container.splines
        optimized.texts = container.texts

        # 1. Process Lines & Polylines
        raw_lines = container.lines
        raw_polys = container.polylines

        # Extract line segments
        all_segments: List[Tuple[Tuple[float, float], Tuple[float, float], Tuple[float, float, float], float, str]] = []

        for line in raw_lines:
            p1 = self._snap_pt(line.start)
            p2 = self._snap_pt(line.end)
            if self._distance(p1, p2) > self.snap_tolerance:
                all_segments.append((p1, p2, line.color, line.width, line.layer))

        for poly in raw_polys:
            pts = poly.points
            for i in range(len(pts) - 1):
                p1 = self._snap_pt(pts[i])
                p2 = self._snap_pt(pts[i+1])
                if self._distance(p1, p2) > self.snap_tolerance:
                    all_segments.append((p1, p2, poly.color, poly.width, poly.layer))

        # 2. Deduplicate Lines if requested
        if self.remove_duplicates:
            all_segments = self._deduplicate_segments(all_segments)

        # 3. Join consecutive segments into LWPOLYLINEs
        if self.join_segments and all_segments:
            final_lines, final_polys = self._join_segments(all_segments)
            optimized.lines = final_lines
            optimized.polylines = final_polys
        else:
            optimized.lines = [
                LineEntity(
                    start=Point2D(s[0][0], s[0][1]),
                    end=Point2D(s[1][0], s[1][1]),
                    color=s[2],
                    width=s[3],
                    layer=s[4]
                ) for s in all_segments
            ]

        elapsed_time = round(time.time() - start_time, 4)
        final_counts = optimized.entity_counts()

        initial_total = initial_counts["total"]
        final_total = final_counts["total"]
        opt_percent = 0.0
        if initial_total > 0:
            opt_percent = round(((initial_total - final_total) / initial_total) * 100, 2)

        stats = {
            "original_counts": initial_counts,
            "optimized_counts": final_counts,
            "optimization_percentage": opt_percent,
            "execution_time_seconds": elapsed_time
        }

        logger.info(f"Optimization finished in {elapsed_time}s. Reduction: {opt_percent}% ({initial_total} -> {final_total} entities)")
        return optimized, stats

    def _snap_pt(self, pt: Point2D) -> Tuple[float, float]:
        tol = self.snap_tolerance
        x = round(pt.x / tol) * tol if tol > 0 else pt.x
        y = round(pt.y / tol) * tol if tol > 0 else pt.y
        return (round(x, 4), round(y, 4))

    def _distance(self, p1: Tuple[float, float], p2: Tuple[float, float]) -> float:
        return math.hypot(p2[0] - p1[0], p2[1] - p1[1])

    def _deduplicate_segments(self, segments: List[Tuple]) -> List[Tuple]:
        seen: Set[Tuple] = set()
        deduped = []
        for p1, p2, color, width, layer in segments:
            # Canonical segment representation (sorted endpoints)
            if p1 > p2:
                key = (p2, p1, layer)
            else:
                key = (p1, p2, layer)

            if key not in seen:
                seen.add(key)
                deduped.append((p1, p2, color, width, layer))
        return deduped

    def _join_segments(self, segments: List[Tuple]) -> Tuple[List[LineEntity], List[PolylineEntity]]:
        lines_out: List[LineEntity] = []
        polys_out: List[PolylineEntity] = []

        # Group by layer & color
        groups: Dict[Tuple, List] = {}
        for seg in segments:
            key = (seg[4], seg[2])  # (layer, color)
            if key not in groups:
                groups[key] = []
            groups[key].append(seg)

        for (layer, color), group_segs in groups.items():
            shapely_lines = [LineString([s[0], s[1]]) for s in group_segs]
            merged = linemerge(shapely_lines)

            if isinstance(merged, LineString):
                merged_list = [merged]
            elif isinstance(merged, MultiLineString):
                merged_list = list(merged.geoms)
            else:
                merged_list = []

            for geom in merged_list:
                coords = list(geom.coords)
                # Clean collinear points
                cleaned_coords = self._clean_collinear_points(coords)
                
                if len(cleaned_coords) == 2:
                    lines_out.append(LineEntity(
                        start=Point2D(cleaned_coords[0][0], cleaned_coords[0][1]),
                        end=Point2D(cleaned_coords[1][0], cleaned_coords[1][1]),
                        color=color,
                        layer=layer
                    ))
                elif len(cleaned_coords) > 2:
                    is_closed = (cleaned_coords[0] == cleaned_coords[-1])
                    polys_out.append(PolylineEntity(
                        points=[Point2D(c[0], c[1]) for c in cleaned_coords],
                        is_closed=is_closed,
                        color=color,
                        layer=layer
                    ))

        return lines_out, polys_out

    def _clean_collinear_points(self, coords: List[Tuple[float, float]]) -> List[Tuple[float, float]]:
        if len(coords) <= 2:
            return coords

        cleaned = [coords[0]]
        for i in range(1, len(coords) - 1):
            p_prev = cleaned[-1]
            p_curr = coords[i]
            p_next = coords[i+1]

            # Cross product to check collinearity
            cross = (p_curr[0] - p_prev[0]) * (p_next[1] - p_prev[1]) - (p_curr[1] - p_prev[1]) * (p_next[0] - p_prev[0])
            if abs(cross) > 1e-4:
                cleaned.append(p_curr)

        cleaned.append(coords[-1])
        return cleaned
