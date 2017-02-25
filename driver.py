import cluster
import pandas as pd
###### Clustering test

out_cluster=cluster.get_cluster()

print out_cluster[0]['data']

df = pd.DataFrame(out_cluster[0]['data'])
print df 
# print cluster.parse_duration(' <1 hour ')
# print cluster.get_distance({'x': 0, 'y': 0}, {'x': 3, 'y': 4})