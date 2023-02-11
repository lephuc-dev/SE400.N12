from utils import functions
from bs4 import BeautifulSoup
import cloudscraper
from utils.scores import scores
import json

data = []

page_sourse = functions.scraping_dynamic_web_pages(
    url='https://nomadlist.com/',
    time_rest=3,
)

# using Beautifulsoup retrieve data from html file

beautiful_soup = BeautifulSoup(page_sourse, 'html.parser')

cities = beautiful_soup.find('ul', {'class': 'grid'}).find_all(
    'li', {'data-type': 'city'})[:-1]
# list bug cities
bugged_cities = [
    '{slug}', 'essaouira', 'la-paz-mexico', 'faisalabad',
    'san-jose-costa-rica', 'la-serena', 'cordoba-spain',
    'macau', 'victoria-seychelles', 'george-town-cayman-islands'
]


# using cloudscraper  to bypass Cloudflare's anti-bot page

session = cloudscraper.create_scraper()
session.max_redirects = 3000

cities_with_all_criterias = []
city_id = 0

for city in cities:
    current_city = city['data-slug']
    print(f"City Name: {current_city}")

    if current_city in bugged_cities:
        continue

    city_url = 'https://nomadlist.com/' + current_city + '/'
    print(f'City URL: {city_url}')
    city_response = session.get(city_url)
    city_page = city_response.content

    city_soup = BeautifulSoup(city_page, 'html.parser')
    table = city_soup.find('table')
    if table:
        rows = table.find_all('tr')
    else:
        continue

    if rows:

        keys_class_pattern = {
            'Internet': 'internet',
            'Air quality now': 'air_quality',
            'Safety': 'safety',
        }

        keys_data_value_pattern = {
            'Quality of life score': 'quality_of_life_score',
            'Family score': 'family_score',
            'Fun': 'fun',
            'Education level': 'education_level',
            'English speaking': 'english_speaking',
            'Walkability': 'walkability',
            'Peace no pol conflict': 'peace',
            'Traffic safety': 'traffic_safety',
            'Hospitals': 'hospitals',
            'Happiness': 'happiness',
            'Nightlife': 'nightlife',
            'Free WiFi in city': 'free_wifi_in_city',
            'Places to work from': 'places_to_work_from',
            'AC or heating': 'ac_or_heating',
            'Friendly to foreigners': 'friendly_to_foreigners',
            'Freedom of speech': 'freedom_of_speech',
            'Female friendly': 'female_friendly',
            'LGBTQ friendly': 'lgbt_friendly',
            'Startup Score': 'startup_score'
        }

        current_city_criterias = {}

        for r in rows:
            key = r.find('td', {'class': 'key'}).text
            new_key = functions.extract_text(key)

            if new_key == 'Cost':
                criteria_name = 'cost'
                cost_text = r.find('div', {'class': 'filling'}).get_text()
                if cost_text:
                    cost_value = functions.format_cost(cost_text)
                    current_city_criterias[criteria_name] = cost_value
                    print(f'{criteria_name}: {cost_value}')  # float

            if new_key == 'Temperature now':
                criteria_name = 'temperature'
                temperature_text = r.find(
                    'span', {'class': 'metric'}).get_text()
                if temperature_text:
                    temperature_value = functions.string_to_int(
                        temperature_text)
                    current_city_criterias[criteria_name] = temperature_value
                    print(f'{criteria_name}: {temperature_value}')  # int

            if new_key == 'Humidity now':
                criteria_name = 'humidity'
                humidity_text = r.find(
                    'div', {'class': 'filling'}).get_text()
                if humidity_text:
                    humidity_value = functions.format_humidity(
                        humidity_text)
                    current_city_criterias[criteria_name] = humidity_value
                    print(f'{criteria_name}: {humidity_value}')  # int

            if new_key == 'Total score':
                criteria_name = 'total_score'
                overall_score_text = r.find('div', {'class': 'filling'}).find(
                    'span', {'xitemprop': 'ratingValue'}, recursive=False).text
                if overall_score_text:
                    overall_score_value = float(overall_score_text)
                    current_city_criterias[criteria_name] = overall_score_value
                    print(f'{criteria_name}: {overall_score_value}')  # float

            if new_key in keys_data_value_pattern:
                criteria_name = keys_data_value_pattern[new_key]
                criteria_field = r.find('div', {'class': 'rating'})
                if criteria_field and criteria_field.has_attr('data-value'):
                    criteria_value = int(criteria_field['data-value'][0])
                    current_city_criterias[criteria_name] = criteria_value
                    print(f'{criteria_name}: {criteria_value}')  # int

            if new_key in keys_class_pattern:
                criteria_name = keys_class_pattern[new_key]
                criteria_field = r.find('div', {'class': 'rating'})
                if criteria_field:
                    criteria_value = int(criteria_field['class'][-1][1])
                    current_city_criterias[criteria_name] = criteria_value
                    print(f'{criteria_name}: {criteria_value}')  # int

        has_all_criterias = True
        for score in scores:
            if score not in current_city_criterias:
                has_all_criterias = False
                break

        # print(f'City {current_city} has all criterias: {has_all_criterias}')
        # print()

        if has_all_criterias:
            city_id += 1
            cities_with_all_criterias.append(
                {'city': current_city, 'url': city_url})
            data.append({'nr': city_id, 'fields': {}})
            criterias_dict = data[-1]['fields']

            criterias_dict['city'] = current_city
            for criteria_name in scores:
                criterias_dict[criteria_name] = current_city_criterias[criteria_name]

print(f'Cities that have all the attributes: {cities_with_all_criterias}')
print(f'Data: {data}')

with open('files/analyze-data.json', 'w') as outfile:
    json.dump(data, outfile)
