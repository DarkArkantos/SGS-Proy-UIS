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
from scipy.stats import beta
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


def sgs_parallel():
    print('\n|------- Ejecutando Modelo SGS en Paralelo ------ |')
    activitties = gen_act.gen_activities();
    paral = Parallel(activitties, resources, with_logs = True, single_esc=False)
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
    print('| 1) Modelo SGS Paralelo.......................|')
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