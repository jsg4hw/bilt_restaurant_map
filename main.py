# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


import requests
# from bs4 import BeautifulSoup
import csv

# city_ids = {
#     'New York': 1
#     # 'Chicago': 3,
#     # 'Boston': 11,
#     # 'DC': 6
# }

city_list = [
    ('NewYork', 1),
    ('Chicago', 3),
    ('WashingtonDC', 6),
    ('Boston', 11)
]

CITY_URL = "https://api.biltrewards.com/seated/cities/"

# URL = "https://api.biltrewards.com/seated/restaurants?city_id=3&sort_by=rating"
URL = "https://api.biltrewards.com/seated/restaurants?"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# cities = []
# city_ping = requests.get(CITY_URL, headers=HEADERS)
# city_ping.raise_for_status()
# city_data = city_ping.json()
#
# for city in city_data:
#     city_id = city['id']
#     city_name = city['name']
#
#     cities.append([city_id, city_name])

places = []
for city, city_id in city_list:

    page = 0
    # response0 = requests.get(f"{URL}&city_id={city_id}&sort_by=rating")
    # data0 = response0.json()
    # page = data0['meta_data']['page_number']

    while True:

        response = requests.get(f"{URL}&city_id={city_id}&sort_by=rating&page={page}")
        response.raise_for_status()
        data = response.json()

        # print(data['meta_data']['page_number'])
        # print(data['meta_data']['has_more_items'])

        for place in data['restaurants']:
            # Extract the desired details. Again, the class names used below are placeholders and should be updated accordingly.
            name = place['name']
            rating = place['rating']
            menu_url = place['menu_url']
            if place['primary_cuisine'] is not None:
                primary_cuisine = place['primary_cuisine'].get('name', 'Unknown')
            else:
                primary_cuisine = 'Unknown'
            address = place['address']
            latitude = place['latitude']
            longitude = place['longitude']
            coordinates = latitude, longitude
            if primary_cuisine == ('Drinks' or 'Bars & Breweries'):
                isBar = 'Bar'
            else:
                isBar = 'Restaurant'
            points = place['multiplier']['monday']
            # description = place['description']


            # places.append([name, rating, menu_url, primary_cuisine, address, points, description])
            places.append([name, rating, menu_url, primary_cuisine, address, coordinates, points, isBar])


        if not data['meta_data']['has_more_items']: # checks the meta_data in the JSON to determine if there are more pages of data to query.
            break
        page += 1        #If there are, it adds 1 to the page number


    with open(f"{city}_restaurants.csv", 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        # writer.writerow(["Name", "Rating", "Menu Link", "Cuisine", "Address", "Points", "Description"])  # Header row.
        writer.writerow(["Name", "Rating", "Menu Link", "Cuisine", "Address", "Lat/Long", "Bilt Points", "Is Bar?"])  # Header row
        writer.writerows(places)

# if __name__ == "__main__":
#     restaurants = get_restaurants_info(URL)
#     write_to_csv(restaurants)
