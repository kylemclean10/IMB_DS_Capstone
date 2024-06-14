# Launch Sites Locations Analysis with Folium

# The launch success rate may depend on many factors such as payload mass, orbit type, and so on.
# It may also depend on the location and proximities of a launch site, i.e., the initial position of rocket trajectories. Finding an optimal location for
# building a launch site certainly involves many factors and
# hopefully we could discover some of the factors by analyzing the existing launch site locations.
#
# In the previous exploratory data analysis labs, you have visualized the SpaceX launch dataset using matplotlib and seaborn and discovered some preliminary
# correlations between the launch site and success rates. In this lab, you will be performing more interactive visual analytics using Folium.

# Objectives
# TASK 1: Mark all launch sites on a map
# TASK 2: Mark the success/failed launches for each site on the map
# TASK 3: Calculate the distances between a launch site to its proximities
# After completed the above tasks, you should be able to find some geographical patterns about launch sites.

import folium
import pandas as pd
# Import folium MarkerCluster plugin
from folium.plugins import MarkerCluster
# Import folium MousePosition plugin
from folium.plugins import MousePosition
# Import folium DivIcon plugin
from folium.features import DivIcon

from math import sin, cos, sqrt, atan2, radians

# Load data
URL = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_geo.csv'
spacex_df = pd.read_csv(URL)

# Select relevant sub-columns: `Launch Site`, `Lat`, `Long`, `class`
spacex_df = spacex_df[['Launch Site', 'Lat', 'Long', 'class']]
launch_sites_df = spacex_df.groupby(['Launch Site'], as_index=False).first()
launch_sites_df = launch_sites_df[['Launch Site', 'Lat', 'Long']]


# Function to calculate distance between two points
def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6373.0  # approximate radius of earth in km

    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    return distance


# Coordinates for proximities (example coordinates)
proximities = {
    'coastline': (28.56367, -80.57163),
    'city': (28.3922, -80.6077),  # Cocoa Beach, FL
    'railway': (28.5721, -80.5853),
    'highway': (28.5623, -80.5772)
}

# Start location is NASA Johnson Space Center
nasa_coordinate = [29.559684888503615, -95.0830971930759]
site_map = folium.Map(location=nasa_coordinate, zoom_start=5)

# Initialize a MarkerCluster object
marker_cluster = MarkerCluster().add_to(site_map)

# Add a marker for each launch site
for index, row in launch_sites_df.iterrows():
    launch_site_name = row['Launch Site']
    launch_site_lat = row['Lat']
    launch_site_long = row['Long']

    # Create a circle and add a popup label with the launch site name
    circle = folium.Circle([launch_site_lat, launch_site_long], radius=1000, color='#d35400', fill=True).add_child(
        folium.Popup(launch_site_name))

    # Create a marker with a text label
    marker = folium.Marker(
        [launch_site_lat, launch_site_long],
        icon=DivIcon(
            icon_size=(20, 20),
            icon_anchor=(0, 0),
            html='<div style="font-size: 12; color:#d35400;"><b>%s</b></div>' % launch_site_name,
        )
    )

    site_map.add_child(circle)
    site_map.add_child(marker)

# Add markers and lines for each proximity
for proximity_name, (prox_lat, prox_lon) in proximities.items():
    for index, row in launch_sites_df.iterrows():
        launch_site_name = row['Launch Site']
        launch_site_lat = row['Lat']
        launch_site_long = row['Long']

        # Calculate distance to the proximity
        distance = calculate_distance(launch_site_lat, launch_site_long, prox_lat, prox_lon)

        # Create and add a folium.Marker on the proximity point
        distance_marker = folium.Marker(
            [prox_lat, prox_lon],
            icon=DivIcon(
                icon_size=(20, 20),
                icon_anchor=(0, 0),
                html='<div style="font-size: 12; color:#d35400;"><b>{:10.2f} KM</b></div>'.format(distance),
            )
        )
        site_map.add_child(distance_marker)

        # Create a PolyLine object using the proximity coordinates and launch site coordinate
        lines = folium.PolyLine(locations=[[launch_site_lat, launch_site_long], [prox_lat, prox_lon]], weight=1)
        site_map.add_child(lines)

# Add Mouse Position to get the coordinate (Lat, Long) for a mouse over on the map
formatter = "function(num) {return L.Util.formatNum(num, 5);};"
mouse_position = MousePosition(
    position='topright',
    separator=' Long: ',
    empty_string='NaN',
    lng_first=False,
    num_digits=20,
    prefix='Lat:',
    lat_formatter=formatter,
    lng_formatter=formatter,
)

site_map.add_child(mouse_position)

# Display the map of the sites
site_map.save("site_map.html")
site_map
