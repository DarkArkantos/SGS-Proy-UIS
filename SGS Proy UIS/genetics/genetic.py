from sgs.serie import Serie
from models.activity import Activity
from typing import List
import utils.activities_utils as gen_act
from utils.ThreadWithReturn import ThreadWithReturn
import utils.print as prnt
import _thread as thread

from queue import Queue # Python 3.x
from threading import Thread

import concurrent.futures as tasks



class Genetic:
  
    nPobActivities : List[List[Activity]]
    nPob : int
    def __init__(self, nPob: int):
        self.nPob = nPob
        self.nPobActivities = []
    
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
        
        for i in range(0, 4):
            print(f'Progress: {(i+1)/10}%', end='\r')
            res :List[List[Activity]] = self.multi_threading(threads=5)
            print(f'Number of lists: {len(res)}')
            for r in res:
                for j in range(0, len(r)):
                    chromosome[j].start += r[j].start / 1001
            
        print()
        return chromosome

    def get_single_sgs_serie(self) -> List[Activity]:
        activitties = gen_act.gen_activities()
        serie = Serie(activitties, False)
        return serie.run()

    def get_sgs_serie(self) -> List[List[Activity]]:
        print('Thread started')
        res : List[List[Activity]] = []
        for i in range(0, 50):
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


    def run_genetic(self):
        print('......')
        self.set_npob()
    


