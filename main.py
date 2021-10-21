import requests
import json


def get_data():
    return requests.get('http://open.tan.fr/ewp/tempsattente.json/ICAM')

def get_information():
    data = get_data()
    json_string = data.text
    return json_string


#def parse_data(json_string):
    
data = get_information().split()[0]
print(json.load(data))
    