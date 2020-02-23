# -*- coding: utf-8 -*-
# Created on Sat Feb 22 16:16:07 2020
# @author: arthurd


import numpy as np


class Selector:
    """
    Select best individuals from a population.
    
    Attributes
    ----------
    population : Population
        Population where individuals will be extracted.
    
    """
    
    def __init__(self, population):
        
        self.population = population
        
    
    
    
    


def elitism_selection(population, num_individuals):
    individuals = sorted(population.individuals, key = lambda individual: individual.fitness, reverse=True)
    return individuals[:num_individuals]

def roulette_wheel_selection(population, num_individuals):
    selection = []
    wheel = np.sum(individual.fitness for individual in population.individuals)
    for _ in range(num_individuals):
        pick = np.random.uniform(0, wheel)
        current = 0
        for individual in population.individuals:
            current += individual.fitness
            if current > pick:
                selection.append(individual)
                break

    return selection

def tournament_selection(population, num_individuals, tournament_size):
    selection = []
    for _ in range(num_individuals):
        tournament = np.random.choice(population.individuals, tournament_size)
        best_from_tournament = max(tournament, key = lambda individual: individual.fitness)
        selection.append(best_from_tournament)

    return selection