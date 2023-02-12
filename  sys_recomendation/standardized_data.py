import json

from utils.criteria import selected_set_2 as selected_set

if len(selected_set) == 26:
    output_file_path = './files/analyze-data.json'
elif len(selected_set) == 5:
    output_file_path = './files/set-1.json'
elif len(selected_set) == 4:
    output_file_path = './files/set-2.json'
else:
    output_file_path = './files/set-3.json'

set_data=[]

with open('./files/analyze-data.json', 'r') as f:
  data = json.load(f)

city_id=1

for item in data:

    temp={}
    temp["city"]=item["fields"]["city"]
    for atrr in selected_set:
        temp[atrr]=item["fields"][atrr]

    set_data.append({'nr': city_id, 'fields': temp})
    city_id+=1

with open(output_file_path, 'w') as outfile:
        json.dump(set_data, outfile)
