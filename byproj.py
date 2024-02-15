from pyproj import CRS
from pprint import pprint
from pyproj import Transformer

wgs84 = CRS.from_string("EPSG:4326")
utm48n = CRS.from_string("EPSG:32648")

wgs84_to_utm48 = Transformer.from_crs(wgs84, utm48n)

dt = [crs.to_wkt(pretty=True) for crs in [wgs84, utm48n]]

# pprint(dt)

print(wgs84_to_utm48.transform(53.5799906986,103.4574251838))
