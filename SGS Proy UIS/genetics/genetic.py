from sgs.serie import Serie
from sgs.parallel import Parallel
from models.activity import Activity
from typing import List
import utils.activities_utils as gen_act
from utils.ThreadWithReturn import ThreadWithReturn
import utils.print as prnt
import _thread as thread

from queue import Queue # Python 3.x
from threading import Thread

import time

import concurrent.futures as tasks



class Genetic:
  
    nPobActivities : List[List[Activity]]
    ## List of the last activity that indicates the makespan of each choromosome
    makeSpan: List[Activity]
    ## Best makespan obtained so far.
    best_makespan: List[Activity]

    nPob : int
    def __init__(self, nPob: int):
        self.nPob = nPob
        self.nPobActivities = []
        self.makeSpan=[]
        self.best_makespan = []
    
    def set_npob(self):
        """ Sets the list of chromosomes in the genetic algorithm """
        for i in range(0, self.nPob):
            print(f'Chromosome: {i}')
            chromosome = self.set_single_chromosome()
            prnt.print_activities(chromosome)
            self.nPobActivities.append(chromosome)

    def set_single_chromosome(self) -> List[Activity]:
        """Creates a single chromosome, this process runs 1000 times to get a good average"""

        ## Initial list, range goes from 0 to 999 discounting this initial
        ## asignment
        chromosome : List[Activity] = self.get_single_sgs_serie()
        ## Division by 1001 due to the extra sample that is being taken
        ## (initial list).
        for act in chromosome:
            act.start/=1001
        
        initialTime = time.time()
        for i in range(0, 5):
            print(f'Progress: {(i+1)/20}%')
            res :List[List[Activity]] = self.multi_threading(threads=2)
            print(f'Number of lists: {len(res)}')
            for r in res:
                for j in range(0, len(r)):
                    chromosome[j].start += r[j].start / 101
            
        print()
        print(f'Time elapsed for creating one Chromosome: \n {time.time()-initialTime}s\n')
        return chromosome

    def get_single_sgs_serie(self) -> List[Activity]:
        activitties = gen_act.gen_activities()
        serie = Serie(activitties, False)
        return serie.run()

    def get_sgs_serie(self) -> List[List[Activity]]:
        print('Thread started')
        res : List[List[Activity]] = []
        for i in range(0, 10):
            res.append(self.get_single_sgs_serie())
        print('Thread ended')
        return res

    def multi_threading(self, threads: int=3) -> List[List[Activity]]:
        thread_list = []
        que = Queue()
        for i in range(0, threads):
            #t = Thread(target=self.get_sgs_serie)
            t = ThreadWithReturn(target= self.get_sgs_serie)
            t.start()
            thread_list.append(t)

        res : List[List[Activity]] = []

        for t in thread_list:
            for items in t.join():
                res.append(items)       
        
        return res


    def run_parallel(self):
        for acts in self.nPobActivities:
            parallel = Parallel(activities=acts, with_logs=False)
            self.makeSpan.append(parallel.run())
    

    def set_best_makespan(self):
        self.makeSpan.sort('end')
        current_best: Activity = self.best_makespan[len(self.best_makespan)]
        new_best:Activity= self.makeSpan[len(self.makeSpan)-1]
        is_better = new_best.end < current_best.end

        if is_better:
            self.best_makespan = new_best


    def run_genetic(self):
        print('......')
        ## The population is set
        self.set_npob()
        ## Each chromosome is run using the parallel mode.
        self.run_parallel()
        ## Sets the Best Makespan
        self.set_best_makespan()

    


