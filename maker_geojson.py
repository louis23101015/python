import os
import geopandas
import pandas as pd
from shapely.geometry import MultiPolygon

cwd = os.path.join(os.getcwd(), 'area_info')
folders = [x for x in os.listdir(cwd) if not os.path.isfile(x)]
shp_files = [os.path.join(cwd, x, "TL_SCCO_SIG.shp") for x in folders]
shp_files

geodf = geopandas.GeoDataFrame()

for file in shp_files:
    temp = geopandas.read_file(file, encoding='cp949')
    geodf = pd.concat([geodf, temp], sort=False).reset_index(drop=True)
    

geodf.to_file('법정구역_시군구.geojson', driver='GeoJSON')



def filter_small_polygons(multi_polygon, threshold_area):
    filtered_polygons = []
    if type(multi_polygon) == MultiPolygon:
        for polygon in list(multi_polygon.geoms):
            if polygon.area >= threshold_area:
                filtered_polygons.append(polygon)
        
        return MultiPolygon(filtered_polygons)
    else:
        return multi_polygon
    
    
geodf['geometry'] = geodf['geometry'].apply(lambda x: filter_small_polygons(x, threshold_area=7000000))

geodf['geometry'] = geodf['geometry'].simplify(100)

geodf = geodf.set_crs(epsg=5179)
geodf = geodf.to_crs(epsg=4326)

geodf.to_file('법정구역_시군구.geojson', driver='GeoJSON')