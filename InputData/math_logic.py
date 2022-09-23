# Importing all the required libraries
import pandas as pd
import numpy as np
import geopy.distance

# Defining basic functions to make the locator.py and preprocessing.py easy to compile.

# Defining the key value set for dictionary
def key_set(dictionary, key, value):
    if key not in dictionary:
        dictionary[key] = value
    elif type(dictionary[key]) == list:
        dictionary[key].append(value)
    else:
        dictionary[key] = [dictionary[key], value]

# Defining a function to find common values between two list
def common_values(List1, List2):
    temp = []
    for e in List1:
        if e not in List2:
            temp.append(e)
    return temp

# Defining a function to return the coordinates
def office_coordinates(officesID, collection):
    temp = []
    for f in officesID:
        for e in collection:
            if e['_id'] == f:
                temp.append(e['office_1_location'])
    return temp

# Defining a function to clean the list as per the requirements
def clean_List(venueList):
    temp = []
    for i in range(len(venueList)):
        if len(venueList[i][1]['results']) > 0:
            temp.append([venueList[i][0],
                venueList[i][1]['results'][0]["geocodes"]["main"]["latitude"],
                venueList[i][1]['results'][0]["geocodes"]["main"]["longitude"],
                venueList[i][1]['results'][0]['distance'],
                venueList[i][1]['results'][0]['location']['formatted_address'],
                venueList[i][1]["results"][0]["categories"][0]["name"]])
    return temp

# Defining a function to obatin the latitude
def Lat_Venue(venueList, df):
    temp = []
    for j in range(len(df)):
        for i in range(len(venueList)):
            if df.iloc[j][0] == str(venueList[i][0]):
                temp.append(venueList[i][1])
    return temp
    
# Defining a function to obtain the longitude
def Long_Venue(venueList, df):
    temp = []
    for j in range(len(df)):
        for i in range(len(venueList)):
            if df.iloc[j][0] == str(venueList[i][0]):
                temp.append(venueList[i][2])   
    return temp

# Defining a function to obtain the distance
def Distance_Venue(venueList, df):
    temp = []
    for j in range(len(df)):
        for i in range(len(venueList)):
            if df.iloc[j][0] == str(venueList[i][0]):
                temp.append(venueList[i][3])     
    return temp

# Defining a function to obtain the name
def Name_Venue(venueList, df):
    temp = []
    for j in range(len(df)):
        for i in range(len(venueList)):
            if df.iloc[j][0] == str(venueList[i][0]):
                temp.append(venueList[i][5])    
    return temp

# Defining a function for integere input
def Integer_Input():
    while True:
        get_input = input('n = ')
        try:
            get_input = int(get_input)
            break
        except ValueError:
            print('A valid integer should be entered')
            continue
    return get_input

# Defining a function to provide a delimiter for integer input
def DelimitedInteger_Input():
    while True:
        order = input('Mention your priority = ')
        try:
            order = int(order)
            if order > 0 and order < 5:
                break
            else:
                print('Please enter a valid integer: 1 for Starbucks and 2 for School.') 
        except ValueError:
            print('Please enter a valid integer: 1 for Starbucks and 2 for School.')
            continue
    return order

# Defining a function to calculate distance between two coordinates
def calculate_Distance(x,y):
    distances_temp = []
    for e in x:
        coords_1 = (e['coordinates'][1], e['coordinates'][0])
        dist = []
        for i in range(len(y)):
            coords_2 = (y.at[i,'Lat'],y.at[i,'Long'])
            dist.append(geopy.distance.geodesic(coords_1, coords_2).km)
        distances_temp.append(dist)   
    return distances_temp

# Defining a function to obtain information about the aiports
def Closer_Airports(distances, offices, airports):
    office_airports = []
    for i in range(len(distances)):
        temp = []
        temp.append(offices[i])
        for j in range(len(distances[i])):
            if distances[i][j] <= 20:
                temp.append([airports.at[j,'FacilityName'],
                            distances[i][j],
                            airports.at[j,'Lat'],
                            airports.at[j,'Long']])
        office_airports.append(temp)
    return office_airports
