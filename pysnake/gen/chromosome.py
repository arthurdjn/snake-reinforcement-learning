# -*- coding: utf-8 -*-
# Created on Mon Feb 24 11:06:01 2020
# @author: arthurd


from abc import ABC, abstractmethod
import numpy as np



class ChromosomeSkeleton(ABC):
    """
    Structure of a chromosome. Abstract class.
    
    Attributes
    ----------
    id: int
        Identifiant of a chromosome, used to track the evolution of genes.
    genes: list
        List of elements (int, float, etc.).
    size: int
        Length of genes.
    dtype: type
        Type of a gene. Note that all genes in a chromosome have the same type.
    enable_crossover: bool
        Enable crossover for this chromosome.
    enable_mutation: bool
        Enable mutation for this chromosome.
    size_min: int
        Minimum size genes can have.
    size_max: int
        Maximal size genes can have
    value_min: float or int
        Minimal value a gene can have.
    value_max: float or int
        Maximal value a gene can have.
    """
    
    def __init__(self, genes, id  = None, 
                 enable_crossover = False, 
                 enable_mutation  = True,
                 size_min  = None, size_max  = None,
                 value_min = None, value_max = None):
        
        self.__id = id
        self.__genes = self._process_genes(genes)
        self.__size = self.size
        self.__dtype = self.genes.dtype
        self.enable_crossover = enable_crossover
        self.enable_mutation = enable_mutation
        # Set a range of possible length / values
        self.size_min = size_min
        self.size_max = size_max
        self.value_min = value_min
        self.value_max = value_max
    
    # -------------------------------------------------------------------------
    # Abstract Methods
        
    @abstractmethod
    def mutate(self):
        """
        Define the genes mutation style.

        Returns
        -------
        None.
        """
        raise Exception("this method is not implemented.")
                        
                        
    # -------------------------------------------------------------------------
    # Methods
        
    def _process_genes(self, value):
        """
        Flatten genes to a 1D vector.

        Parameters
        ----------
        value : numpy.ndarray
            Genes to preprocess.

        Returns
        -------
        genes : numpy.ndarray
            Reshaped genes.
        """
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
    """
    Chromosome made of float / int genes.
    """
    
    def __init__(self, genes, **kwargs):
        super().__init__(genes, **kwargs)
        
    
    def mutate(self, prob_mutation, mu = 0, sigma = 1):
        # Determine which genes will be mutated
        mutation_array = np.random.random(self.genes.shape) <= prob_mutation
        # Create gaussian distribution around each one
        gaussian_mutation = np.random.normal(mu, sigma, size=self.genes.shape)
        if self.dtype == int:
            gaussian_mutation = gaussian_mutation.round().astype(self.dtype)
        # Update
        self.genes[mutation_array] += gaussian_mutation[mutation_array]
        

# =============================================================================


class ChromosomeBinary(ChromosomeSkeleton):
    """
    Binary chromosome made of int (1 or 0).
    """
    
    def __init__(self, genes, **kwargs):
        self._binary_check()
        super(ChromosomeBinary, self).__init__(genes, **kwargs)

        
    def mutate(self, prob_mutation):
        # Determine which genes will be mutated
        mutation_array = np.random.random(self.genes.shape) <= prob_mutation
        # Update
        self.genes[mutation_array] = 1 - self.genes[mutation_array]

        
    def _binary_check(self):
        """
        Make sure the genes are binary.

        Returns
        -------
        None.
        """
        if not np.array_equal(self.genes, self.genes.astype(bool)):
            raise ValueError("the chromosome do not code binary information in its genes.")
        
      
        
        
        
        
        
        