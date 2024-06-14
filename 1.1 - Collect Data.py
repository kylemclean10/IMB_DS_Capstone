import requests
import pandas as pd
import numpy as np
import datetime

# Setting this option will print all columns of a dataframe
pd.set_option('display.max_columns', None)
# Setting this option will print all of the data in a feature
pd.set_option('display.max_colwidth', None)

# Define helper functions to extract additional information using API calls
def getBoosterVersion(data):
    for x in data['rocket']:
        if x:
            response = requests.get("https://api.spacexdata.com/v4/rockets/"+str(x)).json()
            BoosterVersion.append(response['name'])

def getLaunchSite(data):
    for x in data['launchpad']:
        if x:
            response = requests.get("https://api.spacexdata.com/v4/launchpads/"+str(x)).json()
            Longitude.append(response['longitude'])
            Latitude.append(response['latitude'])
            LaunchSite.append(response['name'])

def getPayloadData(data):
    for load in data['payloads']:
        if load:
            response = requests.get("https://api.spacexdata.com/v4/payloads/"+load).json()
            PayloadMass.append(response['mass_kg'])
            Orbit.append(response['orbit'])

def getCoreData(data):
    for core in data['cores']:
        if core['core'] != None:
            response = requests.get("https://api.spacexdata.com/v4/cores/"+core['core']).json()
            Block.append(response['block'])
            ReusedCount.append(response['reuse_count'])
            Serial.append(response['serial'])
        else:
            Block.append(None)
            ReusedCount.append(None)
            Serial.append(None)
        Outcome.append(str(core['landing_success'])+' '+str(core['landing_type']))
        Flights.append(core['flight'])
        GridFins.append(core['gridfins'])
        Reused.append(core['reused'])
        Legs.append(core['legs'])
        LandingPad.append(core['landpad'])

# URL to the static JSON data
static_json_url = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/API_call_spacex_api.json'
response = requests.get(static_json_url)

# Check if the request was successful
if response.status_code == 200:
    print("Request was successful!")
else:
    print(f"Failed to retrieve data. Status code: {response.status_code}")

# Decode the response content as JSON
data = response.json()

# Use json_normalize method to convert the JSON result into a DataFrame
df = pd.json_normalize(data)

# Display the DataFrame
print(df.head())

# Let's take a subset of our dataframe keeping only the features we want and the flight number, and date_utc
df = df[['rocket', 'payloads', 'launchpad', 'cores', 'flight_number', 'date_utc']]

# We will remove rows with multiple cores because those are falcon rockets with 2 extra rocket boosters and rows that have multiple payloads in a single rocket.
df = df[df['cores'].map(len) == 1]
df = df[df['payloads'].map(len) == 1]

# Since payloads and cores are lists of size 1 we will also extract the single value in the list and replace the feature.
df['cores'] = df['cores'].map(lambda x: x[0])
df['payloads'] = df['payloads'].map(lambda x: x[0])

# We also want to convert the date_utc to a datetime datatype and then extract the date leaving the time
df['date'] = pd.to_datetime(df['date_utc']).dt.date

# Using the date we will restrict the dates of the launches
df = df[df['date'] <= datetime.date(2020, 11, 13)]

# Display the final DataFrame
print(df.head())

# Global variables
BoosterVersion = []
PayloadMass = []
Orbit = []
LaunchSite = []
Outcome = []
Flights = []
GridFins = []
Reused = []
Legs = []
LandingPad = []
Block = []
ReusedCount = []
Serial = []
Longitude = []
Latitude = []

# Call helper functions
getBoosterVersion(df)
getLaunchSite(df)
getPayloadData(df)
getCoreData(df)

# Check the lengths of the lists
print(f"BoosterVersion: {len(BoosterVersion)}")
print(f"PayloadMass: {len(PayloadMass)}")
print(f"Orbit: {len(Orbit)}")
print(f"LaunchSite: {len(LaunchSite)}")
print(f"Outcome: {len(Outcome)}")
print(f"Flights: {len(Flights)}")
print(f"GridFins: {len(GridFins)}")
print(f"Reused: {len(Reused)}")
print(f"Legs: {len(Legs)}")
print(f"LandingPad: {len(LandingPad)}")
print(f"Block: {len(Block)}")
print(f"ReusedCount: {len(ReusedCount)}")
print(f"Serial: {len(Serial)}")
print(f"Longitude: {len(Longitude)}")
print(f"Latitude: {len(Latitude)}")

# Ensure all lists are the same length before creating the DataFrame
min_length = min(len(BoosterVersion), len(PayloadMass), len(Orbit), len(LaunchSite), len(Outcome),
                 len(Flights), len(GridFins), len(Reused), len(Legs), len(LandingPad),
                 len(Block), len(ReusedCount), len(Serial), len(Longitude), len(Latitude))

launch_data = pd.DataFrame({
    'FlightNumber': df['flight_number'][:min_length],
    'Date': df['date'][:min_length],
    'BoosterVersion': BoosterVersion[:min_length],
    'PayloadMass': PayloadMass[:min_length],
    'Orbit': Orbit[:min_length],
    'LaunchSite': LaunchSite[:min_length],
    'Outcome': Outcome[:min_length],
    'Flights': Flights[:min_length],
    'GridFins': GridFins[:min_length],
    'Reused': Reused[:min_length],
    'Legs': Legs[:min_length],
    'LandingPad': LandingPad[:min_length],
    'Block': Block[:min_length],
    'ReusedCount': ReusedCount[:min_length],
    'Serial': Serial[:min_length],
    'Longitude': Longitude[:min_length],
    'Latitude': Latitude[:min_length]
})

# Display the new DataFrame
print(launch_data.head())

# Then, we need to create a Pandas data frame from the dictionary launch_dict.

# Assuming launch_dict is your dictionary
launch_dict = {
    # Your data here
}

# Create a DataFrame from the dictionary
launch_df = pd.DataFrame(launch_dict)

# Display the DataFrame
print(launch_df)

# Task 2: Filter the dataframe to only include Falcon 9 launches
# Finally we will remove the Falcon 1 launches keeping only the Falcon 9 launches. Filter the data dataframe using the BoosterVersion column to only keep the Falcon 9 launches.
# Save the filtered data to a new dataframe called data_falcon9.

# Assuming launch_df is your DataFrame
launch_df = pd.DataFrame({
    'FlightNumber': [1, 2, 3, 4],
    'Date': ['2020-01-01', '2020-02-01', '2020-03-01', '2020-04-01'],
    'BoosterVersion': ['Falcon 9', 'Falcon Heavy', 'Falcon 9', 'Falcon 1'],
    'PayloadMass': [500, 1000, 1500, 200],
    'Orbit': ['LEO', 'GTO', 'LEO', 'SSO'],
    'LaunchSite': ['CCAFS LC-40', 'KSC LC-39A', 'CCAFS LC-40', 'Omelek Island'],
    'Outcome': ['Success', 'Success', 'Success', 'Failure'],
    'Flights': [1, 1, 1, 1],
    'GridFins': [True, True, False, False],
    'Reused': [False, True, True, False],
    'Legs': [True, True, True, False],
    'LandingPad': ['LZ-1', 'LZ-2', 'LZ-1', None],
    'Block': [5, 5, 4, None],
    'ReusedCount': [0, 1, 2, 0],
    'Serial': ['B1049', 'B1051', 'B1046', 'B0003'],
    'Longitude': [-80.5772, -80.6043, -80.5772, 167.7403],
    'Latitude': [28.5623, 28.5733, 28.5623, 9.0483]
})

# Filter the DataFrame to only include Falcon 9 launches
data_falcon9 = launch_df[launch_df['BoosterVersion'] == 'Falcon 9']

# Display the filtered DataFrame
print(data_falcon9)

# Now that we have removed some values we should reset the FlgihtNumber column
data_falcon9.loc[:,'FlightNumber'] = list(range(1, data_falcon9.shape[0]+1))
print(data_falcon9)

########################################## Data Wrangling ##########################################
# We can see below that some of the rows are missing values in our dataset.
print(data_falcon9.isnull().sum())
# this shows 0 null values!!!!!!!!!!!

# Task 3: Dealing with Missing Values¶
# Calculate below the mean for the PayloadMass using the .mean().
# Then use the mean and the .replace() function to replace np.nan values in the data with the mean you calculated.

# Filter to only include Falcon 9 launches
data_falcon9 = data_falcon9[data_falcon9['BoosterVersion'] == 'Falcon 9'].copy()

# Calculate the mean value of PayloadMass column
mean_payload_mass = data_falcon9['PayloadMass'].mean()
print(f"Mean PayloadMass: {mean_payload_mass}")

# Replace the np.nan values in the PayloadMass column with its mean value
data_falcon9['PayloadMass'] = data_falcon9['PayloadMass'].replace(np.nan, mean_payload_mass)

# Verify there are no missing values in PayloadMass column
print(f"Missing values in PayloadMass after replacement: {data_falcon9['PayloadMass'].isnull().sum()}")

# Export the DataFrame to a CSV file
data_falcon9.to_csv('dataset_part_1.csv', index=False)

# Display the DataFrame to verify changes
print(data_falcon9)



# You should see the number of missing values of the PayLoadMass change to zero.
# Now we should have no missing values in our dataset except for in LandingPad.
# We can now export it to a CSV for the next section,but to make the answers consistent, in the next lab we will provide data in a pre-selected date range.



data_falcon9.to_csv('dataset_part_1.csv', index=False)




