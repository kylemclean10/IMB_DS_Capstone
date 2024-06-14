# In this lab, you will be performing web scraping to collect Falcon 9 historical launch records from a Wikipedia page titled List of Falcon 9 and Falcon Heavy launches
# https://en.wikipedia.org/wiki/List_of_Falcon_9_and_Falcon_Heavy_launches

# Objectives
# Web scrap Falcon 9 launch records with BeautifulSoup:
# Extract a Falcon 9 launch records HTML table from Wikipedia
# Parse the table and convert it into a Pandas data frame
#
# First let's import required packages for this lab

import sys
import requests
from bs4 import BeautifulSoup
import re
import unicodedata
import pandas as pd

# and we will provide some helper functions for you to process web scraped HTML table

def date_time(table_cells):
    """
    This function returns the data and time from the HTML  table cell
    Input: the  element of a table data cell extracts extra row
    """
    return [data_time.strip() for data_time in list(table_cells.strings)][0:2]


def booster_version(table_cells):
    """
    This function returns the booster version from the HTML  table cell
    Input: the  element of a table data cell extracts extra row
    """
    out = ''.join([booster_version for i, booster_version in enumerate(table_cells.strings) if i % 2 == 0][0:-1])
    return out


def landing_status(table_cells):
    """
    This function returns the landing status from the HTML table cell
    Input: the  element of a table data cell extracts extra row
    """
    out = [i for i in table_cells.strings][0]
    return out


def get_mass(table_cells):
    mass = unicodedata.normalize("NFKD", table_cells.text).strip()
    if mass:
        mass.find("kg")
        new_mass = mass[0:mass.find("kg") + 2]
    else:
        new_mass = 0
    return new_mass


def extract_column_from_header(row):
    """
    This function returns the landing status from the HTML table cell
    Input: the  element of a table data cell extracts extra row
    """
    if (row.br):
        row.br.extract()
    if row.a:
        row.a.extract()
    if row.sup:
        row.sup.extract()

    colunm_name = ' '.join(row.contents)

    # Filter the digit and empty names
    if not (colunm_name.strip().isdigit()):
        colunm_name = colunm_name.strip()
        return colunm_name


# To keep the lab tasks consistent, you will be asked to scrape the data from a snapshot of the List of Falcon 9 and Falcon Heavy launches Wikipage updated on 9th June 2021

static_url = "https://en.wikipedia.org/w/index.php?title=List_of_Falcon_9_and_Falcon_Heavy_launches&oldid=1027686922"

# Next, request the HTML page from the above URL and get a response object

# TASK 1: Request the Falcon9 Launch Wiki page from its URL

# First, let's perform an HTTP GET method to request the Falcon9 Launch HTML page, as an HTTP response.

# Perform an HTTP GET request to fetch the HTML page
response = requests.get(static_url)

# Check the status code of the response to ensure the request was successful
if response.status_code == 200:
    print("Request was successful.")
else:
    print("Request failed with status code:", response.status_code)

# Optionally, you can print the first 500 characters of the response content to verify the HTML content
print(response.content[:500])

# Create a BeautifulSoup object from the HTML response content
soup = BeautifulSoup(response.text, 'html.parser')

# Optionally, you can print the title of the page to verify the BeautifulSoup object
print(soup.title.string)

# TASK 2: Extract all column/variable names from the HTML table header¶
# Next, we want to collect all relevant column names from the HTML table header
# Let's try to find all tables on the wiki page first. If you need to refresh your memory about BeautifulSoup,
# please check the external reference link towards the end of this lab)

# Find all tables on the wiki page
html_tables = soup.find_all('table')

# Print the number of tables found to verify
print(f"Number of tables found: {len(html_tables)}")

# Starting from the third table is our target table contains the actual launch records.

# Let's print the third table and check its content
first_launch_table = html_tables[2]
print(first_launch_table)

# Extract column names from the table header
column_names = []

# Apply find_all() function with `th` element on first_launch_table
th_elements = first_launch_table.find_all('th')

# Iterate each th element and apply the provided extract_column_from_header() to get a column name
for th in th_elements:
    name = extract_column_from_header(th)
    # Append the Non-empty column name into the list
    if name is not None and len(name) > 0:
        column_names.append(name)

# Print the column names to verify
print("Column Names:", column_names)

# TASK 3: Create a data frame by parsing the launch HTML tables
# We will create an empty dictionary with keys from the extracted column names in the previous task. Later,
# this dictionary will be converted into a Pandas dataframe

launch_dict= dict.fromkeys(column_names)

# Remove an irrelvant column
del launch_dict['Date and time ( )']

# Let's initial the launch_dict with each value to be an empty list
launch_dict['Flight No.'] = []
launch_dict['Launch site'] = []
launch_dict['Payload'] = []
launch_dict['Payload mass'] = []
launch_dict['Orbit'] = []
launch_dict['Customer'] = []
launch_dict['Launch outcome'] = []
# Added some new columns
launch_dict['Version Booster']=[]
launch_dict['Booster landing']=[]
launch_dict['Date']=[]
launch_dict['Time']=[]

# Next, we just need to fill up the launch_dict with launch records extracted from table rows.
# Usually, HTML tables in Wiki pages are likely to contain unexpected annotations and other types of noises,
# such as reference links B0004.1[8], missing values N/A [e], inconsistent formatting, etc.
# To simplify the parsing process, we have provided an incomplete code snippet below to help you to fill up the launch_dict.
# Please complete the following code snippet with TODOs or you can choose to write your own logic to parse all launch tables:

# Extract each table
extracted_row = 0
for table_number, table in enumerate(soup.find_all('table', "wikitable plainrowheaders collapsible")):
    # Get table row
    for rows in table.find_all("tr"):
        # Check to see if first table heading is a number corresponding to launch number
        if rows.th:
            if rows.th.string:
                flight_number = rows.th.string.strip()
                flag = flight_number.isdigit()
        else:
            flag = False

        # Get table element
        row = rows.find_all('td')

        # If it is a number, save cells in a dictionary
        if flag:
            extracted_row += 1

            # Flight Number value
            launch_dict['Flight No.'].append(flight_number)

            # Date and Time
            datatimelist = date_time(row[0])
            date = datatimelist[0].strip(',')
            time = datatimelist[1]
            launch_dict['Date'].append(date)
            launch_dict['Time'].append(time)

            # Booster version
            bv = booster_version(row[1])
            if not bv:
                bv = row[1].a.string if row[1].a else ''
            launch_dict['Version Booster'].append(bv)

            # Launch Site
            launch_site = row[2].a.string if row[2].a else ''
            launch_dict['Launch site'].append(launch_site)

            # Payload
            payload = row[3].a.string if row[3].a else ''
            launch_dict['Payload'].append(payload)

            # Payload Mass
            payload_mass = get_mass(row[4])
            launch_dict['Payload mass'].append(payload_mass)

            # Orbit
            orbit = row[5].a.string if row[5].a else ''
            launch_dict['Orbit'].append(orbit)

            # Customer
            customer = row[6].a.string if row[6].a else ''
            launch_dict['Customer'].append(customer)

            # Launch outcome
            launch_outcome = list(row[7].strings)[0] if row[7].strings else ''
            launch_dict['Launch outcome'].append(launch_outcome)

            # Booster landing
            booster_landing = landing_status(row[8])
            launch_dict['Booster landing'].append(booster_landing)

# Convert the dictionary into a Pandas DataFrame
launch_df = pd.DataFrame(launch_dict)

# Display the DataFrame to verify
print(launch_df.head())

df= pd.DataFrame({ key:pd.Series(value) for key, value in launch_dict.items() })

df.to_csv('spacex_web_scraped.csv', index=False)