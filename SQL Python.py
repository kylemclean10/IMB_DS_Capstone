# -- Using this Python notebook you will:
# --
# -- Understand the Spacex DataSet
# -- Load the dataset into the corresponding table in a Db2 database
# -- Execute SQL queries to answer assignment questions
#
# -- Overview of the DataSet¶
# -- SpaceX has gained worldwide attention for a series of historic milestones.
# --
# -- It is the only private company ever to return a spacecraft from low-earth orbit, which it first accomplished in December 2010.
# -- SpaceX advertises Falcon 9 rocket launches on its website with a cost of 62 million dollars wheras other providers cost upward
# -- of 165 million dollars each, much of the savings is because Space X can reuse the first stage.
# ----- Therefore if we can determine if the first stage will land, we can determine the cost of a launch.
# ----- This information can be used if an alternate company wants to bid against SpaceX for a rocket launch.
# ----- This dataset includes a record for each payload carried during a SpaceX mission into outer space.
#
# ---------------------------------------------- Download the datasets¶
#
# -- This assignment requires you to load the spacex dataset.
# --
# -- In many cases the dataset to be analyzed is available as a .CSV (comma separated values) file, perhaps on the internet.
# -- Click on the link below to download and save the dataset (.CSV file):
#
# !pip install sqlalchemy==1.3.9
#
# %load_ext sql

import sqlite3

con = sqlite3.connect("my_data1.db")
cur = con.cursor()

# %sql sqlite:///my_data1.db

import pandas as pd
df = pd.read_csv("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/labs/module_2/data/Spacex.csv")
# df.to_sql("SPACEXTBL", con, if_exists='replace', index=False,method="multi")

# Load the dataset
# df = pd.read_csv('/path/to/Spacex.csv')
print(df.head())

# Connect to SQLite database (it will be created if it doesn't exist)
conn = sqlite3.connect('spacex.db')

# Write the DataFrame to a SQLite table
df.to_sql('spacex', conn, if_exists='replace', index=False)

# %sql create table SPACEXTABLE as select * from SPACEXTBL where Date is not null

# Commit and close the connection
conn.commit()
conn.close()

# Reconnect to the SQLite database
conn = sqlite3.connect('spacex.db')

# Read the data from the table
df_from_db = pd.read_sql('SELECT * FROM spacex', conn)
print("Data from SQLite database:")
print(df_from_db.head())

# Create a cursor object
cursor = conn.cursor()

# TASK 1 : Display the names of the unique launch sites in the space mission
print("TASK 1 : Display the names of the unique launch sites in the space mission")
# Execute the SQL query to get unique launch sites
query = 'SELECT DISTINCT "Launch_Site" FROM spacex'
cursor.execute(query)

# Fetch all unique launch sites
unique_launch_sites = cursor.fetchall()

# Print the unique launch sites
print("Unique Launch Sites:")
for site in unique_launch_sites:
    print(site[0])

# Task 2: Display 5 records where launch sites begin with the string 'CCA'
print("Task 2: Display 5 records where launch sites begin with the string 'CCA'")
# Execute the SQL query to get 5 records where launch sites begin with 'CCA'
query = 'SELECT * FROM spacex WHERE "Launch_Site" LIKE "CCA%" LIMIT 5'
cursor.execute(query)

# Fetch the records
records = cursor.fetchall()

# Print the records
print("5 Records where Launch_Site begins with 'CCA':")
for record in records:
    print(record)

# Task 3: Display the total payload mass carried by boosters launched by NASA (CRS)
print("Task 3: Display the total payload mass carried by boosters launched by NASA (CRS)")
# Execute the SQL query to get the total payload mass for NASA (CRS) missions
query = 'SELECT SUM("Payload_Mass__kg_") FROM spacex WHERE "Customer" LIKE "%NASA (CRS)%"'
cursor.execute(query)

# Fetch the total payload mass
total_payload_mass = cursor.fetchone()[0]

# Print the total payload mass
print("Total Payload Mass carried by boosters launched by NASA (CRS):")
print(total_payload_mass, "kg")

# Task 4: Display average payload mass carried by booster version F9 v1.1
print("Task 4: Display average payload mass carried by booster version F9 v1.1")
# Execute the SQL query to get the average payload mass for F9 v1.1 booster version
query = 'SELECT AVG("Payload_Mass__kg_") FROM spacex WHERE "Booster_Version" = "F9 v1.1"'
cursor.execute(query)

# Fetch the average payload mass
avg_payload_mass = cursor.fetchone()[0]

# Print the average payload mass
print("Average Payload Mass carried by booster version F9 v1.1:")
print(avg_payload_mass, "kg")

# Task 5: List the date when the first succesful landing outcome in ground pad was acheived
print("Task 5: List the date when the first succesful landing outcome in ground pad was acheived")
# Execute the SQL query to get the date of the first successful landing on ground pad
query = '''
SELECT MIN("Date") 
FROM spacex 
WHERE "Landing_Outcome" = "Success (ground pad)"
'''
cursor.execute(query)

# Fetch the date
first_success_date = cursor.fetchone()[0]

# Print the date
print("Date of the first successful landing on ground pad:")
print(first_success_date)

# Task 6: List the names of the boosters which have success in drone ship and have payload mass greater than 4000 but less than 6000
print("Task 6: List the names of the boosters which have success in drone ship and have payload mass greater than 4000 but less than 6000")

# Execute the SQL query to get booster names with the specified conditions
query = '''
SELECT "Booster_Version"
FROM spacex 
WHERE "Landing_Outcome" = "Success (drone ship)"
AND "Payload_Mass__kg_" > 4000 
AND "Payload_Mass__kg_" < 6000
'''
cursor.execute(query)

# Fetch the booster names
booster_names = cursor.fetchall()

# Print the booster names
print("Booster names with success in drone ship and payload mass between 4000 and 6000 kg:")
for name in booster_names:
    print(name[0])

# Task 7: List the total number of successful and failure mission outcomes
print("Task 7: List the total number of successful and failure mission outcomes")

# Execute the SQL query to count the number of successful and failure mission outcomes
query = '''
SELECT "Mission_Outcome", COUNT(*)
FROM spacex
GROUP BY "Mission_Outcome"
'''
cursor.execute(query)

# Fetch the results
mission_outcomes = cursor.fetchall()

# Print the results
print("Total number of successful and failure mission outcomes:")
for outcome in mission_outcomes:
    print(outcome[0], ":", outcome[1])

# Task 8: List the names of the booster_versions which have carried the maximum payload mass. Use a subquery
print("Task 8: List the names of the booster_versions which have carried the maximum payload mass. Use a subquery")

# Execute the SQL query to get the booster versions with the maximum payload mass
query = '''
SELECT "Booster_Version"
FROM spacex
WHERE "Payload_Mass__kg_" = (
    SELECT MAX("Payload_Mass__kg_")
    FROM spacex
)
'''
cursor.execute(query)

# Fetch the booster versions
booster_versions = cursor.fetchall()

# Print the booster versions
print("Booster versions which have carried the maximum payload mass:")
for version in booster_versions:
    print(version[0])

# Task 9: List the records which will display the month names, failure landing_outcomes in drone ship ,booster versions, launch_site for the months in year 2015.
print("Task 9: List the records which will display the month names, failure landing_outcomes in drone ship ,booster versions, launch_site for the months in year 2015.")
# Note: SQLLite does not support monthnames. So you need to use substr(Date, 6,2) as month to get the months and substr(Date,0,5)='2015' for year.

# Execute the SQL query to get the required records
query = '''
SELECT 
    CASE SUBSTR("Date", 6, 2)
        WHEN '01' THEN 'January'
        WHEN '02' THEN 'February'
        WHEN '03' THEN 'March'
        WHEN '04' THEN 'April'
        WHEN '05' THEN 'May'
        WHEN '06' THEN 'June'
        WHEN '07' THEN 'July'
        WHEN '08' THEN 'August'
        WHEN '09' THEN 'September'
        WHEN '10' THEN 'October'
        WHEN '11' THEN 'November'
        WHEN '12' THEN 'December'
    END AS Month_Name,
    "Landing_Outcome",
    "Booster_Version",
    "Launch_Site"
FROM spacex
WHERE "Landing_Outcome" LIKE '%Failure (drone ship)%'
AND SUBSTR("Date", 1, 4) = '2015'
'''
cursor.execute(query)

# Fetch the records
records = cursor.fetchall()

# Print the records
print("Records with failure landing outcomes on drone ship in 2015:")
for record in records:
    print(record)

# Task 10: Rank the count of landing outcomes (such as Failure (drone ship) or Success (ground pad)) between the date 2010-06-04 and 2017-03-20, in descending order.
print("Task 10: Rank the count of landing outcomes (such as Failure (drone ship) or Success (ground pad)) between the date 2010-06-04 and 2017-03-20, in descending order.")

# Execute the SQL query to get the count of landing outcomes in the specified date range
query = '''
SELECT "Landing_Outcome", COUNT(*) as Outcome_Count
FROM spacex
WHERE "Date" BETWEEN '2010-06-04' AND '2017-03-20'
GROUP BY "Landing_Outcome"
ORDER BY Outcome_Count DESC
'''
cursor.execute(query)

# Fetch the results
landing_outcomes = cursor.fetchall()

# Print the results
print("Landing outcomes count between 2010-06-04 and 2017-03-20 in descending order:")
for outcome in landing_outcomes:
    print(outcome[0], ":", outcome[1])

# Close the connection
conn.close()

