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

    with_logs : bool

    def __init__(self, activities: List[Activity], resources:Resources, with_logs: bool):
        self.activities = activities
        self.resources = resources
        self.with_logs = with_logs

    def sort_activities(self, param: str):
        # Activities are ordered according to the starting time equivalent to
        # vector Z(K)
        self.activities.sort(key=operator.attrgetter(param))
        if(self.with_logs):
            print('############ Actividades Ordenadas segun su tiempo de inicio ##########')
            print(f'\n Number of Activities: {len(self.activities)}')
            prt.print_activities(self.activities)

    def print_activities(self):
        if(self.with_logs):
            print(f'\n Activities: {len(self.activities)}')
            print('############   Available activities:  ##############')
            prt.print_activities(self.activities)

    def print_resources(self):
        if(self.with_logs):
            print(f'\nCurrent resources: ')
            prt.print_resources(self.resources)

    def get_elegible_activities(self) -> List[Activity]:
        [act.set_eleg() for act in self.activities 
                if self.__eval_prec(act) and act.index != 1 and self.resources.check_enough_resources(act.resources)]
        return [act for act in self.activities if act.eleg]

    def select_activity():
        print('not implemented')

    def complete_activity(self, activity: Activity):
        activity.complete_activity()
        self.resources.add_resources(activity.resources)

    def __eval_prec(self, act:Activity) -> bool:
        # Inicia en true para hacer una operación AND en caso de que alguna de
        # las precedencias no se haya completado retorna false
        res :bool = True

        for i in act.pre:
            if(i > 0):
                try:
                    actc = next(act for act in self.activities if act.index == i)
                    res&=actc.completed
                except StopIteration:
                    print('Something weird happened... Discarting Chromosome')

        return res and not act.completed and not act.eleg and not act.active

    def __get_index(self, index: int):
        for i in range(len(self.activities)):
            if(self.activities[i].index == index):
                return i


    def init_first_activity(self):
        act1 = next((act for act in self.activities if act.index == 1), None)
        act1.reset_activity()
        act1.active = True
        act1.d = 0