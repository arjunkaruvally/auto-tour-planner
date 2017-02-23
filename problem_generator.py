from cluster import get_cluster

city_list = ["Kochi (Cochin)"] #TODO, add other cities; make it dynamic

#Add better clustering output

def create_cluster_file():
	f = open("cluster.txt", "w")
	for city in city_list:
		r = get_cluster(city)
		f.write(str(r))
		f.write("\n")

	f.close()

problem_text_start = """
(define (problem problem)
    (:domain
        travel-domain    
    )
    (:objects
        waypoint1 waypoint2 waypoint3
        user1
    )
    
    (:init
        (= (total-score) 0)
        (= (current-time) 10)
        (= (end-time) 20)
        (user user1)
"""

problem_text_end = """
    	)
    )
    (:metric 
        maximize (total-score)         
    )
)
"""

def create_problem_file(file_path="sample.csv"):
	file = open(file_path)

	pois = []

	text = file.readlines();
	file.close()

	poi_index = 1
	problem_text_mid = ""
	for i in text:
		s = i.strip().split(",") #s[0]s houl
		problem_text_mid += "\t\t(waypoint waypoint" + str(poi_index) + ")\n"
		problem_text_mid += "\t\t(= (score waypoint" + str(poi_index) + ") " + s[1] +")\n"
		problem_text_mid += "\t\t(= (duration waypoint" + str(poi_index) + ") " + s[2] +")\n"
		poi_index += 1


	#TODO WRITE WAYS TO COMPUTE DISTANCE BETWEEN POIs

	############

	for i in range(1,poi_index):
		problem_text_mid += "\t\t(not ( visited user1 waypoint" + str(i) + ") )\n"

	problem_text_mid += "\t\t(user-at user1 waypoint1) ) \n\n\t(:goal\n\t\t(and\n"

	for i in range(1,poi_index):
		problem_text_mid += "\t\t\t(visited user1 waypoint" + str(i) + ")\n"

	return problem_text_start + problem_text_mid + problem_text_end

print create_problem_file()