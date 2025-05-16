import requests
from bs4 import BeautifulSoup
import json


website = "https://www.bbc.com/weather/"

def scrape(url):
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        location_element = soup.find('h1', id='wr-location-name-id')

        if location_element:
            location_name = location_element.text.strip()
            temperature_element = soup.find('span', class_='wr-value--temperature--c')

            if temperature_element:
                temperature = temperature_element.text
                location_name = location_name.replace(" - Weather warnings issued", "")
                return f'The current temperature in {location_name} is {temperature}'
            else:
                return 'Temperature element not found on the page.'
        else:
            return 'Location element not found on the page.'
    else:
        return f'Failed to retrieve the web page. Status code: {response.status_code}'



with open(f"codes.json", "r") as file:
    city_codes = json.load(file)

user_input = input("Enter a city: ").lower().replace(" ", "")

for country, cities in city_codes.items():
    if user_input in cities:
        url = website + cities[user_input]
        print(scrape(url))
        break
else:
    print("City not found.")