# -*- coding: utf-8 -*-
# Created on Fri Feb 21 11:01:32 2020
# @author: arthurd


"""
Population set-up for genetic algorithm.
Original code from https://github.com/Chrispresso/SnakeAI.
"""

import numpy as np  

from pysnake.gen.chromosome import Chromosome, ChromosomeBinary


class Population:
    """
    Abstract class that defines a population.
    A population contains a set of individuals.
    
    Attributes
    ----------
    id : int
        Identifiant of the population.
    size : int
        Number of individuals in the population.
    individuals : list(pysnake.gen.individual.Individual)
        List of individual.
    fitness : list(float)
        Fitness list of all individuals.
    mean_fitness : float
        Fitness mean of all individuals.
    std_fitness : float
        Fitness standard deviation of all individuals.
    fittest : pysnake.gen.individual.Individual
        Best individual, with the highest fitnest.
    """
    
    def __init__(self, individuals, id = None):        
        # @NOTE :
        # individuals must be set first
        self.individuals = individuals
        self.__id = id
        self.__size = self.size
        self.__fitness = self.fitness
        self.__mean_fitness = self.mean_fitness
        self.__std_fitness = self.std_fitness
        self.__fittest = self.fittest
        

    # -------------------------------------------------------------------------
    # Methods
        
    def calculate_fitness(self):
        """
        Calculate the fitness for all individuals.

        Returns
        -------
        None.
        """
        for individual in self.individuals:
            individual.calculate_fitness()
            
            
    def select_elitism(self, num_individuals):
        """
        Select the top X best individuals.

        Parameters
        ----------
        num_individuals : int
            Top X individuals to select.

        Returns
        -------
        list(pysnake.gen.individual.Individual)
            List of the top X individuals.
        """
        individuals = sorted(self.individuals, key = lambda individual: individual.fitness, reverse=True)
        return individuals[:num_individuals]
    
    
    def select_roulette_wheel(self, num_individuals):
        """
        Select individuals in a roulette wheel game.

        Parameters
        ----------
        num_individuals : int
            Number of individuals to select.

        Returns
        -------
        list(pysnake.gen.individual.Individual)
            List of the selected individuals.
        """
        selection = []
        wheel = np.sum(individual.fitness for individual in self.individuals)
        for _ in range(num_individuals):
            pick = np.random.uniform(0, wheel)
            current = 0
            for individual in self.individuals:
                current += individual.fitness
                if current > pick:
                    selection.append(individual)
                    break
    
        return selection
    
        
    def select_tournament(self, num_individuals, tournament_size):
        """
        Select the best individuals in a sub list of individuals X times.

        Parameters
        ----------
        num_individuals : int
            Number of individuals to select.
        tournament_size : int
            Size of the competitive tournament.

        Returns
        -------
       list(pysnake.gen.individual.Individual)
            List of the selected individuals.
        """
        selection = []
        for _ in range(num_individuals):
            tournament = np.random.choice(self.individuals, tournament_size)
            best_from_tournament = max(tournament, key = lambda individual: individual.fitness)
            selection.append(best_from_tournament)
            
        return selection
    
    
    def crossover_simulated_binary(self, parent1, parent2, eta=100):
        
        assert parent1.size == parent2.size, ("The parents must have the same number of chromosomes.")
        
        chromosomes1 = []
        chromosomes2 = []
        
        # Loop over all chromosomes
        for i in range(parent1.size):
            # Get the chromosome from both parents
            chromosome1 = parent1.chromosomes[i]
            chromosome2 = parent2.chromosomes[i]
            
            # If these chromosomes can crossover
            if chromosome1.enable_crossover and chromosome2.enable_crossover:
                # Get the genes that will change
                genes1 = chromosome1.genes
                genes2 = chromosome2.genes
                
                rand = np.random.random(chromosome1.size)
                gamma = np.empty(chromosome1.size)
                # First case of equation 9.11
                gamma[rand <= 0.5] = (2 * rand[rand <= 0.5]) ** (1.0 / (eta + 1))  
                # Second case
                gamma[rand > 0.5] = (1.0 / (2.0 * (1.0 - rand[rand > 0.5]))) ** (1.0 / (eta + 1))  
        
                # Calculate Child 1 chromosome (Eq. 9.9)
                child_genes1 = 0.5 * ((1 + gamma)*genes1 + (1 - gamma)*genes2)
                # Calculate Child 2 chromosome (Eq. 9.10)
                child_genes2 = 0.5 * ((1 - gamma)*genes1 + (1 + gamma)*genes2)
            
                # Create the new chromosome with the updated genes
                chromosome1 = Chromosome(child_genes1, id=chromosome1.id, enable_crossover=True)
                chromosome2 = Chromosome(child_genes2, id=chromosome2.id, enable_crossover=True)
            
            # Add the chromosome to a list
            chromosomes1.append(chromosome1)
            chromosomes2.append(chromosome2)
                
        return chromosomes1, chromosomes2
    
    
    def crossover_single_point(self, parent1, parent2):
        
        assert parent1.size == parent2.size, ("The parents must have the same number of chromosomes.")
        
        chromosomes1 = []
        chromosomes2 = []
        
        for i in range(parent1.size):
            # Get the chromosome from both parents
            chromosome1 = parent1.chromosomes[i]
            chromosome2 = parent2.chromosomes[i]
            
            # If these chromosomes can crossover
            if chromosome1.enable_crossover and chromosome2.enable_crossover:
                # Get the genes that will change
                genes1 = chromosome1.genes
                genes2 = chromosome2.genes
            
                single_point = np.random.choice(np.arange(parent1.size))
                child_genes1 = np.concatenate((genes1[:single_point], genes2[single_point:]))
                child_genes2 = np.concatenate((genes2[:single_point], genes1[single_point:]))
    
                # Create the new chromosome with the updated genes
                if isinstance(chromosome1, ChromosomeBinary):
                    assert isinstance(chromosome1, ChromosomeBinary) == isinstance(chromosome2, ChromosomeBinary), (
                        "The matching chromosome from both parents should be the same type (here binary).")
                    chromosome1 = ChromosomeBinary(child_genes1, id=chromosome1.id, enable_crossover=True)
                    chromosome2 = ChromosomeBinary(child_genes2, id=chromosome2.id, enable_crossover=True)
                else:
                    chromosome1 = Chromosome(child_genes1, id=chromosome1.id, enable_crossover=True)
                    chromosome2 = Chromosome(child_genes2, id=chromosome2.id, enable_crossover=True)
    
            # Add the chromosome to a list
            chromosomes1.append(chromosome1)
            chromosomes2.append(chromosome2)
                
        return chromosomes1, chromosomes2


    # -------------------------------------------------------------------------
    # Getters and setters

    @property
    def size(self):
        return len(self.individuals)

    @size.setter
    def size(self, value):
        raise AttributeError("attribute 'size' of 'Population' objects is not writable.",
                             "Change attribute 'individuals' instead.")

    @property
    def fitness(self):
        return np.array([individual.fitness for individual in self.individuals])
    
    @fitness.setter
    def fitness(self, value):
        raise AttributeError("attribute 'fitness' of 'Population' objects is not writable.",
                             "Change attribute 'individuals' instead.")

    @property
    def mean_fitness(self):
        return np.mean(self.fitness)

    @mean_fitness.setter
    def mean_fitness(self, value):
        raise AttributeError("attribute 'mean_fitness' of 'Population' objects is not writable.",
                             "Change attribute 'individuals' instead.")

    @property
    def std_fitness(self):
        return np.std(self.fitness)
    
    @std_fitness.setter
    def std_fitness(self, value):
        raise AttributeError("attribute 'std_fitness' of 'Population' objects is not writable.",
                             "Change attribute 'individuals' instead.") 

    @property
    def fittest(self):
        return max(self.individuals, key = lambda individual: individual.fitness)

    @fittest.setter
    def fittest(self, value):
        raise AttributeError("attribute 'fittest' of 'Population' objects is not writable.",
                             "Change attribute 'individuals' instead.")

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, value):
        raise AttributeError("attribute 'id' of 'Population' objects is not writable.")


    # -------------------------------------------------------------------------
    # Access

    def __getitem__(self, index):
        return self.individuals[index]
    
    def __str__(self):
        string =  "Population: {0}\n".format(self.id if self.id is not None else "")
        string += "      size: {0}\n".format(self.size)
        string += "  mean fit: {0}\n".format(self.mean_fitness)
        string += "   std fit: {0}\n".format(self.std_fitness)
        string += "   fittest: {0}".format(self.fittest.fitness)
        
        return string
    
    

