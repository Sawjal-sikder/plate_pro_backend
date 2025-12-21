import math
import ezdxf
import io


def polygon_area(points):
    """Calculate the area of a polygon using the Shoelace formula."""
    area = 0
    n = len(points)
    for i in range(n):
        x1, y1 = points[i]
        x2, y2 = points[(i + 1) % n]
        area += (x1 * y2) - (x2 * y1)
    return abs(area) / 2


def calculate_area(corners, holes):
    """
    Calculate the net area of a plate shape.
    
    Args:
        corners: List of corner dictionaries with x, y, radius
        holes: List of hole dictionaries with x, y, radius
    
    Returns:
        Dictionary containing area calculations
    """
    # Convert corners to points for area calculation
    corner_points = [(corner['x'], corner['y']) for corner in corners]
    
    # Calculate outer area
    outer_area = polygon_area(corner_points)
    
    # Calculate hole area
    hole_area = sum(math.pi * hole['radius']**2 for hole in holes) if holes else 0
    
    # Calculate net area
    net_area_sq_units = outer_area - hole_area
    net_area_sqft = net_area_sq_units / 144  # if 1 unit = 1 inch
    net_area_sqm = net_area_sqft * 0.092903  # square feet to square meters
    
    return {
        "outer_area": round(outer_area, 2),
        "hole_area": round(hole_area, 2),
        "net_area_sq_units": round(net_area_sq_units, 2),
        "net_area_sqft": round(net_area_sqft, 2),
        "net_area_sqm": round(net_area_sqm, 2),
        "unit": "square units (assumed inches)"
    }


def generate_dxf(corners, holes, filename="shape.dxf"):
    """
    Generate an AutoCAD DXF file from corner and hole data.
    
    Args:
        corners: List of corner dictionaries with x, y, radius
        holes: List of hole dictionaries with x, y, radius
        filename: Name of the output DXF file
    
    Returns:
        BytesIO object containing the DXF file data
    """
    # Create a new DXF document
    doc = ezdxf.new('R2010')
    msp = doc.modelspace()
    
    # Draw outer boundary
    corner_points = [(corner['x'], corner['y']) for corner in corners]
    msp.add_lwpolyline(corner_points, close=True)
    
    # Draw holes as circles
    if holes:
        for hole in holes:
            msp.add_circle(
                center=(hole['x'], hole['y']),
                radius=hole['radius']
            )
    
    # Save to BytesIO object for in-memory handling
    dxf_buffer = io.BytesIO()
    # Write DXF content as text to BytesIO
    dxf_stream = io.StringIO()
    doc.write(dxf_stream)
    dxf_content = dxf_stream.getvalue()
    dxf_buffer.write(dxf_content.encode('utf-8'))
    dxf_buffer.seek(0)
    
    return dxf_buffer
