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
import utils.activities_utils as gen_act

#Genetics
import utils.activities_utils as acts

#SGS

from sgs.parallel import Parallel
from sgs.serie import Serie
    
    
def sgs_serie():
    print('|------- Ejecutando Modelo SGS en Serie ------ |')
    activitties = gen_act.gen_activities();
    serie = Serie(activitties)
    serie.run()


def sgs_parallel():
    print('|------- Ejecutando Modelo SGS en Paralelo ------ |')
    activitties = gen_act.gen_activities();
    paral = Parallel(activitties)
    paral.run()



def showMenu():
    print('| Seleccione el modelo con el que desea operar: ')
    print('|----------------------------------------------|')
    print('| 1) Modelo SGS Paralelo.......................|')
    print('| 2) Modelo SGS Serie..........................|')
    print('|----------------------------------------------|')

    option = int(input('Ingrese su opción: '))
    
    if option<=0 and option>2:
        sys.exit()

    evaluate = {
            1: sgs_parallel,
            2: sgs_serie
        }

    result = evaluate.get(option)
    result()


def main():
    print(' Software de programación de actividades SGS Serie y paralelo ')
    # Displays the menu to go through either Parallel or Serie.
    showMenu()






main()