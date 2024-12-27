# Import libraries
import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Fetch the API response
url = 'http://api.nobelprize.org/2.1/laureates'
params = {'limit': 100, # each request will fetch up to 100 records
          'offset': 0}  # where the API should start fetching data
temp_nobel = []

while True:
    response = requests.get(url, params= params)
    
    # Check for response errors 
    if response.status_code >= 300:
        print(f'Failed to fetch data. Status code: {response.status_code}')
        break
    
    # Parse the response data
    data = response.json()
    laureates = data.get('laureates', [])

    # Break if no laureates are found
    if not laureates:
        break

    # Iterate through each laureate
    for laureate in laureates:
        # Check if the laureate is an organization
        if 'orgName' in laureate:
            for prize in laureate.get('nobelPrizes', []):
                # Add laureate and prize data
                temp_nobel.append({
                    'id': laureate.get('id'),
                    'year' : prize.get('awardYear', 'NaN'),
                    'category': prize.get('category', {}).get('en', 'NaN'),
                    'laureate_type': 'Organization',
                    'full_name': laureate.get('orgName', {}).get('en', 'NaN'),
                    'org_city_now': laureate.get('founded', {}).get('place', {}).get('cityNow', {}).get('en', 'NaN'),
                    'org_country_now': laureate.get('founded', {}).get('place', {}).get('countryNow', {}).get('en', 'NaN'),
                    'org_continent': laureate.get('founded', {}).get('place', {}).get('continent', {}).get('en', 'NaN'),
                    'prize_share': prize.get('portion', 'NaN'),
                    'prize': prize.get('categoryFullName', {}).get('en', 'NaN') + ' ' + prize.get('awardYear', 'NaN'),
                    'motivation': prize.get('motivation', {}).get('en', 'NaN'),
                })
        # Check if the laureate is an individual
        elif 'fullName' in laureate:
            for prize in laureate.get('nobelPrizes', []):
                # Process affiliations dynamically (because an individual may have more than one affiliation)
                affiliations = prize.get('affiliations', [])
                affiliation_data = {}
                
                # Map each affiliation to a key with a numbered suffix
                for idx, affiliation in enumerate(affiliations, start= 1):
                    affiliation_data[f'affiliation_{idx}_name'] = affiliation.get('nameNow', {}).get('en', 'NaN')
                    affiliation_data[f'affiliation_{idx}_city'] = affiliation.get('cityNow', {}).get('en', 'NaN')
                    affiliation_data[f'affiliation_{idx}_country'] = affiliation.get('countryNow', {}).get('en', 'NaN')

                temp_nobel.append({
                    'id': laureate.get('id'),
                    'year': prize.get('awardYear', 'NaN'),
                    'category': prize.get('category', {}).get('en', 'NaN'),
                    'laureate_type': 'Individual',
                    'full_name': laureate.get('fullName', {}).get('en', 'NaN'),
                    'gender': laureate.get('gender'),
                    'birth_date': laureate.get('birth', {}).get('date', 'NaN'),
                    'birth_city': laureate.get('birth', {}).get('place', {}).get('city', {}).get('en', 'NaN'),
                    'birth_city_now': laureate.get('birth', {}).get('place', {}).get('cityNow', {}).get('en', 'NaN'),
                    'birth_country': laureate.get('birth', {}).get('place', {}).get('country', {}).get('en', 'NaN'),
                    'birth_country_now': laureate.get('birth', {}).get('place', {}).get('countryNow', {}).get('en', 'NaN'),
                    'birth_city': laureate.get('birth', {}).get('place', {}).get('city', {}).get('en', 'NaN'),
                    'birth_continent': laureate.get('birth', {}).get('place', {}).get('continent', {}).get('en', 'NaN'),
                    'death_date': laureate.get('death', {}).get('date', 'NaN'),
                    'prize_share': prize.get('portion', 'NaN'),
                    'prize': prize.get('categoryFullName', {}).get('en', 'NaN') + ' ' + prize.get('awardYear', 'NaN'),
                    'motivation': prize.get('motivation', {}).get('en', 'NaN'),
                    **affiliation_data # Add affiliation data dynamically
                })
        else:
            print('No valid data found in laureate')

    # Update offset for the next batch
    params['offset'] += params['limit']

# Convert the list to a DataFrame
nobel = pd.DataFrame(temp_nobel)

# Save the dataset as a csv
nobel.to_csv('./data/nobel.csv')

# Check NaNs and data types
nobel.info()

# Change data types if needed
nobel['id'] = nobel['id'].astype(int)
nobel['year'] = nobel['year'].astype(int)

# region Question-1

# Filter only women winners, find the first (oldest) one
first_woman = nobel[nobel['gender'] == 'female'].sort_values('year', ascending= True).head(1)
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
print(multiple_prize)


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
gender_ratio = nobel['gender'].value_counts(normalize= True)
print(gender_ratio)

# Visualize winners by gender and category
# Set the theme and size of the plot
sns.set_theme(style= 'darkgrid', palette='Set2')

# Create an order for categories to see clearly the difference (you can order by male or female)
cat_order = nobel[nobel['gender'] == 'male'].groupby(['category', 'gender'])['full_name'].count().reset_index(name= 'counts').sort_values('counts', ascending= False)['category']

# Create the plot, change the title and legend
sns.catplot(data= nobel, kind= 'count', x= 'gender', hue= 'category', height= 6, aspect= 1.33, legend_out= False, hue_order = cat_order)
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

# Find the total number of winners for each birth_country_now and order by continent and counts
nobel_continent = nobel.groupby(['birth_continent', 'birth_country_now'])['birth_country_now'].count().reset_index(name= 'counts').sort_values(['birth_continent', 'counts'], ascending= [True, False])

# Visualize winners by birth country and for one continent
# Set the theme and size of the plot
plt.figure(figsize=(15,10))
sns.set_theme(style= 'darkgrid', palette='Set2')

# Add new variable to filter data, lets say we want to look at Asia
filter_continent = 'Asia'

# Create the plot, change the title and legend
sns.barplot(data= nobel_continent[nobel_continent['birth_continent'] == filter_continent], x= 'birth_country_now', y= 'counts', hue= 'birth_continent')
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
ax = sns.histplot(data= nobel[nobel['birth_continent'] != 'NaN'], x= 'birth_continent', hue= 'gender', multiple= 'dodge', shrink= 0.8)
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