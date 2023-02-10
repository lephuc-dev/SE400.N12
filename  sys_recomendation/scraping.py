from utils import functions
from bs4 import BeautifulSoup
import cloudscraper

data = []

page_sourse = functions.scraping_dynamic_web_pages(
    url='https://nomadlist.com/',
    time_rest=3,
)

# using Beautifulsoup retrieve data from html file

beautiful_soup = BeautifulSoup(page_sourse, 'html.parser')

cities = beautiful_soup.find('ul', {'class': 'grid'}).find_all(
    'li', {'data-type': 'city'})[:-1]

# using cloudscraper  to bypass Cloudflare's anti-bot page

session = cloudscraper.create_scraper()
session.max_redirects = 3000
