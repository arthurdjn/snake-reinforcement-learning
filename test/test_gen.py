# -*- coding: utf-8 -*-
# Created on Sat Feb 22 14:45:37 2020
# @author: arthurd


import matplotlib.pyplot as plt
plt.style.use("seaborn-darkgrid")

import random as rd
import numpy as np
# Fix the seed for debugging
np.random.seed(42)
rd.seed(42)

# Import pysnake modules
from pysnake.gen import Individual, Population




class MyIndividual(Individual):
    
    def __init__(self, chromosome = None):

        self._Individual__chromosome = chromosome if chromosome is not None else self.encode_chromosome()
        self.calculate_fitness()        
        self._Individual__id = None
           
    def encode_chromosome(self):
        x = np.random.uniform(-5, 5)
        y = np.random.uniform(-5, 5)
        return np.array([x, y])
        
    def decode_chromosome(self):
        raise Exception('decode_chromosome function must be defined')
    
    def calculate_fitness(self):
        # Function to optimize
        dumb_function = lambda x,y: (2*x**2 - 1.05*x**4 + ((x**6)/6) + x*y + y**2)
        fitness = 1. / dumb_function(*self.chromosome)
        # Set the fitness
        self._Individual__fitness = fitness
        
    def gaussian_mutation(self, prob_mutation, 
                          mu = 0, sigma = 1):
            
        chromosome = self.chromosome
        # Determine which genes will be mutated
        mutation_array = np.random.random(chromosome.shape) < prob_mutation
        # Create gaussian distribution around each one
        gaussian_mutation = np.random.normal(mu, sigma, size=chromosome.shape)
        # Update
        chromosome[mutation_array] += gaussian_mutation[mutation_array]




def test_individual():
    # 1/ Test the default individual
    ind = MyIndividual()
    print("\t1. Default ind")
    print("\t1.1 Chromosome :", ind.chromosome)
    print("\t1.2 Fitness :", ind.fitness)
    
    ind = MyIndividual(chromosome = np.array([2., 2., 2., 2.]))
    print("\t2. New ind")
    print("\t2.1 Chromosome :", ind.chromosome)
    print("\t2.2 Fitness :", ind.fitness)
    
    # 3/ Test mutation
    chromosome = ind.chromosome
    print("\t3.1. Original :", chromosome)
    ind.gaussian_mutation(0.1)
    print("\t3.2. Mutation :", ind.chromosome)
    
    

def test_population():
    # Generate a population
    inds = [MyIndividual() for k in range(15)]
    pop = Population(inds) 
    print("\t1. Fitness", pop.fitness)
    print("\t2. Fittest", pop.fittest)
    print("\t2.1. Fittest fitness", pop.fittest.fitness)
    print("\t3. Mean", pop.mean_fitness)
    print("\t4. Std", pop.std_fitness)
    
    # Testing selectors
    print("\t5. Testing the selectors.")
    roulette = pop.select_roulette_wheel(5)
    elitism = pop.select_elitism(5)
    print("\t5.1. Roulette wheel :", [ind.fitness for ind in roulette])
    print("\t5.2. Elitism :", [ind.fitness for ind in elitism])

    # Crossover
    print("\t6. Crossover")
    parent1 = inds[0]
    parent2 = inds[1]
    eta = 100
    sbx = pop.simulated_binary_crossover(parent1, parent2, eta)
    print("\t6.1 Origianl chromosomes :", parent1.chromosome, parent2.chromosome)
    print("\t6.2 SBX :", sbx)
    print("\t6.3 Difference :", sbx[0] == parent2.chromosome)
    

def test_genalgo():
    NUM_INDIVIDUALS = 60
    NUM_GENERATIONS = 300
    fitness = []  # For tracking average fitness over generation
    
    # Create and initialize the population
    individuals = [MyIndividual() for _ in range(NUM_INDIVIDUALS)]
    pop = Population(individuals)

    for generation in range(NUM_GENERATIONS):
        print("\rgeneration : {}/{}".format(generation+1, NUM_GENERATIONS), end="")
        next_individuals = []  # For setting next population

        # Get best individuals from current pop
        best_from_pop = pop.select_elitism(2)
        next_individuals.extend(best_from_pop)
        
        while len(next_individuals) < NUM_INDIVIDUALS:
            p1, p2 = pop.select_roulette_wheel(2)
            # p1, p2 = tournament_selection(pop, 2, 4)
            mutation_rate = 0.05 / (generation + 1)**0.5
            # mutation_rate = 0.05

            # Create offpsring through crossover
            eta = 1
            chromosome1, chromosome2 = pop.simulated_binary_crossover(p1, p2, eta)
            child1 = MyIndividual(chromosome1)
            child2 = MyIndividual(chromosome2)

            # Mutate offspring
            child1.gaussian_mutation(mutation_rate)
            child2.gaussian_mutation(mutation_rate)

            # Add to next population
            next_individuals.extend([child1, child2])
        
        # Track average fitness
        fitness.append(pop.mean_fitness)

        # Set the next generation
        pop = Population(next_individuals)
        
    plt.yscale('symlog')
    plt.xlabel('Generation')
    plt.ylabel('Fitness')
    plt.plot(range(len(fitness)), fitness)
    plt.tight_layout()
    plt.show()



if __name__ == "__main__":
    
    # # Test individual
    # print("Testing Individual...")
    # test_individual()
    # print("Individual tested.\n")


    # # Test population
    # print("Testing Population...")
    # test_population()
    # print("Population tested.")

    test_genalgo()
    
    
    
    
