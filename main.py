
import requests
import csv

city_list = [ #static list because I don't want all cities
    ('NewYork', 1),
    ('Chicago', 3),
    ('WashingtonDC', 6),
    ('Boston', 11)
]

URL = "https://api.biltrewards.com/seated/restaurants?"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# saving for later to query the cities table rather than static list
# cities = []
# CITY_URL = "https://api.biltrewards.com/seated/cities/"
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

    while True:

        response = requests.get(f"{URL}&city_id={city_id}&sort_by=rating&page={page}")
        response.raise_for_status()
        data = response.json()

        for place in data['restaurants']:
            # Extract the restaurant details
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
            coordinates = latitude, longitude #using coordinates to avoid errors in uploading on MyMaps (address updates weren't working
            if primary_cuisine == ('Drinks' or 'Bars & Breweries'): #create isBar variable to ease MyMaps labeling later
                isBar = 'Bar'
            else:
                isBar = 'Restaurant'
            points = place['multiplier']['monday']

            places.append([name, rating, menu_url, primary_cuisine, address, coordinates, points, isBar])


        if not data['meta_data']['has_more_items']: # checks the meta_data in the JSON to determine if there are more pages of data to query.
            break
        page += 1


    with open(f"{city}_restaurants.csv", 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["Name", "Rating", "Menu Link", "Cuisine", "Address", "Lat/Long", "Bilt Points", "Is Bar?"])  # Header row
        writer.writerows(places)

