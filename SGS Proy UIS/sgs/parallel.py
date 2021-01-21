# Python libraries
import numpy as num
from typing import List
import operator
import sys
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

    def __init__(self, activities: List[Activity], resources:List[int], with_logs:bool = True, single_esc = True):
        
        super(Parallel, self).__init__(activities, resources, with_logs)
        self.smc = []
        self.single_esc = single_esc


    def __printMaxNumberOfResources(self):
        print('Available Resources: ')
        prt.print_resources(self.resources)

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

        print('######## Actividades después de ser programadas ############')
        prt.print_activities(self.activities)

    def __schedule_activity(self, act:Activity, currentTime:int):
        # Se reducen los recursos disponibles
        self.resources.reduce_resources(act.resources)
        act.reset_activity()
        act.active=True
        # Se asigna su duración con un número aleatorio
        act.duration=rand.get_random_duration(act.index)
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

    def __append_start_time(self, act:Activity):
        self.smc.append(act.end-act.duration)


    def __calculate_robust(self, esc:int):
        robust1:float=0.0
        robust2:float=0.0
        counter:int=0
        obj:Activity = next(act for act in self.activities if act.index==28)
        for i in range(1,len(self.smc)+1):
            if(i%28==0 and i!=0):
                counter+=1
                robust2+=(obj.start-self.smc[i-1])/esc
            robust1+=abs(self.activities[i-1-(counter*28)].start-self.smc[i-1])/(esc)
        return [robust1, robust2]



    def __run_reactive(self):
        # Número de escenarios requeridos:
        esc = 1
        if not self.single_esc:
            esc = int(input("Inserte el número de escenarios: "))
        for x in range(0, esc):
            self.__reset_activities()
            # Se inicia primero la actividad ficticia.
            self.init_first_activity()
            self.schedule_activities()
            # Se guardan los tiempos de inicio de cada actividad
            [self.__append_start_time(act) for act in self.activities]       
    
        rob=self.__calculate_robust(esc)
        print(f'Robustez 1: {rob[0]} \nRobustez 2: {rob[1]}')
        #Muestra los tiempos registrados
        prt.print_timestamp(self.smc)


    def run(self) -> Activity:
        # Activities are defined
        self.print_activities()
        # Activities are ordered
        self.sort_activities('start')
        # Reactive programming is executed
        self.__run_reactive()
        return self.activities[len(self.activities)-1]