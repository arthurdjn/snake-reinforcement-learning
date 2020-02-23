# -*- coding: utf-8 -*-
# Created on Sat Feb 22 17:19:36 2020
# @author: arthurd


import numpy as np


class Chromosome:
    """
    Chromosome object made of genes.
    This chromosome can mutate.
    
    Attributes
    ----------
    genes : numpy.ndarray
    
    prob_mutation : float [0, 1]
    
    
    """
    
    
    def __init__(self, genes, prob_mutation = 0.1):
        
        self.genes = genes
        self.prob_mutation = prob_mutation
        
        
        
        
        
        
        
    # -------------------------------------------------------------------------
    # Methods
        
        
        
    def gaussian_mutation(self, prob_mutation, 
                          mu = 0, sigma = 1):
            
        # Determine which genes will be mutated
        mutation_array = np.random.random(self.shape) < prob_mutation
        # Create gaussian distribution around each one
        gaussian_mutation = np.random.normal(mu, sigma, size=chromosome.shape)
        # Update
        self[mutation_array] += gaussian_mutation[mutation_array]
        
        
    
        
        
        
        