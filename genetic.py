from random import shuffle, sample, randint, random
class PointOfInterest:

	def __init__(self, visit_time, score):
		self.visit_time = visit_time
		self.score = score

	def get_score(self):
		return self.score

	def get_visit_time(self):
		return self.visit_time


class Cluster:
	"""Class  to model each cluster"""
	def __init__(self, pois, distances):
		self.points = pois
		self.distances = distances

class GeneticAlgorithm:

	def __init__ (self, cluster, end_time=600, mutatation_rate=0.01, tournament_size=12):
		self.cluster = cluster
		self.end_time = 600
		self.size = len(cluster.points)
		self.pop_length = 16
		self.tournament_size = 12
		self.mutatation_rate = 0.01


	def fitness(self, chromosome):
		current_time = 0
		reward = 0
		for gene in range(0, self.size):
			allele = chromosome[gene]
			current_time += self.cluster.points[allele].visit_time
			if current_time <= self.end_time:
				reward += self.cluster.points[allele].score
			else:
				reward -= self.cluster.points[allele].score
			if gene < self.size - 1:
				current_time += self.cluster.distances[allele][chromosome[gene+1]]

		return reward

	def random_init(self):
		population = []
		for i in range(0, self.pop_length):
			p = range(0, self.size)
			shuffle(p)
			population.append(p)
		return population

	def tournament_selection(self, population, k):
		parents = sample(range(1,self.pop_length), k)
		best = parents[0]
		for p in parents:
			if self.fitness(population[p]) > self.fitness(population[best]):
				best = p
		return population[best]

	def crossover(self, parent1, parent2):

		starpos = 0
		endpos = 0
		while  starpos >= endpos:
			starpos = randint(0 , self.size-1)
			endpos = randint(0, self.size-1)

		child = [-1] * self.size

		for i in range(0, self.size):
			if i > starpos and i < endpos:
				child[i] = parent1[i]

		for i in range(0 , self.size):
			if parent2[i] not in child:
				for j in range(0, self.size):
					if child[j] == -1:
						child[j] = parent2[i]
						break

		return child

	def mutate(self, point):

		for i in range(0, self.size):
			if random() < self.mutatation_rate:
				j = randint(0 , self.size-1)
				tp = point[i]
				point[i] = point[j]
				point[j] = tp
		return point



	def evolve(self, population):
		next_gen = []
		k = self.tournament_size
		for i in range(0, self.pop_length):
			parent1 = self.tournament_selection(population, k)
			parent2 = self.tournament_selection(population, k)

			child = self.crossover(parent1, parent2)
			next_gen.append(child)
		for i in range (0, len(next_gen)):
			next_gen[i] = self.mutate(next_gen[i])
		return next_gen


	def get_best(self, gen_size):
		population = self.random_init()
		for i in range(0, gen_size):
			population = self.evolve(population)
			print "Generation " + str(i)
			best = population[0]
			for j in range(0, self.pop_length):
				if self.fitness(population[j]) > self.fitness(best):
					best = population[j]
			print best, self.fitness(best)

