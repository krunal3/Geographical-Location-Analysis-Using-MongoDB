# Importing all the required libraries
import sys 
sys.setrecursionlimit(1500)
from pymongo.errors import BulkWriteError

# Importing all the functions from the defined files
from API.api_gathering import*
from Database.database import*
from math_logic import*

# Importing the database and collection
db, coll = details_fecthing('GeoSpatialAnalysis','Companies')
companies = list(coll.find({'$or':[{"offices.latitude":{'$ne':None}},{"offices.longitude":{'$ne':None}}]}))

# Converting from dictionary to dataframe
dict_companies = {}
l = len(companies)
for i in range(l):
        key_set(dict_companies, '_id', companies[i]['_id'])
        key_set(dict_companies, 'name', companies[i]['name'])
        key_set(dict_companies, 'founded_year', companies[i]['founded_year'])
        key_set(dict_companies, 'category_code', companies[i]['category_code'])
        key_set(dict_companies, 'total_money_raised', companies[i]['total_money_raised'])
        key_set(dict_companies, 'deadpooled_year', companies[i]['deadpooled_year'])
companies_df = pd.DataFrame.from_dict(dict_companies)

# Obtaining number of offices and data realted to it
num_offices = []
for i in range(l):
    num_offices.append(len(companies[i]['offices']))

companies_df['num_offices'] = num_offices

m = max(num_offices)
for i in range(m):
        companies_df[f'office_{i+1}_longitude'] = [np.nan] * len(num_offices)
        companies_df[f'office_{i+1}_latitude'] = [np.nan] * len(num_offices)
        companies_df[f'office_{i+1}_location'] = [{}] * len(num_offices)
        companies_df[f'office_{i+1}_city'] = [None] * len(num_offices)
        companies_df[f'office_{i+1}_state_code'] = [None] * len(num_offices)
        companies_df[f'office_{i+1}_country_code'] = [None] * len(num_offices)

# Gathering data related to companies
companies_data = []
for i in range(len(companies)):
    if len(companies[i]['offices'])==0:
        companies_data.append([[0, np.nan, np.nan, np.nan, np.nan, np.nan]])
    elif len(companies[i]['offices'])>0:
        temp_offices = []
        for j in range(len(companies[i]['offices'])):
            temp_offices.append([j+1, companies[i]['offices'][j]['latitude'], companies[i]['offices'][j]['longitude'],companies[i]['offices'][j]['city'], companies[i]['offices'][j]['state_code'],companies[i]['offices'][j]['country_code']])
        companies_data.append(temp_offices)

k = len(companies_data)
for i in range(k):
        for j in range(len(companies_data[i])):
            if companies_data[i][j][0] != 0:
                companies_df.at[i, f'office_{j+1}_longitude'] = companies_data[i][j][2]
                companies_df.at[i, f'office_{j+1}_latitude'] = companies_data[i][j][1]
                companies_df.at[i, f'office_{j+1}_city'] = companies_data[i][j][3]
                companies_df.at[i, f'office_{j+1}_state_code'] = companies_data[i][j][4]
                companies_df.at[i, f'office_{j+1}_country_code'] = companies_data[i][j][5]

# Creating the GeoJson objects from the data
for i in range(k):
        for j in range(len(companies_data[i])):
            if companies_data[i][j][0] != 0:
                companies_df.at[i, f'office_{j+1}_location'] = location_object(companies_df.at[i, f'office_{j+1}_longitude'],companies_df.at[i, f'office_{j+1}_latitude'])


# Gathering and editing the data based on the amount of money raised
companies_df.total_money_raised.replace('$0','0', inplace=True)
companies_df['total_money_raised_currency'] = [None] * len(num_offices)

for i in range(len(companies_df)):
    if companies_df.at[i,'total_money_raised'] == '0':
        companies_df.at[i,'total_money_raised_currency'] = '$'
    else:
        companies_df.at[i,'total_money_raised_currency'] = companies_df.total_money_raised[i][0]
        companies_df.at[i,'total_money_raised'] = companies_df.total_money_raised[i][1:]

for i in range(len(companies_df)):
    if companies_df.at[i,'total_money_raised'][0] == '$':
        companies_df.at[i,'total_money_raised_currency'] = companies_df.total_money_raised[i][0]
        companies_df.at[i,'total_money_raised'] = companies_df.total_money_raised[i][1:]

companies_df.total_money_raised.replace('r21M','21M',inplace=True)

for i in range(len(companies_df)):
    if companies_df.total_money_raised[i][-1] == 'M':
        companies_df.at[i,'total_money_raised'] = str(float(companies_df.total_money_raised[i].split('M')[0])*1000000)
    elif companies_df.total_money_raised[i][-1] == 'B':
        companies_df.at[i,'total_money_raised'] = str(float(companies_df.total_money_raised[i].split('B')[0])*1000000000)
    elif companies_df.total_money_raised[i][-1] == 'k':
        companies_df.at[i,'total_money_raised'] = str(float(companies_df.total_money_raised[i].split('k')[0])*1000)

companies_df['total_money_raised'] = companies_df['total_money_raised'].astype('float')

companies_df.total_money_raised_currency.replace('k','SEK',inplace=True)
companies_df.total_money_raised_currency.replace('$','USD',inplace=True)
companies_df.total_money_raised_currency.replace('£','GBP',inplace=True)
companies_df.total_money_raised_currency.replace('¥','JPY',inplace=True)
companies_df.total_money_raised_currency.replace('€','EUR',inplace=True)

# Details reagrding the companies that got deadpooled in the previous year
companies_df.deadpooled_year.replace(1.0,2006,inplace=True)
companies_df.deadpooled_year.replace(2.0,1998,inplace=True)
companies_df.deadpooled_year.replace(3.0,2008,inplace=True)

# Using the exchange rate API to get the real time rate difference among mentioned currencies
exchangerateGBP = exchangerate_api('GBP').json()
exchangerateSEK = exchangerate_api('SEK').json()
exchangerateEUR = exchangerate_api('EUR').json()

# Setting USD as our standard currency and converting all other one into USD using our API
companies_df['total_money_raised_USD'] = [0.0]*len(companies_df)

for i in range(len(companies_df)):
    if companies_df.at[i,'total_money_raised_currency'] == 'USD':
        companies_df.at[i,'total_money_raised_USD'] = companies_df.at[i,'total_money_raised']
    elif companies_df.at[i,'total_money_raised_currency'] == 'GBP':
        companies_df.at[i,'total_money_raised_USD'] = companies_df.at[i,'total_money_raised']*exchangerateGBP['conversion_rates']['USD']   
    elif companies_df.at[i,'total_money_raised_currency'] == 'SEK':
        companies_df.at[i,'total_money_raised_USD'] = companies_df.at[i,'total_money_raised']*exchangerateSEK['conversion_rates']['USD']   
    elif companies_df.at[i,'total_money_raised_currency'] == 'EUR':
        companies_df.at[i,'total_money_raised_USD'] = companies_df.at[i,'total_money_raised']*exchangerateEUR['conversion_rates']['USD']

# Exporting the cleaned data to a csv file 
companies_df.to_csv('./ProcessedData/companies_df.csv', index=False)

# Exporting the cleaned data to a json file for further use
companies_df.to_json('./ProcessedData/cleaned_companies.json',orient='records',default_handler=str)

# Importing cleaned data to MongoDB and creating a 2dSphere index:
coll2 = db['companies_cleaned_1']
coll2.insert_many(companies_df.to_dict('records'))