import numpy as np 
import math
import random

class GeneticAlgorithm(object): 
	"""
		Implement a simple generationl genetic algorithm as described in the instructions
	"""

	def __init__(	self, chromosomeShape,
					errorFunction,
					elitism = 1,
					populationSize = 25, 
					mutationProbability  = .1, 
					mutationScale = .5,
					numIterations = 10000, 
					errorTreshold = 1e-6
					): 

		np.random.seed(11071998)
		random.seed(11071998)


		self.populationSize = populationSize # size of the population of units
		self.p = mutationProbability # probability of mutation
		self.numIter = numIterations # maximum number of iterations
		self.e = errorTreshold # threshold of error while iterating
		self.f = errorFunction # the error function (reversely proportionl to fitness)
		self.keep = elitism  # number of units to keep for elitism
		self.k = mutationScale # scale of the gaussian noise

		self.i = 0 # iteration counter

		# initialize the population randomly from a gaussian distribution
		# with noise 0.1 and then sort the values and store them internally

		self.population = []
		for _ in range(populationSize):
			chromosome = np.random.randn(chromosomeShape) * 0.1

			fitness = self.calculateFitness(chromosome)
			self.population.append((chromosome, fitness))

		# sort descending according to fitness (larger is better)
		self.population = sorted(self.population, key=lambda t: -t[1])

	
	def step(self):	
		"""
			Run one iteration of the genetic algorithm. In a single iteration,
			you should create a whole new population by first keeping the best
			units as defined by elitism, then iteratively select parents from
			the current population, apply crossover and then mutation.

			The step function should return, as a tuple: 
				
			* boolean value indicating should the iteration stop (True if 
				the learning process is finished, False othwerise)
			* an integer representing the current iteration of the 
				algorithm
			* the weights of the best unit in the current iteration
		
		"""
		
		self.i += 1 

		newGeneration = []
		newGeneration.extend(self.bestN(self.keep))

		for i in range(self.populationSize - self.keep):
			parent1, parent2 = self.selectParents()
			child = self.crossover(parent1[0], parent2[0])
			child = self.mutate(child)
			fitness = self.calculateFitness(np.array(child))
			newGeneration.append((child, fitness))

		self.population = newGeneration
		self.population = sorted(self.population, key=lambda t: -t[1])
		# dodati i za error threshold
		bestOfPopulation = self.best()
		return self.i == self.numIter, self.i, np.array(bestOfPopulation[0])


	def calculateFitness(self, chromosome):
		"""
			Implement a fitness metric as a function of the error of
			a unit. Remember - fitness is larger as the unit is better!
		"""
		chromosomeError = self.f(chromosome)

		return 1.0 / float(chromosomeError)

	def bestN(self, n):		
		"""
			Return the best n units from the population
		"""
		return self.population[:n]

	def best(self):
		"""
			Return the best unit from the population
		"""
		return self.population[0]

	def selectParents(self):
		"""
			Select two parents from the population with probability of 
			selection proportional to the fitness of the units in the
			population		
		"""
		suma = 0
		for chromAndFitness in self.population:
			suma += chromAndFitness[1]

		lista = []
		for i in range(2):
			pointer = random.uniform(0, suma)

			domain = 0
			for chromAndFitness in self.population:
				domain += chromAndFitness[1]
				if pointer <= domain:
					lista.append(chromAndFitness)

		return lista[0], lista[1]


	def crossover(self, p1, p2): 
		"""
			Given two parent units p1 and p2, do a simple crossover by 
			averaging their values in order to create a new child unit
		"""
		i = 0
		child = []
		for weight1 in p1:
			weight2 = p2[i]
			i += 1
			child.append((weight1+weight2)/2.0)
		return child

	def mutate(self, chromosome):
		"""
			Given a unit, mutate its values by applying gaussian noise
			according to the parameter k
		"""
		for i in range(len(chromosome)):
			if(random.uniform(0,1) <= self.p):
				chromosome[i] += random.gauss(0, self.k)
		return chromosome
	
