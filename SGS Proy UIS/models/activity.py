from typing import List, Optional
from models.resources import Resources
from dataclasses import dataclass, field
import marshmallow_dataclass
import marshmallow.validate
import numpy.random as rand
from scipy.stats import beta

@dataclass
class Activity:
    # indice
    index:int
    # inicio tiempo de la actividad
    start:Optional[float]
    # prioridad
    duration:Optional[int]
    # precedencia
    precedence:List[int]
    # recursos [0,0,0]
    resources:List[int]
    # activa
    active:Optional[bool]
    # completada
    completed:Optional[bool]
    # elegible
    eleg:Optional[bool]
    # tiempo de finalización
    end:Optional[int]


    def __init__(self, index:int, start:int, duration:int, precedence:List[int], resources:List[int], active:bool=False, completed:bool=False, eleg:bool=False, end:int=0):
        self.index = index
        self.start=start
        self.duration=duration
        self.precedence=precedence
        self.resources=resources
        self.active=active
        self.completed = completed
        self.eleg = eleg
        self.end = end

    @classmethod
    def empty_activity(self):
        return Activity(
             index = 0,
             start= 0,
             duration=0,
             precedence=[0],
             resources=Resources([0,0,0]),
             active=False,
             completed = False,
             eleg = False,
             end = 0
            )
    
    def __concat_elements(self):
        res=''
        for index in range(0, len(self.precedence)):
            res+=str(self.precedence[index])+', '
        return res
    def complete_activity(self):
        self.reset_activity()
        self.completed=True

    def set_eleg(self):
        self.reset_activity()
        self.eleg=True

    def reset_activity(self):
        self.completed=False
        self.active=False
        self.eleg=False


    def print_activity(self)-> str:
        row = "|  {:^3d} |  {:^5.2f}  |  {:^6.3f}  |  {:>14s}  |  {:^15s}  |  {:^5s}  |  {:^5s}  |  {:^5s}  |  {:^5.2f}  |\n".format
        line = row(self.index, self.start, self.duration, self.__concat_elements(), str(self.resources), str(self.active), str(self.completed), str(self.eleg), self.end)
        print(line)
        return line

    def set_default_values(self):
        self.end = 0
        self.completed = False
        self.eleg = False
        self.active = False
        self.start = 0

    def set_duration_beta(self):
        if( not self.duration==0):
            a = (11.0/20.0)*self.duration
            b = (23.0/8.0)*self.duration
            self.duration = beta.rvs(2, 5, a, b)
