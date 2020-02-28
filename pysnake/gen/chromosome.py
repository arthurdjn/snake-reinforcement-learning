# -*- coding: utf-8 -*-
# Created on Mon Feb 24 11:06:01 2020
# @author: arthurd


from abc import ABC, abstractmethod
import numpy as np




class ChromosomeSkeleton:
    
    def __init__(self, genes, id = None, 
                 enable_crossover = False, 
                 size_min = None, size_max = None,
                 value_min = None, value_max = None):
        
        self.__genes = self._process_genes(genes)
        self.__id = id
        self.__size = self.size
        self.__dtype = self.genes.dtype
        self.enable_crossover = enable_crossover
        # Set a range of possible length
        size_min, size_max = self._set_size_range(size_min, size_max)
        self.size_min = size_min
        self.size_max = size_max
        self.value_min = value_min
        self.value_max = value_max
    
    # -------------------------------------------------------------------------
    # Abstract Methods
        
    # @abstractmethod
    # def mutate(self, prob_mutation):
    #     raise Exception("this method is not implemented.")
                        
                        
    # -------------------------------------------------------------------------
    # Methods
        
    def _set_size_range(self, size_min, size_max):
        current_size = self.size
        size_min = size_min if not size_min is None else current_size
        size_max = size_max if not size_max is None else current_size
        return size_min, size_max
        
    def _process_genes(self, value):
        # Pre-process the genes in a flat array
        genes = np.array(value)
        genes = genes.reshape(genes.size)
        return genes

    
    def __getitem__(self, index):
        return self.genes[index]
    
    def __str__(self):
        string =  "Chromosome: {0}\n".format(self.id if self.id is not None else "")
        string += "     genes: {0}\n".format(np.array2string(self.genes, 
                                                             precision = 3,
                                                             separator = ', ', 
                                                             threshold = 11,
                                                             edgeitems = 3))
        string += "     dtype: {0}\n".format(self.dtype)
        string += "      size: {0}".format(self.size)
        return string
 
    
    # -------------------------------------------------------------------------
    # Getters and setters
       
    @property
    def genes(self):
        return self.__genes
    
    @genes.setter
    def genes(self, value):
        genes = self._process_genes(value)
        self.__genes = genes
        self.__dtype = genes.dtype
            
    @property
    def size(self):
        return self.__genes.size
    
    @size.setter
    def size(self, value):
        raise ValueError("attribute size is not writtable. Change the genes instead.")
                                                  
    @property
    def id(self):
        return self.__id
    
    @id.setter
    def id(self, value):
        raise ValueError("attribute id is not writtable.")
                         
                         
    @property
    def dtype(self):
        return self.__dtype
    
    @dtype.setter
    def dtype(self, value):
        self.__dtype = value
        self.genes = self.genes.astype(value)
    
     
# =============================================================================


class Chromosome(ChromosomeSkeleton):
    
    def __init__(self, genes, **kwargs):
        super(Chromosome, self).__init__(genes, **kwargs)
        
    
    def mutate(self, prob_mutation, mu = 0, sigma = 1):
        genes = self.genes
        # Determine which genes will be mutated
        mutation_array = np.random.random(genes.shape) <= prob_mutation
        # Create gaussian distribution around each one
        gaussian_mutation = np.random.normal(mu, sigma, size=genes.shape)
        if self.dtype == int:
            gaussian_mutation = gaussian_mutation.round().astype(self.dtype)
        # Update
        genes[mutation_array] += gaussian_mutation[mutation_array]
        self.genes = genes
        

# =============================================================================


class ChromosomeBinary(ChromosomeSkeleton):
    
    def __init__(self, genes, **kwargs):
        super(ChromosomeBinary, self).__init__(genes, **kwargs)
        self._binary_check()
        
        
    def mutate(self, prob_mutation):
        genes = self.genes
        # Determine which genes will be mutated
        mutation_array = np.random.random(genes.shape) <= prob_mutation
        # Update
        genes[mutation_array] = 1 - genes[mutation_array]
        self.genes = genes

        
    def _binary_check(self):
        if not np.array_equal(self.genes, self.genes.astype(bool)):
            raise ValueError("the chromosome do not code binary information in its genes.")
        
# =============================================================================



        
        
        
        
        
        
        