from typing import Tuple

# Standard AutoCAD Color Index (ACI) RGB approximations for standard 1-7 colors
ACI_PALETTE = {
    1: (255, 0, 0),     # Red
    2: (255, 255, 0),   # Yellow
    3: (0, 255, 0),     # Green
    4: (0, 255, 255),   # Cyan
    5: (0, 0, 255),     # Blue
    6: (255, 0, 255),   # Magenta
    7: (255, 255, 255), # White/Black
    8: (128, 128, 128), # Dark Grey
    9: (192, 192, 192), # Light Grey
}

def rgb_to_aci(rgb: Tuple[float, float, float]) -> int:
    """
    Converts a normalized (0.0-1.0) or (0-255) RGB tuple to nearest AutoCAD Color Index (ACI).
    Default returns 7 (BYLAYER / Standard White/Black) if near black/white.
    """
    if not rgb:
        return 7
    
    r, g, b = rgb
    if max(r, g, b) <= 1.0:
        r, g, b = int(r * 255), int(g * 255), int(b * 255)
    else:
        r, g, b = int(r), int(g), int(b)
        
    # Check for near black/white
    if (r + g + b) / 3 < 30:
        return 7 # Standard CAD color on dark background
    if (r + g + b) / 3 > 240:
        return 7

    best_aci = 7
    min_dist = float('inf')
    
    for aci, (pr, pg, pb) in ACI_PALETTE.items():
        dist = (r - pr) ** 2 + (g - pg) ** 2 + (b - pb) ** 2
        if dist < min_dist:
            min_dist = dist
            best_aci = aci
            
    return best_aci

def rgb_to_hex(rgb: Tuple[float, float, float]) -> str:
    """Converts RGB tuple to hex string."""
    if not rgb:
        return "#FFFFFF"
    r, g, b = rgb
    if max(r, g, b) <= 1.0:
        r, g, b = int(r * 255), int(g * 255), int(b * 255)
    return f"#{int(r):02x}{int(g):02x}{int(b):02x}"
