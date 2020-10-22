from typing import List
from models.activity import Activity
from models.Resources import Resources
# Header de las tablas
header = '    #    Inicio   Duración      Precedencia        Recursos          Activo   Completado  Elegible Finalización '
divider = '-----------------------------------------------------------------------------------------------------------'

def print_resources(res: Resources):
    print(f'PL: {res.PL}  QA: {res.QA}   DE: {res.DE}')

def print_timestamp(smc:List[int]):
    for sm in range(len(smc)):
        print(f'Index: {sm+1}, Time: {smc[sm]}')

def print_activities(acts:List[Activity]):
    print(header)
    for a in acts:
        a.print_activity()
        print(divider)
    print('\n \n')
