import datetime
import time
import json
import csv
import os
import requests

# open csv file 
# write file for one row every time
def csv_write(c_path,c_data):
    with open(c_path, mode="a", encoding="utf-8", newline="",errors='ignore') as f:
        csv.writer(f).writerow(c_data)

def request_get(c_url):
    response = requests.get(c_url,verify=True,allow_redirects=True)
    response_result = response.content.decode("utf-8")
    return response_result

res_text = request_get(f'http://api.weatherapi.com/v1/forecast.json?key=6fef7d9d5ae343deab5102111221610&q=Perth&days=15&aqi=no&alerts=no')
res_json = json.loads(res_text)

save_path = f'forecast.csv'

if(os.path.exists(save_path)):
    os.remove(save_path)
csv_write(save_path,['timestamp', 'temperature(celcius)', 'dew_point(celcius)', 'humidity(%)', 'Wind', 'wind_speed(mph)', 'wind_gush(mph)', 'pressure(in)', 'precip.(in)', 'Condition'])

end_date = None

item_list = res_json['forecast']['forecastday']
for each_day in item_list:
    for item in each_day['hour']:
        info_time = item['time'] # Time
        info_temp = f"{item['temp_c']}" # Temperature
        info_dewpt = f"{item['dewpoint_c']}" # Dew Point
        info_rh =  f"{item['humidity']}" # Humidity
        info_wdir = item['wind_dir'] # Wind
        info_wspd =  f"{item['wind_mph']}"  # Wind Speed
        info_gust = '0' if item['gust_mph'] == None else f"{item['gust_mph']}" # Wind Gust
        info_pressure = f"{item['pressure_in']}"  # Pressure
        info_phrase = item['condition']['text'] # Condition
        write_data = [info_time,info_temp,info_dewpt,info_rh,info_wdir,info_wspd,info_gust,info_pressure,info_phrase]
        csv_write(save_path,write_data)
        end_date = info_time

print("Weather forecast fetched till", end_date)
        