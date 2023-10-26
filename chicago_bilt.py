import requests
import csv

URL = "https://api.biltrewards.com/seated/restaurants?city_id=3&sort_by=rating"
# URL = "https://api.biltrewards.com/seated/restaurants?city_id=3"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

places = []
page = 0
while True:
    response = requests.get(f"{URL}&page={page}")
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
        points = place['multiplier']['monday']
        description = place['description']

        places.append([name, rating, menu_url, primary_cuisine, address, points, description])

    if not data['meta_data']['has_more_items']: # checks the meta_data in the JSON to determine if there are more pages of data to query.
        break
    page += 1        #If there are, it adds 1 to the page number


with open('chicago_restaurants.csv', 'w', newline='') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(["Name", "Rating", "Menu Link", "Cuisine", "Address", "Points", "Description"])  # Header row.
    writer.writerows(places)

# if __name__ == "__main__":
#     restaurants = get_restaurants_info(URL)
#     write_to_csv(restaurants)
