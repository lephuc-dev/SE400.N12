
import json
import matplotlib.pyplot as plt

from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

from utils.functions import read_data_from_json
from utils.criteria import selected_set_3


def find_best_nr_of_clusters(X, nr_clusters_to_be_tested):
    y_values = []

    best_ncl = -1
    best_score = 0
    for ncl in nr_clusters_to_be_tested:
        km = KMeans(n_clusters=ncl, random_state=42).fit(X)
        sil_score = silhouette_score(X, km.labels_)
        y_values.append(sil_score)
        print(f'Silhouette score is {sil_score} for {ncl} clusters')

        if sil_score > best_score:
            best_score = sil_score
            best_ncl = ncl

    return best_ncl, best_score, y_values


def show_clustering_results(nr_clusters, y_values):
    # Plot the silhouette score for each nr of clusters
    x_clusters = [str(nr) for nr in nr_clusters]

    plt.bar(x_clusters, y_values, color='#00cc66', edgecolor='#00994c')
    plt.xlabel("Number of clusters")
    plt.ylabel("silhouette score")
    plt.show()


def build_clustering(X, nr_clusters_to_be_tested, cities_name):

    best_nr_clusters, best_score, y_values = find_best_nr_of_clusters(
        X=X,
        nr_clusters_to_be_tested=nr_clusters_to_be_tested
    )

    # Plot clustering results
    show_clustering_results(
        nr_clusters=nr_clusters_to_be_tested,
        y_values=y_values
    )

    print(f'Best silhouette score is {best_score} for {best_nr_clusters} clusters')
    # When clustering the cities based all of their features,
    # best silhouette score is 0.13796554112515688 for 20 clusters - Not so good!

    km = KMeans(n_clusters=best_nr_clusters, random_state=42).fit(X)

    # {cluster_id: list of cities that are part of the cluster with id == cluster_id}
    cities_clusters = {}
    # {city_name: corresponding cluster_id}
    in_cluster = {}

    for i in range(len(cities_name)):
        cluster = km.labels_[i]
        current_city = cities_name[i]

        if cluster not in cities_clusters.keys():
            cities_clusters[cluster] = []

        cities_clusters[cluster].append(current_city)
        in_cluster[current_city] = cluster

    return cities_clusters, in_cluster



df, city_names, line_index_in_df = read_data_from_json(
    file_path="./files/set-3.json",
    city_features=selected_set_3
)


""" Clustering """
input_data = df.values
input_data_scaled = MinMaxScaler().fit_transform(input_data)
print(f'Input data: {input_data}')
print(f'Input data length: {len(input_data)}')
print(f'Scaled input data: {input_data_scaled}')
ncl_list = [20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120]

clusters, city_in_cluster = build_clustering(
    X=input_data_scaled,
    nr_clusters_to_be_tested=ncl_list,
    cities_name=city_names
)


print(clusters)

print('==========================================')

print(city_in_cluster)
