# Python libraries
import numpy as num
from typing import List
import operator
# Models
from models.activity import Activity
from models.Resources import Resources
# Utilities
import utils.randtime as rand
import utils.print as prt

#Genetics
import genetics.activities as acts


################################### Proactive Programming #############################
# Variables
# Actividades en el proyecto
activities: List[Activity] =[]

# Máxima cantidad de recursos disponibles por periodo de tiempo -> PL (Project Leader), QA(Quality Assesment), DE(Designer Engineer)
resources = Resources(10,10,5)

################################# Variables de desempeño #############################
smc:List[int]=[]
    



def set_activites():
      #                        Index Strt Prio Prece         Recursos              Activo Coplet Elegi  end
    activities.append(Activity(1,  0,  0, [0],           Resources(0,0,0),     False, False, False, 0))
    activities.append(Activity(2,  0,  0, [1],           Resources(5,0,0),     False, False, False, 0))
    activities.append(Activity(3,  0,  0, [1],           Resources(0,0,5),     False, False, False, 0))
    activities.append(Activity(4,  4,  0, [1],           Resources(2,0,5),     False, False, False, 0))
    activities.append(Activity(5,  6,  0, [2,3,4],       Resources(8,0,0),     False, False, False, 0))
    activities.append(Activity(6,  7,  0, [5],           Resources(5,0,0),     False, False, False, 0))
    activities.append(Activity(7,  0,  0, [1],           Resources(4,0,0),     False, False, False, 0))
    activities.append(Activity(8,  8,  0, [6,7],         Resources(0,0,0),     False, False, False, 0))
    activities.append(Activity(9,  10, 0, [8],           Resources(0,0,0),     False, False, False, 0))
    activities.append(Activity(10, 28, 0, [9],           Resources(0,10,0),    False, False, False, 0))
    activities.append(Activity(11, 30, 0, [9],           Resources(0,10,0),    False, False, False, 0))
    activities.append(Activity(12, 32, 0, [9],           Resources(0,0,0),     False, False, False, 0))
    activities.append(Activity(13, 33, 0, [10,11],       Resources(0,0,0),     False, False, False, 0))
    activities.append(Activity(14, 39, 0, [12,13],       Resources(0,0,0),     False, False, False, 0))
    activities.append(Activity(15, 41, 0, [14],          Resources(10,0,0),    False, False, False, 0))
    activities.append(Activity(16, 42, 0, [15],          Resources(0,0,0),     False, False, False, 0))
    activities.append(Activity(17, 42, 0, [15],          Resources(0,0,0),     False, False, False, 0))
    activities.append(Activity(18, 54, 0, [17],          Resources(0,0,0),     False, False, False, 0))
    activities.append(Activity(19, 42, 0, [15],          Resources(0,0,0),     False, False, False, 0))
    activities.append(Activity(20, 42, 0, [15],          Resources(0,0,0),     False, False, False, 0))
    activities.append(Activity(21, 52, 0, [20],          Resources(0,0,0),     False, False, False, 0))
    activities.append(Activity(22, 60, 0, [16,18,19,21], Resources(5,0,0),     False, False, False, 0))
    activities.append(Activity(23, 58, 0, [15],          Resources(5,0,0),     False, False, False, 0))
    activities.append(Activity(24, 56, 0, [15],          Resources(0,10,0),    False, False, False, 0))
    activities.append(Activity(25, 64, 0, [22,24,23],    Resources(10,0,0),    False, False, False, 0))
    activities.append(Activity(26, 66, 0, [25],          Resources(0,0,0),     False, False, False, 0))
    activities.append(Activity(27, 70, 0, [26],          Resources(2,0,0),     False, False, False, 0))
    activities.append(Activity(28, 90, 0, [27],          Resources(0,0,0),     False, False, False, 0))
    print('############   Actividades a usar:  ##############')
    prt.print_activities(activities)


def printMaxNumberOfResources():
    print(f'Resource type: PL, Max Resources: {resources.PL}')
    print(f'Resource type: QA, Max Resources: {resources.QA}')
    print(f'Resource type: DE, Max Resources: {resources.DE}')
    print('')    

################### Reactive Programming ######################
def reset_activities():
    for act in activities:
        act.reset_activity()

def init_first_activity():
    act1 = next((act for act in activities if act.index==1), None)
    act1.reset_activity()
    act1.active= True
    act1.d = 0


def schedule_activities():
    g:int=0
    tg:int=0
    y:int=0
    H:int=2000
    first2end:Activity
    while y<=len(activities):
        H=2000
        # determinar el tiempo de finalización de las actividades activas
        # filtra las actividades activas
        actives = [act for act in activities if act.active]
        # verifica que la anterior consulta retorne al menos un resultado
        if(len(actives)>0):
            # Busca la actividad que finaliza primero
            first2end = min(actives, key=operator.attrgetter('end'))
            H = first2end.end
            # Si una actividad activa finaliza se liberan sus recursos.
            [resources.add_resources(act.resources) for act in actives if act.end==H]
            tg = H
            # Se completa la actividad si estaba activa y alcanza su tiempo de finalización
            [act.complete_activity() for act in actives if act.end==tg and not act.completed and act.active]

        # Se determina si las precedencias ya fueron completadas y se define como elegible
        [act.set_eleg() for act in activities if eval_prec(act) and act.index!=1]
        # Se filtran las actividades que son elegibles
        eleg=[act for act in activities if act.eleg]
        if (len(eleg)>0):
            # Se programan las actividades que sean elegibles y puedan activarse segun los recursos disponibles.
            [schedule_activity(act, tg) for act in eleg if act.index!=1]
        y+=1

    print('######## Actividades después de ser programadas ############')
    prt.print_activities(activities)

def schedule_activity(act:Activity, currentTime:int):
    # Se determina si hay suficientes recursos para programar una actividad.
    if(resources.check_enough_resources(act.resources)):
        # Se reducen los recursos disponibles
        resources.reduce_resources(act.resources)
        act.reset_activity()
        act.active=True
        # Se asigna su duración con un número aleatorio
        act.duration=rand.get_random_duration(act.index)
        # Se cacula el momento en que finaliza
        act.end=currentTime+act.duration

def eval_prec(act:Activity):
    # Inicia en true para hacer una operación AND en caso de que alguna de las precedencias no se haya completado retorna false
    res:bool=True
    for i in act.pre:
        if(i>0):
            actc=next(act for act in activities if act.index==i)
            res&=actc.completed
    return res and not act.completed and not act.eleg and not act.active

def append_start_time(act:Activity):
    smc.append(act.end-act.duration)

def calculate_robust(esc:int):
    robust1:float=0.0
    robust2:float=0.0
    counter:int=0
    obj:Activity = next(act for act in activities if act.index==28)
    for i in range(1,len(smc)+1):
        if(i%28==0 and i!=0):
            counter+=1
            robust2+=(obj.start-smc[i-1])/esc
        robust1+=abs(activities[i-1-(counter*28)].start-smc[i-1])/(esc)
    return [robust1, robust2]

def run_reactive():
    # Número de escenarios requeridos:
    esc = int(input("Inserte el número de escenarios: "))
    for x in range(0, esc):
        reset_activities()
        # Se inicia primero la actividad ficticia.
        init_first_activity()
        schedule_activities()
        # Se guardan los tiempos de inicio de cada actividad
        [append_start_time(act) for act in activities]       
    
    rob=calculate_robust(esc)
    print(f'Robustez 1: {rob[0]} \nRobustez 2: {rob[1]}')
    #Muestra los tiempos registrados
    prt.print_timestamp(smc)
    
    

def main():
    # Proactive
    printMaxNumberOfResources()
    # sets the group of activitiess
    #activities = acts.gen_activities()
    set_activites()
    # Se ordena la lista según el tiempo de inicio de cada actividad esto es equivalente al vector Z(K)
    print('############ Actividades Ordenadas segun su tiempo de inicio ##########')
    activities.sort(key=operator.attrgetter('start'))
    prt.print_activities(activities)

    # Reactive
    run_reactive()
    #input("Presione cualquier tecla para continuar")






main()