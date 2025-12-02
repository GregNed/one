import json
# Geopandas is a great out-of-the-box tool, but it requires a lot of deps so for such trivial tasks,
# I'd probably try to replace it with plain Shapely + geojson libraries.
import geopandas
# Django would be an overkill with all its scaffolding, and Flask is a bit too barebones.
from fastapi import FastAPI

ISRAEL_EPSG = 2039

gdf_spherical = geopandas.read_file("./tel_aviv_points.geojson")
# The GeoJSON format uses spherical coordinates, since they are unambiguous and universal.
# But computations on the sphere are orders of magnitude heavier than planar. Planar computations are subject to projection distortions.
# However, since we're doing computations on a small scale (within a city/region), the distortion is negligible and is preferred
# over the computational cost. Also, most of the geospatial libraries use planar coordinates for performance reasons.
# However, we're using the spherical coordinates for the API response to present the response in a universal format.
gdf_projected = gdf_spherical.to_crs(epsg=ISRAEL_EPSG)
app = FastAPI()


@app.get("/all/")
async def show_all():
    """Return all points in the file."""
    return json.loads(gdf_spherical.to_json())

@app.get("/within/")
async def distance(poi_name: str, radius: int):
    """Return all points within a radius of a given point, specified by name, as expected, e.g. in an end-user application."""
    poi = gdf_projected[gdf_projected["name"] == poi_name].iloc[0]
    points_within_radius = gdf_projected[gdf_projected.dwithin(poi.geometry, radius, align=True)]
    return json.loads(points_within_radius.to_crs(epsg=4326).to_json())

