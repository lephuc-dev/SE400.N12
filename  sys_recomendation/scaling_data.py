import json

from sklearn.preprocessing import MinMaxScaler

from utils import functions
from utils.criteria import selected_set_3 as city_features

df, city_names, line_index_in_df = functions.read_data_from_json(
    file_path='./files/set-3.json',
    city_features=city_features
)

input_data = df.values
input_data_scaled = MinMaxScaler().fit_transform(input_data)
scaled_data = []

for city in city_names:
    idx = line_index_in_df[city]
    curr_line = {'city': city}

    df_column_idx = 0
    for feature_name in city_features:
        field_name = feature_name + '_scaled'
        curr_line[field_name] = input_data_scaled[idx][df_column_idx]
        df_column_idx += 1

    scaled_data.append(curr_line)

with open(output_scaled_data_file_path, 'w') as outfile:
    json.dump(scaled_data, outfile)