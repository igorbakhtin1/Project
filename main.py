import geopandas as gpd
import pandas as pd
import numpy as np
import json
import h3
import folium
import osmnx as ox
from shapely import wkt
from folium.plugins import HeatMap
from shapely.geometry import Polygon


def visualize_hexagons(hexagons, color="red", folium_map=None):
    polylines = []
    lat = []
    lng = []
    for hex in hexagons:
        polygons = h3.h3_set_to_multi_polygon([hex], geo_json=False)
        outlines = [loop for polygon in polygons for loop in polygon]
        polyline = [outline + [outline[0]] for outline in outlines][0]
        lat.extend(map(lambda v: v[0], polyline))
        lng.extend(map(lambda v: v[1], polyline))
        polylines.append(polyline)

    if folium_map is None:
        m = folium.Map(location=[sum(lat) / len(lat), sum(lng) / len(lng)], zoom_start=20, tiles='cartodbpositron')
    else:
        m = folium_map

    for polyline in polylines:
        my_PolyLine = folium.PolyLine(locations=polyline, weight=8, color=color)
        m.add_child(my_PolyLine)
    return m


h3_address = h3.geo_to_h3(45.035470, 38.975313, 9)  # 9 - индекс, определяющий размер гексагона
visualize_hexagons([h3_address])