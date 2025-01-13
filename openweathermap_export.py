import json
import requests

city_name=input('Enter the city name: ')
api_key='a43aade87cee5978c43c0cf0f574dba7'
api_url=f'https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric'
get_server_information=requests.get(api_url)
json_data=get_server_information.json()

pretty_data=json.dumps(json_data, indent=4, sort_keys=True)
#print(pretty_data)

D=json_data["main"]["temp"]
T=json_data["weather"][0]["description"]
print(D)
print(T)

