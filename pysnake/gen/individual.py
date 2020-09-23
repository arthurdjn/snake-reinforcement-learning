# -*- coding: utf-8 -*-
# Created on Fri Feb 21 11:42:58 2020
# @author: arthurd


from abc import ABC, abstractmethod


class Individual(ABC):
    """
    Abstract class that defines an individual.

    Attributes
    ----------
    id : int
        Identifiant of the individual, to keep track of the mutated agents
        in the genetic algorithm.
    chromosomes : list(pysnake.gen.chromosome.Chromosome)
        List of chromosomes defining its behavior.
    fitness : float
        Reward of the individual. How well did the individual performed ?
    """

    def __init__(self, chromosomes=None, id=None):

        self.chromosomes = self._init_chromosomes(chromosomes)
        self.id = id
        self.calculate_fitness()

    # -------------------------------------------------------------------------
    # Methods

    def _init_chromosomes(self, chromosomes):
        """
        Initialize chromosomes or encode them.

        Parameters
        ----------
        chromosomes : list(pysnake.gen.chromosome.Chromosome)
            Chromosomes to encode if None.

        Returns
        -------
        list(pysnake.gen.chromosome.Chromosome)
            List of encoded chromosomes.
        """
        if chromosomes is not None:
            return chromosomes
        else:
            return self.encode_chromosomes()

    # @DEPRECATED
    def mutate_gaussian(self, prob_mutation, mu=0, sigma=1):
        """
        Mutate the individuals genes regarding a gaussian law.

        Parameters
        ----------
        prob_mutation : float
            Probability that a gene mutate.
        mu : float, optional
            Mean of the gaussian law. The default is 0.
        sigma : float, optional
            Standard deviation of the gaussian law. The default is 1.

        Returns
        -------
        None.
        """
        print("This method is deprecated. Use .mutate() instead.")
        for chromosome in self.chromosomes:
            chromosome.mutate_gaussian(prob_mutation, mu=mu, sigma=sigma)

    def mutate(self, prob_mutation):
        """
        Mutate chromosomes.

        Parameters
        ----------
        prob_mutation : float
            Probability that a gene in a chromosome mutate.

        Returns
        -------
        None.
        """
        for chromosome in self.chromosomes:
            chromosome.mutate(prob_mutation)

    # -------------------------------------------------------------------------
    # Abstract methods

    @abstractmethod
    def encode_chromosomes(self):
        raise Exception('encode_chromosome function must be defined')

    @abstractmethod
    def calculate_fitness(self):
        raise Exception('calculate_fitness function must be defined')

    # -------------------------------------------------------------------------
    # Getters and setters

    @property
    def size(self):
        return len(self.chromosomes)

    @size.setter
    def size(self, value):
        raise AttributeError("attribute 'size' is not writtable.")

    # -------------------------------------------------------------------------
    # Access

    def __getitem__(self, index):
        return self.chromosomes[index]

    def __str__(self):
        string = "Individual: {0}\n".format(self.id if self.id is not None else "")
        string += "fitness   : {0}\n".format(self.fitness)
        # string += "chromosomes: {0}\n".format(len(self.chromosomes))
        string += str(self.chromosomes[0]) + "\n"
        if len(self.chromosomes) > 2:
            string += "      ...\n"
        string += str(self.chromosomes[-1])

        return string
