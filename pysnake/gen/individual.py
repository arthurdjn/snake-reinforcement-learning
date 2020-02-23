# -*- coding: utf-8 -*-
# Created on Fri Feb 21 11:42:58 2020
# @author: arthurd


from abc import ABC, abstractmethod


class Individual(ABC):
    """
    Abstract class that defines an individual.
    
    Attributes
    ----------
    chromosom : numpy.ndarray
    fitness : float
    id : int
    """
    
    
    def __init__(self, id):
        
        self.__fitness = None
        self.__chromosome = None
        self.__id = id
        
        
    # -------------------------------------------------------------------------
    # Abstract methods
    
    @abstractmethod
    def encode_chromosome(self):
        raise Exception('encode_chromosome function must be defined')
        
    @abstractmethod
    def decode_chromosome(self):
        raise Exception('decode_chromosome function must be defined')
    
    @abstractmethod
    def calculate_fitness(self):
        raise Exception('calculate_fitness function must be defined')
    
    
    # -------------------------------------------------------------------------
    # Getters and setters

    @property
    def fitness(self):
        return self.__fitness

    @fitness.setter
    def fitness(self, value):
        raise AttributeError("attribute 'fitness' of 'Individuals' objects is not writable. Use method 'calculate_fitness' instead.")

    @property
    def chromosome(self):
        return self.__chromosome

    @chromosome.setter
    def chromosome(self, value):
        raise AttributeError("attribute 'chromosome' of 'Individuals' objects is not writable.")
        
    @property
    def id(self):
        return self.__id
    
    @id.setter
    def id(self, value):
        raise AttributeError("attribute 'id' of 'Individuals' objects is not writable.")
        
        