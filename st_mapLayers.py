import streamlit as st
import json
import geopandas as gpd
import pyproj
import plotly.graph_objs as go

# reading in the polygon shapefile
polygon = gpd.read_file(r"Downloads\CityBoundaries.shp")

# project geopandas dataframe
map_df = polygon
map_df.to_crs(pyproj.CRS.from_epsg(4326), inplace=True)

# reading in the points shapefile
points = gpd.read_file(r"Downloads\USA_Major_Cities.shp")

# project geopandas dataframe
points.to_crs(pyproj.CRS.from_epsg(4326), inplace=True)

# define lat, long for ponints
Lat = points['Lat']
Long = points['Long']

# leases to geojson
path = r"C:\Users\project\geojson.json"

map_df.to_file(path, driver = "GeoJSON")
with open(path) as geofile:
    j_file = json.load(geofile)

#index geojson
i=1
for feature in j_file["features"]:
    feature ['id'] = str(i).zfill(2)
    i += 1
    
# mapbox token
mapboxt = 'MapBox Token'

# define layers and plot map
choro = go.Choroplethmapbox(z=map_df['STFIPS'], locations = map_df.index, colorscale = 'Viridis', geojson = j_file, text = map_df['NAME'], marker_line_width=0.1)
     # Your choropleth data here


scatt = go.Scattermapbox(lat=Lat,lon=Long,mode='markers+text',below='False', marker=dict( size=12, color ='rgb(56, 44, 100)'))
     # Your scatter data here

layout = go.Layout(title_text ='USA Cities', title_x =0.5, width=950, height=700,mapbox = dict(center= dict(lat=37, lon=-95),accesstoken= mapboxt, zoom=4,style="stamen-terrain"))
    

# streamlit multiselect widget
layer1 = st.multiselect('Layer Selection', [choro, scatt], format_func=lambda x: 'Polygon' if x==choro else 'Points')


#st.write('Layer 1:', layer1)
fig = go.Figure(data=layer1, layout=layout)


# display streamlit
st.plotly_chart(fig)

