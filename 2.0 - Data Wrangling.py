# Lab 2: Data wrangling
#
# In this lab, we will perform some Exploratory Data Analysis (EDA) to find some patterns in the data and determine what would be the label for training supervised models.
#
# In the data set, there are several different cases where the booster did not land successfully.
# Sometimes a landing was attempted but failed due to an accident; for example, True Ocean means the mission outcome was successfully
# landed to a specific region of the ocean while False Ocean means the mission outcome was unsuccessfully landed to a specific region of the ocean.
# True RTLS means the mission outcome was successfully landed to a ground pad False RTLS means the mission outcome was unsuccessfully landed to a ground pad.
# True ASDS means the mission outcome was successfully landed on a drone ship False ASDS means the mission outcome was unsuccessfully landed on a drone ship.
#
# In this lab we will mainly convert those outcomes into Training Labels with 1 means the booster successfully landed 0 means it was unsuccessful.

# Objectives
# Perform exploratory Data Analysis and determine Training Labels
#
# Exploratory Data Analysis
# Determine Training Labels

import pandas as pd
import numpy as np

######################################################## Data Analysis

df=pd.read_csv("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/dataset_part_1.csv")
print(df.head(10))

# Identify and calculate the percentage of the missing values in each attribute
print(df.isnull().sum()/len(df)*100)

# Identify which columns are numerical and categorical:
print(df.dtypes)

########################## TASK 1: Calculate the number of launches on each site
# The data contains several Space X launch facilities: Cape Canaveral Space Launch Complex 40 VAFB SLC 4E ,
# Vandenberg Air Force Base Space Launch Complex 4E (SLC-4E), Kennedy Space Center Launch Complex 39A KSC LC 39A .
# The location of each Launch Is placed in the column LaunchSite
#
# Next, let's see the number of launches for each site.
#
# Use the method value_counts() on the column LaunchSite to determine the number of launches on each site:

# Apply value_counts() on column LaunchSite
launch_counts = df['LaunchSite'].value_counts()

# Display the result
print(launch_counts)

# TASK 2: Calculate the number and occurrence of each orbit
# Use the method .value_counts() to determine the number and occurrence of each orbit in the column Orbit

# Apply value_counts on Orbit column
orbit_counts = df['Orbit'].value_counts()

# Display the result
print(orbit_counts)

# TASK 3: Calculate the number and occurence of mission outcome of the orbits
# Use the method .value_counts() on the column Outcome to determine the number of landing_outcomes.Then assign it to a variable landing_outcomes.

# landing_outcomes = values on Outcome column
landing_outcomes = df['Outcome'].value_counts()

# Display the result
print(landing_outcomes)

# True Ocean means the mission outcome was successfully landed to a specific region of the ocean while False Ocean means the mission outcome was
# unsuccessfully landed to a specific region of the ocean. True RTLS means the mission outcome was successfully landed to a ground pad False RTLS
# the mission outcome was unsuccessfully landed to a ground pad.True ASDS means the mission outcome was successfully landed to a drone ship False
# ASDS means the mission outcome was unsuccessfully landed to a drone ship.
# None ASDS and None None these represent a failure to land.

for i,outcome in enumerate(landing_outcomes.keys()):
    print(i,outcome)

# We create a set of outcomes where the second stage did not land successfully:
bad_outcomes=set(landing_outcomes.keys()[[1,3,5,6,7]])
print(bad_outcomes)

# TASK 4: Create a landing outcome label from Outcome column
# Using the Outcome, create a list where the element is zero if the corresponding row in Outcome is in the set bad_outcome; otherwise, its one.
# Then assign it to the variable landing_class:

# Create the landing_class list
landing_class = [1 if outcome not in bad_outcomes else 0 for outcome in df['Outcome']]

# Assign the list to the variable landing_class
df['landing_class'] = landing_class

# Display the first few rows to verify the new column
print(df[['Outcome', 'landing_class']].head(10))

df['Class']=landing_class
print(df[['Class']].head(8))

print(df.head(5))

print(df["Class"].mean())