# pandas is a software library written for the Python programming language for data manipulation and analysis.
import pandas as pd
#NumPy is a library for the Python programming language, adding support for large, multi-dimensional arrays and matrices, along with a large collection of high-level mathematical functions to operate on these arrays
import numpy as np
# Matplotlib is a plotting library for python and pyplot gives us a MatLab like plotting framework. We will use this in our plotter function to plot data.
import matplotlib.pyplot as plt
#Seaborn is a Python data visualization library based on matplotlib. It provides a high-level interface for drawing attractive and informative statistical graphics
import seaborn as sns

URL = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/dataset_part_2.csv"
df=pd.read_csv(URL)
print(df.head(5))

# First, let's try to see how the FlightNumber (indicating the continuous launch attempts.) and Payload variables would affect the launch outcome.
#
# We can plot out the FlightNumber vs. PayloadMassand overlay the outcome of the launch. We see that as the flight number increases, the first stage is more likely to land successfully. The payload mass is also important;
# it seems the more massive the payload, the less likely the first stage will return.

sns.catplot(y="PayloadMass", x="FlightNumber", hue="Class", data=df, aspect = 5)
plt.xlabel("Flight Number",fontsize=20)
plt.ylabel("Pay load Mass (kg)",fontsize=20)
plt.show()

# We see that different launch sites have different success rates. CCAFS LC-40, has a success rate of 60 %, while KSC LC-39A and VAFB SLC 4E has a success rate of 77%.
# Next, let's drill down to each site visualize its detailed launch records.
### TASK 1: Visualize the relationship between Flight Number and Launch Site

sns.catplot(y="LaunchSite", x="FlightNumber", hue="Class", data=df, aspect=2)
plt.xlabel("Flight Number", fontsize=20)
plt.ylabel("Launch Site", fontsize=20)
plt.title('Flight Number vs Launch Site', fontsize=20)
plt.show()

# Task 2: Plot a scatter plot to visualize the relationship between Payload and Launch Site
sns.catplot(y="LaunchSite", x="PayloadMass", hue="Class", data=df, aspect=2)
plt.xlabel("Payload Mass (kg)", fontsize=20)
plt.ylabel("Launch Site", fontsize=20)
plt.title('Payload Mass vs Launch Site', fontsize=20)
plt.show()

# Task 3: Visualize the launch outcome for each orbit
sns.catplot(y="Orbit", x="FlightNumber", hue="Class", data=df, aspect=2)
plt.xlabel("Flight Number", fontsize=20)
plt.ylabel("Orbit", fontsize=20)
plt.title('Flight Number vs Orbit', fontsize=20)
plt.show()

# Task 4: Create a bar chart for the success rate of each orbit
success_rates = df.groupby('Orbit')['Class'].mean().reset_index()
success_rates.columns = ['Orbit', 'Success Rate']
sns.barplot(x='Orbit', y='Success Rate', data=success_rates)
plt.xlabel("Orbit", fontsize=20)
plt.ylabel("Success Rate", fontsize=20)
plt.title('Success Rate by Orbit', fontsize=20)
plt.xticks(rotation=45)
plt.show()

# Task 5: Plot a heatmap of the correlation between different features
# Filter the dataframe to include only numeric columns
numeric_df = df.select_dtypes(include=[np.number])

# Plot a heatmap of the correlation between numeric features
plt.figure(figsize=(12, 8))
sns.heatmap(numeric_df.corr(), annot=True, cmap='coolwarm', linewidths=.5)
plt.title('Correlation Heatmap', fontsize=20)
plt.show()

# Task 6: Visualize the distribution of Payload Mass
plt.figure(figsize=(10, 6))
sns.histplot(df['PayloadMass'], kde=True, bins=30)
plt.xlabel("Payload Mass (kg)", fontsize=20)
plt.ylabel("Frequency", fontsize=20)
plt.title('Distribution of Payload Mass', fontsize=20)
plt.show()

### TASK  7: Create dummy variables to categorical columns
categorical_columns = ['BoosterVersion', 'LaunchSite', 'Outcome', 'Orbit', 'GridFins', 'Reused', 'Legs', 'LandingPad', 'Serial']
df_dummies = pd.get_dummies(df, columns=categorical_columns)
print(df_dummies.head())

### TASK  8: Cast all numeric columns to `float64`
df_dummies = df_dummies.astype({col: 'float64' for col in df_dummies.select_dtypes(include=[np.number]).columns})

# Verify the data types to ensure all numeric columns are now float64
print(df_dummies.dtypes)








