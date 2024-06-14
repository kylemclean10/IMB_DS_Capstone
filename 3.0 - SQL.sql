-- Using this Python notebook you will:
--
-- Understand the Spacex DataSet
-- Load the dataset into the corresponding table in a Db2 database
-- Execute SQL queries to answer assignment questions

-- Overview of the DataSet¶
-- SpaceX has gained worldwide attention for a series of historic milestones.
--
-- It is the only private company ever to return a spacecraft from low-earth orbit, which it first accomplished in December 2010.
-- SpaceX advertises Falcon 9 rocket launches on its website with a cost of 62 million dollars wheras other providers cost upward
-- of 165 million dollars each, much of the savings is because Space X can reuse the first stage.
----- Therefore if we can determine if the first stage will land, we can determine the cost of a launch.
----- This information can be used if an alternate company wants to bid against SpaceX for a rocket launch.
----- This dataset includes a record for each payload carried during a SpaceX mission into outer space.

---------------------------------------------- Download the datasets¶

-- This assignment requires you to load the spacex dataset.
--
-- In many cases the dataset to be analyzed is available as a .CSV (comma separated values) file, perhaps on the internet.
-- Click on the link below to download and save the dataset (.CSV file):

-- !pip install sqlalchemy==1.3.9

-- %load_ext sql

import sqlite3

con = sqlite3.connect("my_data1.db")
cur = con.cursor()

%sql sqlite:///my_data1.db

import pandas as pd
-- df = pd.read_csv("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/labs/module_2/data/Spacex.csv")
-- df.to_sql("SPACEXTBL", con, if_exists='replace', index=False,method="multi")

-- # Load the dataset
df = pd.read_csv('/path/to/Spacex.csv')
print(df.head())

-- # Connect to SQLite database (it will be created if it doesn't exist)
conn = sqlite3.connect('spacex.db')

-- # Write the DataFrame to a SQLite table
df.to_sql('spacex', conn, if_exists='replace', index=False)

-- %sql create table SPACEXTABLE as select * from SPACEXTBL where Date is not null

-- # Commit and close the connection
conn.commit()
conn.close()

-- # Reconnect to the SQLite database
conn = sqlite3.connect('spacex.db')

-- # Read the data from the table
df_from_db = pd.read_sql('SELECT * FROM spacex', conn)
print("Data from SQLite database:")
print(df_from_db.head())
print("helloworld")
-- # Close the connection
conn.close()