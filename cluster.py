import pandas as pd
import random
import math
import re

def GCD(a, b):
    if b == 0:
        return a
    else:
        return GCD(b, a % b)

def get_distance(p1,p2):
	dis = math.pow(p1['x']-p2['x'],2) + math.pow(p1['y']-p2['y'],2)
	return math.sqrt(dis)	

def represents_int(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

def parse_duration(x):

	if pd.isnull(x):
		return 2

	pattern_less = re.compile(r'.*<([0-9]+) .*')
	pattern_range = re.compile(r'.*([0-9]+)-([0-9]+) .*')
	pattern_more = re.compile(r'.*More than ([0-9]+) .*')

	try:
		result = re.search(pattern_less, x)
		if result!=None:
			return int(result.group(1))

		result = re.search(pattern_range, x)
		if result!=None:
			return (int(result.group(1))+int(result.group(2)))/2

		result = re.search(pattern_more, x)
		if result!=None:
			return int(result.group(1))+2
	except ValueError:
		pass

	return 2

def get_cluster(city='Kochi (Cochin)', filepath="data_retrieval/data/points_of_interest_clean.csv", cluster_size=10, number_of_clusters=10, restrict_cluster=True, iter_limit=10):
	
	#Data Retrival and preprocessing
	df = pd.read_csv(filepath)
	df = df[df['base_city']==city]
	
	score_list = []

	#Score calculation
	factors = [3,2,1,-1,-2]
	for index, row in df.iterrows():
		rating = row['rating'].split('&')
		score = 0
		total = 0
		for x in range(0, len(rating)):
			if represents_int(rating[x]):
				score+=factors[x]*int(rating[x])
				total+=int(rating[x])

		if total!=0:
			score=1.0*score/total
		
		score_list.append(score)
	df.loc[:,'score'] = pd.Series(score_list, index=df.index)

	#Duration parsing
	df['duration'] = df['duration'].apply(parse_duration)
	# print df

	if restrict_cluster:
		number_of_clusters = int(math.ceil(df.shape[0]/cluster_size))

	df.index = pd.Series(range(0,df.shape[0]))

	coords_str = df['geolocation']
	# indexes = coords_str.index
	# print indexes
	coords = {'x': [], 'y': [], 'i': []}
	for x in coords_str:
		location = x.split(',')
		location[0] = int(float(location[0])*1000000)
		location[1] = int(float(location[1])*1000000)
		coords['x'].append(location[0])
		coords['y'].append(location[1])

	gcd={'x': 1, 'y': 1}
	# gcd['x'] = reduce(GCD, coords['x'])
	# gcd['y'] = reduce(GCD, coords['y'])
	maxim = {'x': 0, 'y':0}
	maxim['x'] = max(coords['x'])
	maxim['y'] = max(coords['y'])

	sample = {'x': [], 'y': []}
	sample['x'] = range(0,maxim['x'],gcd['x'])
	sample['y'] = range(0,maxim['y'],gcd['y'])

	random_clusters = []
	for x in range(0, number_of_clusters):
		random_clusters.append({ 'x': random.choice(sample['x']), 'y': random.choice(sample['y']), 'size': 0, 'coords': [], 'tot_x': 0, 'tot_y': 0 })

	ctr = 0

	#print len(coords['x'])," locations"
	#print number_of_clusters," number of clusters"
	
	while ctr<iter_limit:
		distances = []

		for x in range(0, len(random_clusters)):
			random_clusters[x]['coords'] = []
			random_clusters[x]['tot_x'] = 0
			random_clusters[x]['tot_y'] = 0
			random_clusters[x]['size'] = 0

		for x in range(0,len(coords['x'])):
			for y in range(0,len(random_clusters)):
				obj = {'coord_index': 0, 'cluster_index': 0, 'distance': 0}
				obj['coord_index'] = x
				obj['cluster_index'] = y
				obj['distance'] = get_distance({'x': coords['x'][x], 'y': coords['y'][x]}, random_clusters[y])
				distances.append(obj)

		distances = sorted(distances, key=lambda y: y['distance'])
		assigned_index = []

		for x in distances:
			temp_size = random_clusters[x['cluster_index']]['size']
			# if x['cluster_index']!=8:
			# 	print x
			if temp_size <= cluster_size and (x['coord_index'] not in assigned_index):
				assigned_index.append(x['coord_index'])
				random_clusters[x['cluster_index']]['coords'].append(x['coord_index'])
				random_clusters[x['cluster_index']]['tot_x'] += coords['x'][x['coord_index']]
				random_clusters[x['cluster_index']]['tot_y'] += coords['y'][x['coord_index']]
				random_clusters[x['cluster_index']]['size'] = len(random_clusters[x['cluster_index']]['coords'])

		for x in range(0,len(random_clusters)):
			if random_clusters[x]['size'] > 0:
				random_clusters[x]['x'] = random_clusters[x]['tot_x']/random_clusters[x]['size']
				random_clusters[x]['y'] = random_clusters[x]['tot_y']/random_clusters[x]['size']

		ctr += 1

	return_value = []

	# print df.index
	# print df.loc[43,:]

	for x in random_clusters:
		# print x
		temp_cluster = {'stats': x, 'data': []}
		for y in x['coords']:
			# print y
			temp = { 
						'name': df.loc[y,'heading'],
						'score': df.loc[y,'score'],
						'duration': df.loc[y,'duration'],
						'geolocation': df.loc[y,'geolocation']
					}
			temp_cluster['data'].append(temp)
		return_value.append(temp_cluster)

	return return_value