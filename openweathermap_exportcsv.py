import json
import requests
import pandas as pd

# Define API key and base URL
api_key = 'a43aade87cee5978c43c0cf0f574dba7'
base_url = 'https://api.openweathermap.org/data/2.5/weather'

# Read the CSV file with location names
input_csv = "locations.csv"  # Update this with the path to your input CSV
output_csv = "location_temperatures.csv"  # Output file

# Read locations from the input CSV
locations_df = pd.read_csv(input_csv)

# Prepare an empty list to store the results
results = []

# Iterate through each location
for index, row in locations_df.iterrows():
    city_name = row['location']  # Assuming the column name is 'location'
    api_url = f'{base_url}?q={city_name}&appid={api_key}&units=metric'

    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Raise an error for bad status codes
        data = response.json()

        # Extract temperature from the API response
        temperature = data["main"]["temp"]
        results.append({"location": city_name, "temperature": temperature})
        print(f"Retrieved temperature for {city_name}: {temperature}°C")

    except requests.exceptions.RequestException as e:
        print(f"Failed to retrieve data for {city_name}: {e}")
        results.append({"location": city_name, "temperature": None})  # Log None for failed requests

# Convert the results to a DataFrame
output_df = pd.DataFrame(results)

# Save results to a new CSV file
output_df.to_csv(output_csv, index=False)
print(f"Temperature data saved to {output_csv}")
