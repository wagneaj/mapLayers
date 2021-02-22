import streamlit as st
import json
import geopandas as gpd
import matplotlib
import plotly
import plotly.express as px
import contextily as ctx
import streamlit as st
import descartes
import pandas as pd
import numpy as np
import geopandas as gpd
import pyproj
import matplotlib.pyplot as plt
import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode,  iplot

# reading in the leases shapefile
geo_df_leases = gpd.read_file(r"C:\Users\wagneaj\Desktop\Scratch\Streamlit\Shapefiles\leases_clip2.shp")

# project geopandas dataframe
map_df = geo_df_leases
map_df.to_crs(pyproj.CRS.from_epsg(4326), inplace=True)

# reading in the wells shapefile
geo_df_wells = gpd.read_file(r"\\conoco.net\HO_Shared\GGRE_Services_Analytics\Projects\EXPL_AustinChalk_SyntheticWellLog_October2018\Shapefiles\GridJoin_Wells.shp")

# project geopandas dataframe
geo_df_wells.to_crs(pyproj.CRS.from_epsg(4326), inplace=True)

# define lat, long for wells
Lat = geo_df_wells['Lat']
Long = geo_df_wells['Long']

# leases to geojson
path = r"C:\Users\wagneaj\Desktop\Scratch\Streamlit\Shapefiles\geojson.json"

map_df.to_file(path, driver = "GeoJSON")
with open(path) as geofile:
    j_file = json.load(geofile)

#index geojson
i=1
for feature in j_file["features"]:
    feature ['id'] = str(i).zfill(2)
    i += 1
    
# mapbox token
mapboxt = 'pk.eyJ1Ijoid2FnbmVyYWp3IiwiYSI6ImNra2lpN242ZDA0d3gyeHV6YW8xYXRwa2oifQ.b25cbmKgNGefJa2xqkjdLA'

# define layers and plot map
choro = go.Choroplethmapbox(z=map_df['LCN'], locations = map_df.index, colorscale = 'Viridis', geojson = j_file, text = map_df['STATE_CODE'], marker_line_width=0.1)
     # Your choropleth data here


scatt = go.Scattermapbox(lat=Lat,lon=Long,mode='markers+text',below='False', marker=dict( size=12, color ='rgb(56, 44, 100)'))
     # Your scatter data here

layout = go.Layout(title_text ='Wells & Leases', title_x =0.5, width=750, height=700,mapbox = dict(center= dict(lat=37, lon=-95),accesstoken= mapboxt, zoom=6,style="stamen-terrain"))
    

# streamlit multiselect widget
layer1 = st.multiselect('Layer 1', [choro, scatt], format_func=lambda x: 'Leases' if x==choro else 'Wells')


#st.write('Layer 1:', layer1)
fig = go.Figure(data=layer1, layout=layout)

# display streamlit
# display streamlit
st.plotly_chart(fig)

