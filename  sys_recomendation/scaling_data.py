import json

from sklearn.preprocessing import MinMaxScaler

from utils import functions
from utils.criteria import selected_set_2 as set_selected

if len(set_selected) == 26:
    _file_path = './files/analyze-data.json'
    output_file_path = "./scale_data/scaled-data-all-features.json"
elif len(set_selected) == 5:
    _file_path = './files/set-1.json'
    output_file_path = "./scale_data/scaled-data-test-1.json"
elif len(set_selected) == 4:
    _file_path = './files/set-2.json'
    output_file_path = "./scale_data/scaled-data-test-2.json"
else:
    _file_path = './files/set-3.json'
    output_file_path = "./scale_data/scaled-data-test-3.json"

df, city_names, line_index_in_df = functions.read_data_from_json(
    file_path=_file_path,
    city_features=set_selected
)


input_data = df.values
input_data_scaled = MinMaxScaler().fit_transform(input_data)
scaled_data = []

for city in city_names:
    idx = line_index_in_df[city]
    curr_line = {'city': city}

    df_column_idx = 0
    for feature_name in set_selected:
        field_name = feature_name + '_scaled'
        curr_line[field_name] = input_data_scaled[idx][df_column_idx]
        df_column_idx += 1

    scaled_data.append(curr_line)

with open(output_file_path, 'w') as outfile:
    json.dump(scaled_data, outfile)
