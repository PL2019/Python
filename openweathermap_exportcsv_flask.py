from flask import Flask, request, render_template, send_file
import requests
import pandas as pd

app = Flask(__name__)

API_KEY = 'a43aade87cee5978c43c0cf0f574dba7'
BASE_URL = 'https://api.openweathermap.org/data/2.5/weather'

@app.route('/')
def index():
    return '''
    <h1>Weather Data App</h1>
    <form action="/upload" method="post" enctype="multipart/form-data">
        <label for="file">Upload a CSV file with locations:</label><br>
        <input type="file" name="file" id="file"><br><br>
        <input type="submit" value="Upload">
    </form>
    '''

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file uploaded!', 400

    file = request.files['file']
    locations_df = pd.read_csv(file)
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
    output_file = 'location_temperatures.csv'
    output_df.to_csv(output_file, index=False)
    return send_file(output_file, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)