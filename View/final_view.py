# Importing all the required libraries
import os
import re
import folium
import fontawesome as fa
from pathlib import Path
import webbrowser
from colorama import init
init()
from colorama import Fore, Back, Style

def final_map(company,starbucks,school,school_name,name_dist_lat_long_airport,near_startups):

    # Setting up the parameters for the map frame that will be shown as output
    tooltip = 'Click me!'
    map_city = folium.Map(location = company, zoom_start=11)

    # Setting up the vicinity circle
    folium.Circle(radius=2000,location=company,popup='Old companies free zone',color='#3186cc',fill=True,fill_color='#3186cc').add_to(map_city)

    # Setting up the marker for coffee shops we chose "Starbucks"
    folium.Marker(starbucks,radius=2,icon=folium.Icon(icon='coffee', prefix='fa',color='green'),popup='<b>Starbucks</b>',tooltip=tooltip).add_to(map_city)

    # Setting up the marker for school
    folium.Marker(school,radius=2,icon=folium.Icon(icon='graduation-cap', prefix='fa',color='orange'),popup='<b>School</b>',tooltip=tooltip).add_to(map_city)

    # Setting up the marker for airports in our vicinity
    for i in range(0,len(name_dist_lat_long_airport),4):
        folium.Marker([name_dist_lat_long_airport[i+2],name_dist_lat_long_airport[i+3]],radius=2,icon=folium.Icon(icon='plane', prefix='fa',color='blue'),popup=f"<b>Airport</b> '{name_dist_lat_long_airport[i+0]}'. Distance from the office: {int(name_dist_lat_long_airport[i+1])} km",tooltip=tooltip).add_to(map_city)

    # Setting up the marker for your companies location
    folium.Marker(company,radius=2,icon=folium.Icon(icon='briefcase', color='red'),popup='<b>Perfect location for your business</b>',tooltip=tooltip).add_to(map_city)

    # Setting up the marker for the comapnies requested to be in the nearby vivinity based on the money and age requirements
    for j in near_startups:
        category = re.sub("_"," ",j[3].capitalize())
        folium.Marker([j[6], j[5]],radius=2,icon=folium.Icon(icon='building-o', prefix='fa',color='black'),popup=f"<b>[Startup]</b> {j[1]}. Founded year: {int(j[2])}. Category: {category}. Total money raised (USD): {int(j[4])}.",tooltip=tooltip).add_to(map_city)

    map_city.save('./outputdata/map.html')
    url = "file://{}{}{}".format(str(Path(os.getcwd())),"/outputdata", "/map.html")
    webbrowser.open(url, 2)