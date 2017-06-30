from mdp import PointOfInterest, Cluster



point1 = PointOfInterest(120, 2.33333)
point2 = PointOfInterest(120, 2)
point6 = PointOfInterest(120, 2)
point5 = PointOfInterest(120, 3.0)
point4 = PointOfInterest(120, 2.0)
point3 = PointOfInterest(120, 2.25)


points = [point1, point2, point3, point4, point5, point6]

distances = [ [0, 760, 643, 1344, 1344, 1956,] , [760, 0, 1050, 1109, 1109, 2041], [643, 1050, 0, 1253, 1253, 2554],
			  [1344, 1109, 1253, 0, 0, 2742], [1344, 1109, 1253, 0, 0, 2742], [1956, 2041, 2554, 2742, 2742, 0]]

cluster = Cluster(points, distances)
