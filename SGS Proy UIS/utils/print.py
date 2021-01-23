from typing import List
from models.activity import Activity
from models.resources import Resources
from genetics.chromosome import Chromosome
# Header de las tablas
header = '    #      Inicio   Duración      Precedencia         Recursos          Activo   Completado  Elegible Finalización '
divider = '-------------------------------------------------------------------------------------------------------------'

def print_resources(res: List[int]):
    for i in range(res):
        print(f'R{i}: {res[i]}\n')

def print_timestamp(smc:List[int]):
    for sm in range(len(smc)):
        print(f'Index: {sm+1}, Time: {smc[sm]}')

def print_activities(acts:List[Activity]):
    content = header+'\n'
    for a in acts:
        content+= a.print_activity()
        content+= divider+'\n'
    print(content)
    print('\n \n')
    return content

def print_chromosome(chromosome: Chromosome, generations: int, pop: int):
    title = 'Best chromosome:\n'
    fitness = 'Fitness (project_duration): '+str(chromosome.fitness)+'\n'
    pop_s = 'Population: '+str(pop)+'\n'
    generations_s = 'Generations: '+str(generations)+'\n'
    divider_l = divider+'\n'
    print(title)
    print(fitness)
    print(divider_l)
    
    activities = print_activities(chromosome.genes)
    res = title+fitness+pop_s+generations_s+divider_l+activities
    return res


def print_to_file(chromosome:Chromosome, filename:str,  generations: int, pop: int):
    content = print_chromosome(chromosome, generations, pop)
    with open(filename+'.txt', 'w') as file:
        file.write(content)