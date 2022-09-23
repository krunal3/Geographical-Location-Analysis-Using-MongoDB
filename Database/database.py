# Importing all the required libraries
import pymongo
from pymongo import MongoClient

# Intializing the mongoDB connection for the project
base = MongoClient('localhost',27017)

# Creating a function to fetch the database and collection from the database
def details_fecthing(database_name,collection_name):

    # Fetching the database details
    db = base[database_name]
    # Fetching the collection details
    col = db[collection_name]

    return db,col

# Defining a function to create a GeoJson object using the cooridnates mentioned
def location_object(longitude,latitude):

    # Creating the GeoJson object
    loc = {'type':'point','coordinates':[longitude,latitude]}

    return loc


# Defining a function to obtain all the companies in the vicinity of the location obtained from the above function
def Near_companies(longitude,latitude,max_dist):

    # Fetching the database and collection details from the above metnioned function
    db,col = details_fecthing('GeoSpatialAnalysis','companies_cleaned')

    # Setting the vicnity distance to 3km = 3000m
    max_dist = 3000

    # Storing the corrdinates of all the companies in the vicinity using the "near" functionality of mongodb for geo spatial data
    x = list(col.find({"office_1_location":{"$near":{"$geometry":{"type":"Point","coordinates":[longitude,latitude]},"$maxDistance":max_dist}}}))
    
    return x
