import cloudscraper
import json
from bs4 import BeautifulSoup
from utils.criteria import selected_set_3 as selected_set
from utils import functions

set_data=[]

with open('./files/analyze-data.json', 'r') as f:
  data = json.load(f)

city_id=1

for item in data:

    temp={}
    temp["city"]=item["fields"]["city"]
    for atrr in selected_set:
        temp[atrr]=item["fields"][atrr]

    set_data.append({'model': 'app.city', 'pk': city_id, 'fields': temp})

with open("./files/set-3.json", 'w') as outfile:
        json.dump(set_data, outfile)
