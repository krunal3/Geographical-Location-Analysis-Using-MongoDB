# Importing all the required libraries
import os
import requests
import json
from dotenv import load_dotenv
load_dotenv()

# In this project we will be using 2 API's
# 1) Exchange rate API
# 2) Four square API
# We will be defining function for respected API's to establish connection and fetch data

# Exchange rate API
def exchangerate_api(currency):

    # Establishing the connection
    link = "https://v6.exchangerate-api.com/v6/75c08290a84511db5965e5d7/latest/{}".format(currency)
    result = requests.get(link)

    return result

# Four square API

# Defining function to authorize the connection
def foursquare_api(request,latitude,longitude,myquery,limit,radius):

    # Using the required credentials for connection and the details of all the params can be obtained from the API documentation
    url = "https://api.foursquare.com/v3/places/{}".format(request)
    headers = {"Accept": "application/json","Authorization": "fsq319fG/++xpixV/12l770mf7eIsaQZh2KGVIDxru9JlNo="}
    params = dict(ll='{},{}'.format(latitude,longitude),query= myquery,limit=limit,radius=radius)

    # Predefining the radius to avoid confusion
    radius = 500

    resp = requests.get(url=url, params=params,headers=headers)
    return json.loads(resp.text)

# Defining the function to fecth the required data from API
def information_type(coords, offices, type , radius):
    # Creating a list to store all the data
    collected_data = []
    l = len(coords)

    # collecting the data in segements and stroing it in the list created above
    for i in range(l):
        data = foursquare_api('search', coords[i]['coordinates'][1],coords[i]['coordinates'][0], type,1,radius)
        collected_data.append([offices[i],data])

    return collected_data