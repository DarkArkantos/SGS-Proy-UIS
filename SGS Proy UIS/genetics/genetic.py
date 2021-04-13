from sgs.serie import Serie
from sgs.parallel import Parallel
from models.activity import Activity
from models.instance import Instance
from models.pascal_scheme import PascalScheme
from models.resources import Resources
from typing import List
import utils.activities_utils as gen_act
from utils.ThreadWithReturn import ThreadWithReturn
import utils.print as prnt
from genetics.chromosome import Chromosome
import marshmallow_dataclass
import copy
import sys
import time
import random
import operator
import json

import concurrent.futures as tasks



class Genetic:
  
    chromosomes : List[Chromosome]
    ## List of the last activity that indicates the makespan of each
    ## choromosome
    makespan : List[Activity]
    ## Best makespan obtained so far.
    best_makespan : List[Activity]
    ## Fitness ending time of the best last activity
    fitness_reference: Activity
    ## Number of generations
    generations : int
    ##
    nPob : int
    ## mutation rate
    mutation_rate : float
    ## Resources default
    resources = Resources([10,10,5])
    ## Experimental?
    experimental = True
    file_name: str

    def __init__(self, nPob: int, generations, mutation_rate: float=0.3):
        if(not nPob % 2 == 0 or not nPob>2):
            raise Exception(f'The populations must be an even number {nPob} and greater than 2')
        self.nPob = nPob
        self.chromosomes = []
        self.makespan = []
        self.best_makespan = []
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.fitness_reference = Activity.empty_activity()
    
    def set_experimental_pob(self):
        """ Sets the list of chromosomes in the genetic algorithm """
        for i in range(0, self.nPob):
            print(f'Chromosome: {i}')
            chromosome = self.set_single_chromosome()
            prnt.print_activities(chromosome.genes)
            self.chromosomes.append(chromosome)

    def set_pob_from_json(self):
        ## Test: D:\VS\Proyecto SGS UIS\SGS Proy UIS\Resources\instancej301_2.json
        print('\n')
        self.experimental = False
        basefilePath = "D:\VS\Proyecto SGS UIS\SGS Proy UIS\Resources\instance"
        self.file_name = input('Ingrese la instancia a ejecutar (ej. j603_5): ')
        print('\nReading Json file...')      
        instance_schema = marshmallow_dataclass.class_schema(Instance, base_schema=PascalScheme)()

        with open(f'{basefilePath}{self.file_name}.json', 'r', encoding='utf-8', errors='ignore') as j:
            json_dic = json.loads(j.read())

        instance: Instance = instance_schema.load(json_dic)
        self.resources:Resources = Resources(instance.resources)
        for i in range(self.nPob):
            activities = copy.deepcopy(instance.activities)
            [act.set_default_values() for act in activities]
            [act.set_duration_beta() for act in activities]
            genes = self.get_single_sgs_serie(activities)
            self.chromosomes.append(Chromosome(genes=genes))
        # TODO: Take the activities on the list and produce the rest of chromosomes.
        print('Json loaded')

    def set_single_chromosome(self) -> Chromosome:
        """Creates a single chromosome, this process runs 1000 times to get a good average"""

        ## Initial list, range goes from 0 to 999 discounting this initial
        ## asignment
        chromosome = Chromosome(genes=self.get_single_sgs_serie())
        ## Division by 1001 due to the extra sample that is being taken
        ## (initial list).
        for act in chromosome.genes:
            act.start/=1001
        
        initialTime = time.time()
        for i in range(0, 5):
            print(f'Progress: {(i+1)/20}%')
            res :List[Chromosome] = self.multi_threading(threads=2)
            print(f'Number of lists: {len(res)}')
            for ch in res:
                for j in range(0, len(ch.genes)):
                    chromosome.genes[j].start += ch.genes[j].start / 101
            
        print()
        print(f'Time elapsed for creating one Chromosome: \n {time.time()-initialTime}s\n')
        return chromosome

    def get_single_sgs_serie(self, activities:List[Activity]) -> List[Activity]:
        """Runs the SGS Algorithm once, returns a list of activities representing it."""
        serie = Serie(activities, self.resources, False, experimental= self.experimental)
        return serie.run()

    def get_sgs_serie(self) -> List[List[Activity]]:
        print('Thread started')
        res : List[List[Activity]] = []
        for i in range(0, 10):
            activities = gen_act.gen_activities()
            res.append(self.get_single_sgs_serie(activities))
        print('Thread ended')
        return res

    def multi_threading(self, threads: int=3) -> List[Chromosome]:
        thread_list = []
        for i in range(0, threads):
            t = ThreadWithReturn(target= self.get_sgs_serie)
            t.start()
            thread_list.append(t)

        res : List[Chromosome] = []

        for t in thread_list:
            for items in t.join():
                res.append(Chromosome(genes=items))
        return res


    def run_parallel(self):
        self.makespan.clear()
        chromosomes:List[Chromosome] = []
        for chromosome in self.chromosomes:
            genes = copy.deepcopy(chromosome.genes)
            parallel = Parallel(activities=genes, resources=self.resources, with_logs=False)
            scheduled: List[Activity]= parallel.run()
            self.makespan.append(scheduled[len(scheduled)-1])
            chromosome.genes = copy.deepcopy(scheduled)
            chromosomes.append(chromosome)
            del parallel
        self.chromosomes.clear()
        self.chromosomes = chromosomes
    

    def set_best_makespan(self):
        ## List sorted to get the best end
        makespan_sorted = sorted(self.makespan, key=self.get_end, reverse=True)
        current_best : Activity = Activity.empty_activity()
        current_best.end = 1000000
        index_current_best = 0

        if not len(self.best_makespan) == 0:
            current_best : Activity = self.best_makespan[len(self.best_makespan) - 1]

        new_best : Activity = makespan_sorted[0]
        
        
        is_better = new_best.end < current_best.end

        if is_better:
            index :int = self.makespan.index(new_best)
            self.best_makespan = copy.deepcopy(self.chromosomes[index].genes)
            self.fitness_reference = copy.deepcopy(new_best)

        for chromosome in self.chromosomes:
            act = max(chromosome.genes, key= self.get_end)
            new_fitness = float(new_best.end)/float(act.end)
            chromosome.fitness = new_fitness
            #print(f'new fitness {new_fitness}')

        print('\n\nCurrent best: ')
        current_best.print_activity()

        print('New best: ')
        self.best_makespan[len(self.best_makespan) - 1].print_activity()
        print('\n')

    def get_end(self, act: Activity):
        return act.end
    

    def parent_selection()-> List[List[Activity]]:
        """Gets the best 50% of the population"""
        parents:List[List]


    def cross_pob(self):
        print('### Starting crossing.... #####')
        new_pob : List[Chromosome] = []
        
        for i in range(0, len(self.chromosomes), 2):
            pair = self.get_crossed(self.chromosomes[i], self.chromosomes[i + 1])
            for chromosome in pair:
                    new_pob.append(chromosome)



        return new_pob

    def get_crossed(self, chromosome1: Chromosome, chromosome2: Chromosome):
        genes_len = len(chromosome1.genes)-1
        cross_point1 = random.randint(1, genes_len)
        cross_point2 = random.randint(cross_point1, genes_len)
        mutation_index = random.randint(0, 1)

        chromosome1.genes.sort(key=operator.attrgetter('index'))
        chromosome2.genes.sort(key=operator.attrgetter('index'))

                
        #prnt.print_activities(chromosome1.genes)        
        #prnt.print_activities(chromosome2.genes)

        #print(f'Cross Point 1: {cross_point1}, Cross Point 2: {cross_point2}')

        if mutation_index == 0:
            self.mutate_chromosome(chromosome1)
        if mutation_index == 1:
            self.mutate_chromosome(chromosome2)

        for i in range(cross_point1, cross_point2):
            genes1 = copy.deepcopy(chromosome1.genes[i])
            genes2 = copy.deepcopy(chromosome2.genes[i])
            chromosome1.genes[i] = genes2
            chromosome2.genes[i] = genes1
        
        #print('Chromosome 1: ')
        #prnt.print_activities(chromosome1.genes)
        #print('Chromosome 2: ')
        #prnt.print_activities(chromosome2.genes)
        return [chromosome1, chromosome2]

    def mutate_chromosome(self, chromosome: Chromosome, places: int=1):
        """Mutates a chromosome by moving 10% of the activities a random position between 1-3 places forward
        chromosome -- List[Activitiy] Chromosome to be mutated.
        places -- int Upper limit of places the activity will be moved. 3 by default
        """
        chromosome_to_mutate = copy.deepcopy(chromosome)
        ## Determine how many places each gene is going to be moved
        position = random.randint(1, places)
        chromosome_len: int = len(chromosome_to_mutate.genes)
        ## Number of genes to be moved.
        number_of_genes = round(chromosome_len * self.mutation_rate)
        for i in range(0, number_of_genes):
            gene_index = random.randint(1, chromosome_len-2)
            new_index = gene_index+position
            ## Checks that the new index doesn't surpass the len of the array
            if(new_index>=chromosome_len-1):
                new_index = new_index - chromosome_len + 2 # Moves to extra positions to avoid first activity 
            gene1 = chromosome_to_mutate.genes[gene_index]
            gene2 = chromosome_to_mutate.genes[new_index]

            ## Updates the new indexes
            gene1.index = new_index + 1
            gene2.index = gene_index + 1
            ## Sets the genes in the chromosome
            chromosome_to_mutate.genes[new_index] = gene1
            chromosome_to_mutate.genes[gene_index] = gene2
            #print('After mutation: ')
            #prnt.print_activities(chromosome_to_mutate.genes)
            if(not chromosome_to_mutate.is_a_valid_chromosome()):
                #print('Chromosome not valid')
                return
            # print('After mutation: ')
            # prnt.print_activities(chromosome.genes)
            chromosome = chromosome_to_mutate
        

    def menu(self):
        print('\n')
        print('| Running genetic algorithm, select one of the following options')
        print('| 1. Run with simulated data ................................. |')
        print('| 2. Run with model from JsonFile .............................|')
        print('| 3. Exit .....................................................|')
        print('\n')
        option = int(input('Option: '))

        if option<=0 and option>2:
            sys.exit()

        evaluate = {
            1: self.set_experimental_pob,
            2: self.set_pob_from_json,
            3: sys.exit
            }
        result = evaluate.get(option)
        result()


    def set_risk(self, activities: List[Activity]):
            n_activities = []
            r1 = []
            r2 = []
            r3 = []
            risk_1 = 0.5
            risk_2 = 0.6


            if(len(activities)==32):
                r1 = [3]
                r2 = [5, 16, 22, 29, 18]
                r3 = [4, 9, 17, 29]

            elif(len(activities)==62):
                r1 = [2, 3, 6, 11, 27, 30, 33, 41, 45, 61]
                r2 = [12, 14, 20, 29, 38, 50, 51, 56]
                r3 = [25, 43]
            
            else:
                [act.set_risk3(0, 0) for act in activities]

            for i in r1:
                [act.set_risk1(risk_1) for act in activities if act.index==i]
            for i in r2:
                [act.set_risk2(risk_2) for act in activities if act.index==i]
            for i in r3:
                [act.set_risk3(risk_1, risk_2) for act in activities if act.index==i]

    def run_genetic(self):
        print('......')
        self.menu()
        for i in range(0, self.generations):
            ## Each chromosome is run using the parallel mode.
            self.run_parallel()
            ## Sets the Best Makespan
            self.set_best_makespan()
            
            ## Choose the parents
       
            ## Crossing
            crossed_and_mutated = copy.deepcopy(self.cross_pob())
            self.chromosomes.clear()
            self.chromosomes = crossed_and_mutated
            print(f'Current Generation: {i}')
            print(f'Current fitness: {self.fitness_reference.end}')
        # Termina genético
        self.set_risk(self.best_makespan)
        p = Parallel(self.best_makespan, self.resources, with_logs= True, single_esc = False)
        p.run()
        #prnt.print_to_file(Chromosome(genes=self.best_makespan, fitness= self.fitness_reference.end), self.file_name, self.generations, self.nPob)
    


        