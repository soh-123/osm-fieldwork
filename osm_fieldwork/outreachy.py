from io import BytesIO
from osm_fieldwork.basemapper import create_basemap_file

with open("tests/testdata/Rollinsville.geojson", "rb") as geojson_file:
    boundary = geojson_file.read()  # read as a `bytes` object.
    boundary_bytesio = BytesIO(boundary)   # add to a BytesIO wrapper

create_basemap_file(
    verbose=True,
    boundary=boundary_bytesio,
    outfile="outreachy.mbtiles",
    zooms="12-15",
    source="esri",
)

# create_basemap_file(
#     verbose=True,
#     boundary="-4.730494,41.650541,-4.725634,41.652874",
#     outfile="outreachy.mbtiles",
#     zooms="12-15",
#     source="esri",
# )