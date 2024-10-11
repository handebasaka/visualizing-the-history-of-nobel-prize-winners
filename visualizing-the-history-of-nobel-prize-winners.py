# Import libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Read datasets (you need to provide the related file path where your files saved)
nobel = pd.read_csv('./data/nobel.csv')
print(nobel.sample(5))

# Check NaNs
nobel.info()

# region Question-1

# Filter only women winners, find the first (oldest) one
first_woman = nobel[nobel['sex'] == 'Female'].sort_values('year', ascending= True).head(1)
# Print the answer
print(f"Answer 1: The first woman to win a Nobel Prize was {first_woman['full_name'].values[0]}, in the category of {first_woman['category'].values[0]}.")
# endregion

# region Question-2

# Find the decades from year
nobel['decade'] = (nobel['year'] - nobel['year'] % 10).astype(str) + 's'

# Find the total number of winners for each decade
nobel_decades = nobel.groupby('decade')['decade'].count().reset_index(name= 'counts')
print(nobel_decades)

# Visualize total winners over the decades
# Set the theme and size of the plot
plt.figure(figsize=(12,8))
sns.set_theme(style= 'darkgrid', palette='Set2')

# Create the plot, change the title
sns.barplot(data= nobel_decades, x= 'decade', y= 'counts')
plt.title('Nobel Prize Winners Over The Decades', fontsize= 18)

# Change labels and their settings
plt.xlabel('Decade', fontsize= 16)
plt.xticks(fontsize= 16)
plt.ylabel('Number of Winners', fontsize= 16)
plt.yticks(fontsize= 16)

# Show the plot
plt.show();
# endregion

# region Question-3

# Count the full_name in the data
prize_number = nobel['full_name'].value_counts().reset_index(name= 'prize_number').sort_values('prize_number', ascending= False)
# Filter them if the count is greater than 1
multiple_prize = prize_number[prize_number['prize_number'] > 1]

# Filter winners who won multiple nobel from the nobel data
multiple_prize_full_data = nobel[nobel['full_name'].isin(multiple_prize['full_name'].tolist())]

# Visualize multiple nobel prize winners
# Set the theme and size of the plot
plt.figure(figsize=(8,6))
sns.set_theme(style= 'darkgrid', palette='Set2')

# Create the plot, change the title and legend
sns.scatterplot(data= multiple_prize_full_data, y= 'full_name', x= 'year', hue= 'category', s= 200)
plt.title('Multiple Nobel Prize Winners', fontsize= 18)
plt.legend(title= 'Category')

# Change labels and their settings
plt.xlabel('Year', fontsize= 14)
plt.xticks(fontsize= 12)
plt.ylabel('')
plt.yticks(fontsize= 12)

# Show the plot
plt.show();
# endregion

# region Question-4

# Find the ratio of male and female winners in the total
gender_ratio = nobel['sex'].value_counts(normalize= True)
print(gender_ratio)

# Visualize winners by gender and category
# Set the theme and size of the plot
sns.set_theme(style= 'darkgrid', palette='Set2')

# Create an order for categories to see clearly the difference (you can order by male or female)
cat_order = nobel[nobel['sex'] == 'Male'].groupby(['category', 'sex'])['full_name'].count().reset_index(name= 'counts').sort_values('counts', ascending= False)['category']

# Create the plot, change the title and legend
sns.catplot(data= nobel, kind= 'count', x= 'sex', hue= 'category', height= 6, aspect= 1.33, legend_out= False, hue_order = cat_order)
plt.title('Distribution of Nobel Prize Winners by Gender and Category', fontsize= 18)
plt.legend(title= 'Category')

# Change labels and their settings
plt.xlabel('Gender', fontsize= 14)
plt.xticks(fontsize= 12)
plt.ylabel('Number of Winners', fontsize= 14)
plt.yticks(fontsize= 12)

# Show the plot
plt.show();
# endregion

# region Question-5

# Glance at sample of birth_country
nobel['birth_country'].sample(10)

# OR
# nobel['birth_country'].unique()

# Read new dataset (you need to provide the related file path where your files saved)
country_fixed = pd.read_csv('./data/country_fixed.csv')
# Merge country_fixed data to add standardized country and continent info
nobel = nobel.merge(country_fixed, on= 'birth_country', how= 'left')
print(nobel.sample(5))

# Find the total number of winners for each fixed_birth_country and order by continent and counts
nobel_continent = nobel.groupby(['continent', 'fixed_birth_country'])['fixed_birth_country'].count().reset_index(name= 'counts').sort_values(['continent', 'counts'], ascending= [True, False])

# Visualize winners by birth country and continent
# Set the theme and size of the plot
plt.figure(figsize=(30,12))
sns.set_theme(style= 'darkgrid', palette='Set2')

# Create the plot, change the title and legend
sns.barplot(data= nobel_continent, x= 'fixed_birth_country', y= 'counts', hue= 'continent')
plt.title('Nobel Prize Winners by Birth Country and Continent', fontsize= 24)
plt.legend(title= 'Continent', title_fontsize= 20, fontsize= 20)

# Change labels and their settings
plt.xlabel('Birth Country', fontsize= 18)
plt.xticks(fontsize= 14, rotation= 45)
plt.ylabel('Number of Winners', fontsize= 18)
plt.yticks(fontsize= 16)

# Show the plot
plt.show();

# Visualize winners by birth country and for one continent
# Set the theme and size of the plot
plt.figure(figsize=(15,10))
sns.set_theme(style= 'darkgrid', palette='Set2')

# Add new variable to filter data, lets say we want to look at Asia
filter_continent = 'Asia'

# Create the plot, change the title and legend
sns.barplot(data= nobel_continent[nobel_continent['continent'] == filter_continent], x= 'fixed_birth_country', y= 'counts', hue= 'continent')
plt.title(f"Nobel Prize Winners by Birth Country for {filter_continent}", fontsize= 20)
plt.legend(title= 'Continent', title_fontsize= 16, fontsize= 16)

# Change labels and their settings
plt.xlabel('Birth Country', fontsize= 16)
plt.xticks(fontsize= 14, rotation= 45)
plt.ylabel('Number of Winners', fontsize= 16)
plt.yticks(fontsize= 14)

# Show the plot
plt.show();
# endregion

# region Question-6

# Visualize winners by gender and continent
# Set the theme and size of the plot
plt.figure(figsize=(15,10))
sns.set_theme(style= 'darkgrid', palette='Set2')

# Create the plot, change the title and legend
ax = sns.histplot(data= nobel, x= 'continent', hue= 'sex', multiple= 'dodge', shrink= 0.8)
plt.title('Distribution of Nobel Prize Winners by Gender and Continent (Based on Birth Country)', fontsize= 18)
ax.legend_.set_title('Gender')

# Loop through containers and add annotations
for container in ax.containers:
    ax.bar_label(container, fontsize=12, color='dimgray', label_type='edge')

# Change labels and their settings
plt.xlabel('Continent', fontsize= 14)
plt.xticks(fontsize= 12)
plt.ylabel('Number of Winners', fontsize= 14)
plt.yticks(fontsize= 12)

# Show the plot
plt.show();
# endregion
