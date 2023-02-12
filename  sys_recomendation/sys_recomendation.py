import json
import math
import pandas as pd

from utils.criteria import selected_set_3 as city_features


def read_scaled_data_from_json(file_path, features_names):
    scaled_features_names = [name + '_scaled' for name in features_names]
    df = pd.DataFrame(columns=scaled_features_names)
    line_index_in_dataframe = {}

    with open(file_path) as input_file:
        loaded_json = json.load(input_file)

        pandas_idx = 0
        for line in loaded_json:
            pandas_line = []
            current_city_name = line['city']

            for feature in scaled_features_names:
                pandas_line.append(line[feature])

            df.loc[pandas_idx] = pandas_line
            line_index_in_dataframe[current_city_name] = pandas_idx
            pandas_idx += 1

    return df, line_index_in_dataframe


def get_clustering_information(file_clusters_path, file_cities_info_path):
    clusters_info = {}
    city_in_cluster = {}

    with open(file_clusters_path) as clusters_file:
        loaded_json = json.load(clusters_file)

        for line in loaded_json:
            cluster_id = line['cluster_id']
            cluster_cities = line['cities']

            clusters_info[cluster_id] = cluster_cities

    with open(file_cities_info_path) as cities_info:
        loaded_json = json.load(cities_info)

        for line in loaded_json:
            current_dict = line['fields']
            current_city_name = current_dict['city']
            current_city_cluster_id = current_dict['id_cluster']

            city_in_cluster[current_city_name] = current_city_cluster_id

    return clusters_info, city_in_cluster


def l2_distance(city_1, city_2):
    loss = 0
    for idx in range(len(city_1)):
        loss += (city_1[idx] - city_2[idx]) ** 2

    loss = math.sqrt(loss)
    return loss

scaled_df, line_index_in_df = read_scaled_data_from_json(
        file_path="./scale-data/scaled-data-test-3.json",
        features_names=city_features
    )

scaled_values = scaled_df.values
total_nr_cities = len(scaled_values)

clusters, in_cluster = get_clustering_information(
    file_clusters_path='./kmeans/files/test-3/clusters-test-3.json',
    file_cities_info_path='./kmeans/files/test-3/fixture-test-3.json'
)

print(clusters)
print("============================================")
print(in_cluster)
