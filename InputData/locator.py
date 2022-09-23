# Importing all the required libraries
from os import spawnl
import pickle
import pandas as pd
import numpy as np
import pymongo

# Importing all the functions from the created files
from API.api_gathering import*
from Database.database import*
from View.start_view import*
from View.final_view import*
from math_logic import*

header_1()

header_2()

# Importing all the data from the json file that was created after pre-processing
df = pd.read_json('./ProcessedData/cleaned_companies.json')
cols = ['_id', 'name', 'founded_year', 'category_code','deadpooled_year', 'total_money_raised_USD', 'num_offices','office_1_longitude','office_1_latitude', 'office_1_location', 'office_1_city','office_1_state_code','office_1_country_code']
df = df[cols]

# Importing database and collection where the updated data was stored
db, coll = details_fecthing('GeoSpatialAnalysis','companies_cleaned')
companies = list(coll.find())

# Taking into consideration the money factor for finding the location of your company
header_money()
inputmoney = Integer_Input()
print("\n Loading your input in the system")

successful_tech_startups = list(coll.find({'$and':[{'$or':[{'category_code':'semiconductor'},{'category_code':'network_hosting'},{'category_code':'consulting'},{'category_code':'design'},{'category_code':'hardware'},{'category_code':'nanotech'},{'category_code':'mobile'},{'category_code':'games_video'},{'category_code':'cleantech'},{'category_code':'software'},{'category_code':'analytics'},{'category_code':'web'},{'category_code':'biotech'}]},{'deadpooled_year': np.nan},{'founded_year':{'$gte':1999}},{'total_money_raised_USD':{'$gte':inputmoney}}]}))

startups_and_near_companies = []
possible_offices_criterion_1 = []

# Considering office_1_location as 2d sphere index for geo spatial analysis in mongoDB
coll.create_index([("office_1_location", pymongo.GEOSPHERE)])

# Calculating the companies present near the location obtained based on the requirements of your compnay
for e in successful_tech_startups:
        
    if(e["office_1_location"]!={}):
            
        near_companies = Near_companies(e['office_1_location']['coordinates'][0],e['office_1_location']['coordinates'][1],3000)
        temp = []
        temp.append([e['_id'], e['name'], e['founded_year'], e['category_code'], e['total_money_raised'], e['office_1_longitude'], e['office_1_latitude']])
        temp.append([near_companies[i]['name'] for i in range(len(near_companies)) if near_companies[i]['name'] != e['name']])    
        startups_and_near_companies.append(temp)
        for f in near_companies:
            if f['_id'] != e['name']:
                possible_offices_criterion_1.append(f['_id'])

possible_offices_c1 = list(set(possible_offices_criterion_1))

# Taking into consideration the age factor of the company for finding the location of your company
header_year()
inputyears = Integer_Input()
print("\n Loading your input in the system")

old_companies = list(coll.find({'$and':[{'deadpooled_year': np.nan},{'founded_year':{'$lte':2019-inputyears}}]}))

not_possible_offices_criterion_2 = []
for e in old_companies:

    if(e["office_1_location"]!={}):
        near_companies = Near_companies(e['office_1_location']['coordinates'][0],e['office_1_location']['coordinates'][1],3000)
        for f in near_companies:
            if f['_id'] != e['name']:
                not_possible_offices_criterion_2.append(f['_id'])

not_possible_offices_c2 = list(set(not_possible_offices_criterion_2))

possible_offices_c1_c2 = common_values(possible_offices_c1, not_possible_offices_c2)
possible_offices_c1_c2_coords = office_coordinates(possible_offices_c1_c2, companies)

# Taking into consideration the airport distance factor of the company for finding the location of your company
header_airports()
airports_df = pd.read_csv('./InputData/airports.csv', header=None,usecols=[1,2,3,4,6,7,12], names=['FacilityName', 'City', 'Country','3CharCode','Lat','Long','FacilityType'])
airports_df = airports_df[airports_df['FacilityType']=='airport']
airports_df.reset_index(drop=True, inplace=True)
distances = calculate_Distance(possible_offices_c1_c2_coords, airports_df)
office_airports = Closer_Airports(distances, possible_offices_c1_c2, airports_df)
possible_offices_c1_c2_c3 = []
for e in office_airports:
    if len(e) >= 2:
        possible_offices_c1_c2_c3.append(e[0])
    
possible_offices_c1_c2_c3_coords = office_coordinates(possible_offices_c1_c2_c3, companies)

# Taking into consideration the coffee shop factor here you choice was starbucks
header_coffee()
starbucks_list = information_type(possible_offices_c1_c2_c3_coords, possible_offices_c1_c2_c3,'starbucks',500)
cleaned_starbucks_list = clean_List(starbucks_list)

possible_offices_c1_c2_c3_c4 = [e[0] for e in cleaned_starbucks_list]
possible_offices_c1_c2_c3_c4_coords = office_coordinates(possible_offices_c1_c2_c3_c4, companies)

# Taking into consideration the school factor here for finding the location of your company
header_school()
school_list = information_type(possible_offices_c1_c2_c3_c4_coords, possible_offices_c1_c2_c3_c4,'school',500)
cleaned_school_list = clean_List(school_list)

possible_offices_c1_c2_c3_c4_c5 = [e[0] for e in cleaned_school_list]
possible_offices_c1_c2_c3_c4_c5_coords = office_coordinates(possible_offices_c1_c2_c3_c4, companies)

possible_offices_c1_c2_c3_c4_to_string = [str(e) for e in possible_offices_c1_c2_c3_c4]

# Checking an important condition to proceed with the search of location for your company
cond = len(possible_offices_c1_c2_c3_c4_coords)
if cond < 1:
    print('''We are sorry, there aren't any available locations for your company in our database.''')

else:
    print('''Please wait, in a few seconds we will offer you the perfect location for your company!''')

# Starting to create the filetered dataframe that will be converted to csv and will be input in the final map
indexs = []
for i in range(len(df)):
    if df['_id'][i] in possible_offices_c1_c2_c3_c4_to_string:
        indexs.append(i)
df_filtered = df.iloc[indexs]
df_filtered.reset_index(drop=True, inplace=True)

df_filtered = df_filtered[['_id', 'name', 'office_1_longitude', 'office_1_latitude', 'office_1_city','office_1_country_code']]

# Creating new columns to store the obtained infromation based on the requirements
df_filtered['starbucks_lat'] = Lat_Venue(cleaned_starbucks_list, df_filtered)
df_filtered['starbucks_long'] = Long_Venue(cleaned_starbucks_list, df_filtered)
df_filtered['starbucks_dist'] = Distance_Venue(cleaned_starbucks_list, df_filtered)
df_filtered['shope_name_type'] = Name_Venue(cleaned_starbucks_list, df_filtered)

df_filtered['school_lat'] = Lat_Venue(cleaned_school_list, df_filtered)
df_filtered['school_long'] = Long_Venue(cleaned_school_list, df_filtered)
df_filtered['school_dist'] = Distance_Venue(cleaned_school_list, df_filtered)
df_filtered['school_name_type'] = Name_Venue(cleaned_school_list, df_filtered)

# Further priortizing one condition to obtain effecient results
print('''What do you prefer to have closer? A Starbucks (then enter 1), A School (then enter 2)?''')  
cc = DelimitedInteger_Input()           
if cc == 1:
    sortby = 'starbucks_dist'
elif cc == 2:
    sortby = 'school_dist'

df_filtered = df_filtered.sort_values([sortby], ascending=[True])
e = [df_filtered.iloc[0][3], df_filtered.iloc[0][2]]

# Associating the airports vicinity condition to the filtered dataframe
name_dist_lat_long_airport = []
for i in range(len(office_airports)):
    if str(office_airports[i][0]) == df_filtered.iloc[0][0]:
        for j in range(1, len(office_airports[i])):
            name_dist_lat_long_airport.append(office_airports[i][j][0])
            name_dist_lat_long_airport.append(office_airports[i][j][1])           
            name_dist_lat_long_airport.append(office_airports[i][j][2])
            name_dist_lat_long_airport.append(office_airports[i][j][3])

# Associating the distance of the mentioned companies from your companies expected location to the filtered dataframe
near_startups = []
for i in range(len(startups_and_near_companies)):
    if df_filtered.iloc[0][1] in startups_and_near_companies[i][1]:
        near_startups.append(startups_and_near_companies[i][0]) 

# Exporting the filtered dataframe into a csv file
df_filtered.to_csv('./OutputData/final.csv', index=False)

# Exporting the filetred dataframe to folium map that will be used to visualize the output
final_map(e, [df_filtered.iloc[0][6], df_filtered.iloc[0][7]],[df_filtered.iloc[0][10], df_filtered.iloc[0][11]], df_filtered.iloc[0][13],name_dist_lat_long_airport,near_startups)