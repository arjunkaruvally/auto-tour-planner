from cluster import get_cluster
from genetic import Cluster, PointOfInterest, GeneticAlgorithm
import pandas as pd
import json
import requests

def get_distances(geolocation):
	
	distances = []
	BASE_URL = "https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins="
	KEY = "&key=AIzaSyC5Cd047LqwkP9KVoFKjS-WtRdktusONWI"
	geolocation =  geolocation.replace(",", "%2C")
	REQUEST_URL  = BASE_URL + geolocation + "&destinations=" + geolocation + KEY
	
	print REQUEST_URL

	res = requests.get(REQUEST_URL).text
	res = json.loads(res)
	for i in res["rows"]:
		distance_vector = []
		for element in i["elements"]:
			distance_vector.append(element["duration"]["value"])
		
		distances.append(distance_vector)
	return distances

def get_clusters(city):
	all_clusters = get_cluster(city, cluster_size=8)
	clusters  = []
	for index in range(0, len(all_clusters)):
		
		cluster = all_clusters[index]["data"]
		geolocation = ""
		poi_index = 1
		points = []
		for s in cluster:
			p = PointOfInterest(s['duration']*60, s['score'])
			points.append(p)
			geolocation += str(s["geolocation"]) + "%7C"
			poi_index += 1
			if poi_index >8:
				break
		
		geolocation = geolocation[:-3]

		distancematrix = get_distances(geolocation)
		
		cluster = Cluster(points, distancematrix)
		clusters.append(cluster)

	return clusters

"""
DATA_PATH = "data_retrieval/data/points_of_interest_clean.csv"

cities = {}
city_list = [] 
data = pd.read_csv(DATA_PATH)

for i in data["base_city"]:
	if cities.has_key(i):
		cities[i]+=1
	else:
		cities[i] = 1
	

for key in cities:
	if cities[key] > 5:
		city_list.append(key)


clusters = get_clusters(city_list[0])

ga = GeneticAlgorithm(clusters[1])

ga.get_best(200)
"""