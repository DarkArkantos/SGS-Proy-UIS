from typing import List
from models.activity import Activity


class Chromosome(object):
    """Class that reperesent a Chromosome"""
    genes: List[Activity]
    fitness: float

    def __init__(self, genes: List[Activity], fitness: float=0):
        self.fitness = fitness
        self.genes = genes

    def is_a_valid_chromosome(self):
        res: bool = True
        for act in self.genes:
            for pre in act.pre:
                if(not pre< act.index):
                    res&=False
        return res

