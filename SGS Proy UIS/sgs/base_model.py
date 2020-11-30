# Python libraries
import numpy as num
from typing import List
import operator
import sys

# Models
from models.activity import Activity
from models.Resources import Resources

# Utilities
import utils.randtime as rand
import utils.print as prt

class BaseModel:

    ################################### Proactive Programming
    ################################### #############################
    # Variables
    # Actividades en el proyecto
    activities : List[Activity]
    # Máxima cantidad de recursos disponibles por periodo de tiempo -> PL
    # (Project Leader), QA(Quality Assesment), DE(Designer Engineer)
    resources : Resources

    def __init__(self, activities: List[Activity], resources:Resources):
        self.activities = activities
        self.resources = resources

    def sort_activities(self, param: str):
        # Activities are ordered according to the starting time equivalent to
        # vector Z(K)
        print('############ Actividades Ordenadas segun su tiempo de inicio ##########')
        print(f'\n Number of Activities: {len(self.activities)}')
        self.activities.sort(key=operator.attrgetter(param))
        prt.print_activities(self.activities)

    def print_activities(self):
        print(f'\n Activities: {len(self.activities)}')
        print('############   Available activities:  ##############')
        prt.print_activities(self.activities)

    def get_elegible_activities(self) -> List[Activity]:
        [act.set_eleg() for act in self.activities 
                if self.__eval_prec(act) and act.index != 1 and self.resources.check_enough_resources(act.resources)]
        return [act for act in self.activities if act.eleg]

    def select_activity():
        print('not implemented')

    def __eval_prec(self, act:Activity) -> bool:
        # Inicia en true para hacer una operación AND en caso de que alguna de
        # las precedencias no se haya completado retorna false
        res :bool = True
        for i in act.pre:
            if(i > 0):
                actc = next(act for act in self.activities if act.index == i)
                res&=actc.completed

        return res and not act.completed and not act.eleg and not act.active

    def init_first_activity(self):
        act1 = next((act for act in self.activities if act.index == 1), None)
        act1.reset_activity()
        act1.active = True
        act1.d = 0