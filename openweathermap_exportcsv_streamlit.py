import streamlit as st
import requests
import pandas as pd

API_KEY = 'a43aade87cee5978c43c0cf0f574dba7'
BASE_URL = 'https://api.openweathermap.org/data/2.5/weather'

st.title("Retrieve temp value via openWeathermap api V1.0")

uploaded_file = st.file_uploader("Upload a CSV file with locations", type=["csv"])
if uploaded_file:
    locations_df = pd.read_csv(uploaded_file)
    results = []

    for _, row in locations_df.iterrows():
        city_name = row['location']
        try:
            response = requests.get(f"{BASE_URL}?q={city_name}&appid={API_KEY}&units=metric")
            response.raise_for_status()
            data = response.json()
            temperature = data["main"]["temp"]
            results.append({"location": city_name, "temperature": temperature})
        except requests.exceptions.RequestException:
            results.append({"location": city_name, "temperature": None})

    output_df = pd.DataFrame(results)
    st.write("Results:", output_df)
    st.download_button(
        label="Download CSV",
        data=output_df.to_csv(index=False),
        file_name="location_temperatures.csv",
        mime="text/csv",
    )
