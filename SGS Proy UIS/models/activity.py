from typing import List
from models.Resources import Resources
class Activity:
    # indice
    index:int
    # inicio tiempo de la actividad
    start:int
    # prioridad
    duration:int
    # precedencia
    pre:List[int]
    # recursos [0,0,0]
    resources:Resources
    # activa
    active:bool
    # completada
    completed:bool
    # elegible
    eleg:bool
    # tiempo de finalización
    end:int


    def __init__(self, index:int, start:int, duration:int, pre:List[int], resources:Resources, active:bool, completed:bool, eleg:bool, end:int):
        self.index = index
        self.start=start
        self.duration=duration
        self.pre=pre
        self.resources=resources
        self.active=active
        self.completed = completed
        self.eleg = eleg
        self.end = end
    
    def __concat_elements(self):
        res=''
        for index in range(0, len(self.pre)):
            res+=str(self.pre[index])+', '
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


    def print_activity(self):
        row = "|  {:^3d}  |  {:^5d}  |  {:^5d}  |  {:>16s}  |  {:^3d} - {:^3d} - {:^3d}  |  {:^5s}  |  {:^5s}  |  {:^5s}  |  {:^3d}  |".format
        print(row(self.index, self.start, self.duration, self.__concat_elements(), self.resources.PL,self.resources.QA,self.resources.DE, str(self.active), str(self.completed), str(self.eleg), self.end))

    
