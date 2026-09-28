import math
from sqlalchemy.orm import Session
from app.models.citizen_request import CitizenRequest
from app.schemas.intelligence import GeographicHotspot, RegionalHotspotsResponse


def compute_regional_hotspots(
    db: Session,
    region_id: int,
    region_name: str,
    grid_size_degree: float = 0.05
) -> RegionalHotspotsResponse:
    requests = (
        db.query(CitizenRequest)
        .filter(
            CitizenRequest.region_id == region_id,
            CitizenRequest.latitude.isnot(None),
            CitizenRequest.longitude.isnot(None)
        )
        .all()
    )
    
    if not requests:
        return RegionalHotspotsResponse(
            region_id=region_id,
            region_name=region_name,
            total_hotspots=0,
            hotspots=[]
        )
        
    # Grid aggregation to protect exact coordinates
    grid_buckets: dict[tuple[float, float], list[CitizenRequest]] = {}
    
    for req in requests:
        # Snap latitude and longitude to grid step
        lat_grid = round(math.floor(req.latitude / grid_size_degree) * grid_size_degree + (grid_size_degree / 2.0), 3)
        lon_grid = round(math.floor(req.longitude / grid_size_degree) * grid_size_degree + (grid_size_degree / 2.0), 3)
        
        cell = (lat_grid, lon_grid)
        if cell not in grid_buckets:
            grid_buckets[cell] = []
        grid_buckets[cell].append(req)
        
    hotspots: list[GeographicHotspot] = []
    hotspot_counter = 1
    
    # Sort grid cells by request volume descending
    sorted_cells = sorted(grid_buckets.items(), key=lambda x: len(x[1]), reverse=True)
    
    for (lat, lon), cell_requests in sorted_cells:
        cat_counts: dict[str, int] = {}
        for r in cell_requests:
            c = r.category or "Uncategorized"
            cat_counts[c] = cat_counts.get(c, 0) + 1
            
        dominant_cat = max(cat_counts.items(), key=lambda x: x[1])[0] if cat_counts else "General"
        
        # Approximate radius based on grid size (~ 5.5 km for 0.05 deg)
        radius_km = round(grid_size_degree * 111.0 / 2.0, 1)
        
        hotspots.append(
            GeographicHotspot(
                hotspot_id=f"HOTSPOT-{region_id:02d}-{hotspot_counter:03d}",
                approx_latitude=lat,
                approx_longitude=lon,
                radius_km=radius_km,
                request_count=len(cell_requests),
                dominant_category=dominant_cat,
                categories=cat_counts
            )
        )
        hotspot_counter += 1
        
    return RegionalHotspotsResponse(
        region_id=region_id,
        region_name=region_name,
        total_hotspots=len(hotspots),
        hotspots=hotspots
    )
