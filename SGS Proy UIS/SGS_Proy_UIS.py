# Python libraries
import numpy as num
from numpy.random import default_rng
from typing import List
import operator
import sys
# Models
from models.activity import Activity
from models.resources import Resources
# Utilities
import utils.randtime as rand
import utils.print as prt
import utils.activities_utils as gen_act
import utils.file_uitls as futils
from solutions.j30 import J30
from scipy.stats import beta
import copy
#Genetics
import utils.activities_utils as acts

#SGS

from sgs.parallel import Parallel
from sgs.serie import Serie
from genetics.genetic import Genetic
    

resources = Resources([10,10,5])    

def sgs_serie():
    print('|------- Ejecutando Modelo SGS en Serie ------ |')
    activitties = gen_act.gen_activities();
    serie = Serie(activitties, resources, True)
    serie.run()


def prepare_instance(instance):
    original_instance = futils.get_instance_from_file(instance[0])
    for i in range(len(instance[1])):
        act:Activity = ([act for act in instance[1] if act.index==i+1])[0]
        act_or: Activity = [act for act in original_instance.activities if act.index==i+1][0]
        act.duration_base = act_or.duration

    results = futils.load_results(instance[0])
    
    for tup in results:
        act = [act for act in instance[1] if act.index == tup[0]][0]
        act.start = tup[1]

    return [copy.deepcopy(instance[1]), original_instance.resources]


def sgs_parallel():
    print('\n|------- Ejecutando Modelo SGS en Paralelo ------ |')

    j30 = J30()

    instances = {
            1: ['j3014_3', j30.j3014_3],
            2: ['j3019_5', j30.j3019_5],
            3: ['j301_10', j30.j301_10],
            4: ['j301_2', j30.j301_2],
            5: ['j3020_7', j30.j3020_7],
            6: ['j3023_9', j30.j3023_9],
            7: ['j3037_8', j30.j3037_8],
            8: ['j3044_9', j30.j3044_9],
            9: ['j3047_6', j30.j3047_6],
            10: ['j306_3', j30.j306_3],
            11: ['j6011_8', j30.j6011_8],
            12: ['j6012_10', j30.j6012_10],
            13: ['j6014_2', j30.j6014_2],
            14: ['j6017_6', j30.j6017_6],
            15: ['j601_2', j30.j601_2],
            16: ['j601_6', j30.j601_6],
            17: ['j6022_10', j30.j6022_10],
            18: ['j603_5', j30.j603_5],
            19: ['j604_6', j30.j604_6],
            20: ['j607_7', j30.j607_7]
        }
    keys = list(instances.values())
    for i in range(len(keys)):
        print(f'{i}. {(keys[i])[0]}')

    option = int(input('Seleccione la instancia a evaluar'))
    la = prepare_instance(instances.get(option))

    paral = Parallel(la[0], Resources(la[1]), with_logs = True, single_esc=False)
    paral.run()

def sgs_genetic():
    print('\n|---------- Ejecutando Algoritmo genético --------|')
    pob = int(input('Ingrese el número de individuos en la población: '))
    gen = int(input('Ingrese el número de generaciones que desea: '))
    Gen = Genetic(nPob=pob, generations=gen)
    Gen.run_genetic()

def calc_beta():
    rng = default_rng()
    a = (11.0/20.0)*10
    b = (23.0/8.0)*10
    r = beta.rvs(a, b, loc= a, scale= b-a, size=10)
    print(r)

def showMenu():
    print('| Seleccione el modelo con el que desea operar: ')
    print('|----------------------------------------------|')
    print('| 1) Modelo SGS Paralelo sol. profesor.........|')
    print('| 2) Modelo SGS Serie..........................|')
    print('| 3) Algoritmo genético........................|')
    print('| 4) Prueba distribución beta..................|')
    print('|----------------------------------------------|')

    option = int(input('Ingrese su opción: '))
    
    if option<=0 and option>2:
        sys.exit()

    evaluate = {
            1: sgs_parallel,
            2: sgs_serie,
            3: sgs_genetic,
            4: calc_beta
        }

    result = evaluate.get(option)
    result()


def main():
    print(' Software de programación de actividades SGS Serie y paralelo ')
    # Displays the menu to go through either Parallel or Serie.
    showMenu()






main()