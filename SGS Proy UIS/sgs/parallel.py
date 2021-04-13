# Python libraries
import numpy as num
from typing import List
import operator
import sys
import random
import copy
# Models
from models.activity import Activity
from models.resources import Resources
# Utilities
import utils.randtime as rand
import utils.print as prt

# SGS
from sgs.base_model import BaseModel

#Genetics
import utils.activities_utils as gen_act


class Parallel(BaseModel):

    ################################# Variables de desempeño #############################
    smc:List[int]
    single_esc: bool
    esc_durations: List[int]
    initial_activities: List[Activity]
    esc: int
    rob: List[Activity]

    def __init__(self, activities: List[Activity], resources:List[int], with_logs:bool = True, single_esc = True):
        
        super(Parallel, self).__init__(activities, resources, with_logs)
        self.smc = []
        self.single_esc = single_esc
        self.esc_durations = []
        self.initial_activities = copy.deepcopy(activities)
        self.esc = 1
        self.rob = []

    def __printMaxNumberOfResources(self):
        print('Available Resources: ')
        prt.print_resources(self.resources)

    def __eval_single_risk(self, activity: Activity):
        ## 0-1 -> 0.6
        prob_risk = random.random()
        ## riesgo 1 pasa
        activity.eval_risk1(prob_risk)
        ## riesgo 2 se quema
        activity.eval_risk2(prob_risk)

        ## beta: 10 - 12
        ## duracion original 11
        ## riesgo 1 pasó
        ## duracion = duracion + (0.5*11*0.5+ 0*11*0.7)
        new_duration =  activity.duration + (activity.risk1 * activity.duration_base + activity.risk2 * activity.duration_base)
        activity.duration = new_duration

    def __evaluate_risk(self):
        [self.__eval_single_risk(act) for act in self.activities if act.risk1 != 0 or act.risk2 != 0]

    ################### Reactive Programming ######################
    def __reset_activities(self):
        for act in self.activities:
            act.reset_activity()


    def schedule_activities(self):
        g:int=0
        tg:int=0
        y:int=0
        H:int=2000
        first2end:Activity
        while y<=len(self.activities):
            H=2000
            # determinar el tiempo de finalización de las actividades activas
            # filtra las actividades activas
            actives = [act for act in self.activities if act.active]
            # Se evalua el riesgo
            self.__evaluate_risk()
            # verifica que la anterior consulta retorne al menos un resultado
            if(len(actives)>0):
                # Busca la actividad que finaliza primero
                first2end = min(actives, key=operator.attrgetter('end'))
                H = first2end.end
                # Si una actividad activa finaliza se liberan sus recursos.
                [self.resources.add_resources(act.resources) for act in actives if act.end==H]
                tg = H
                # Se completa la actividad si estaba activa y alcanza su tiempo de finalización
                [act.complete_activity() for act in actives if act.end==tg and not act.completed and act.active]

            # Se filtran las actividades que son elegibles
            eleg=self.get_elegible_activities()
            if (len(eleg)>0):
                # Se programan las actividades que sean elegibles y puedan activarse segun los recursos disponibles.
                [self.__schedule_activity(act, tg) for act in eleg if act.index!=1]
            y+=1

        # print('######## Actividades después de ser programadas ############')
        # prt.print_activities(self.activities)

    def __schedule_activity(self, act:Activity, currentTime:int):
        # Se reducen los recursos disponibles
        self.resources.reduce_resources(act.resources)
        act.reset_activity()
        act.active=True
        act.start = currentTime
        # Se asigna su duración con un número aleatorio
        #act.duration=rand.get_random_duration(act.index)
        # Se cacula el momento en que finaliza
        act.end=currentTime+act.duration

    def __eval_prec(self, act:Activity):
        # Inicia en true para hacer una operación AND en caso de que alguna de las precedencias no se haya completado retorna false
        res:bool=True
        for i in act.precedence:
            if(i>0):
                actc=next(act for act in self.activities if act.index==i)
                res&=actc.completed
        return res and not act.completed and not act.eleg and not act.active


    def __calculate_robust(self, esc:int):
        n_activities = len(self.activities)
        robust1:float=0.0
        robust2:float=0.0
        expected_value: float = 0.0
        counter:int=0
        obj:Activity = next(act for act in self.activities if act.index==n_activities)
        ds = 0.0
        for j in range(n_activities):
            for i in range(self.esc):
                ds += (abs(self.initial_activities[j].start-self.rob[i][j].start))/self.esc
                if(j<1):
                    act_original = self.initial_activities[n_activities-1]
                    act_esc = self.rob[i][n_activities-1]
                    robust2+= abs(act_original.end-act_esc.end)
        robust1 = ds
        
        for d in self.esc_durations:
            expected_value += d
         
        expected_value = expected_value/float(esc)

        return [robust1, robust2/esc, expected_value]

    def set_partial_rob(self):
        n_activities = len(self.initial_activities)
        partial_result = 0.0
        for esc in self.rob:
            partial_result +=0

    def __run_reactive(self):
        # Número de escenarios requeridos:
        self.esc = 1
        if not self.single_esc:
            self.esc = int(input("Inserte el número de escenarios: "))
        for x in range(0, self.esc):
            self.__reset_activities()
            # Se inicia primero la actividad ficticia.
            self.init_first_activity()
            self.schedule_activities()
            # Se guardan los tiempos de inicio de cada actividad
            self.rob.append(copy.deepcopy(self.activities))
            #self.set_partial_rob()
            self.esc_durations.append((self.activities[len(self.activities)-1]).end)
            self.activities = copy.deepcopy(self.initial_activities)
           
    
        rob=self.__calculate_robust(self.esc)
        if(self.with_logs):
            print(f'Robustez 1: {rob[0]} \nRobustez 2: {rob[1]} \nValor Esperado: {rob[2]}')

            #Muestra los tiempos registrados
            #prt.print_timestamp(self.smc)


    def run(self) -> Activity:
        # Activities are defined
        if(self.with_logs):
            self.print_activities()
        # Activities are ordered
        self.sort_activities('start')
        # Reactive programming is executed
        self.__run_reactive()
        return self.activities