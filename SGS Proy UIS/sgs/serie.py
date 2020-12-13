from typing import List
from models.activity import Activity
from sgs.base_model import BaseModel
import utils.randtime as random_time
import utils.print as prnt
from models.Resources import Resources
import numpy.random as rand
import numpy as num


class Serie(BaseModel):

    def __init__(self, activities:List[Activity], with_logs:bool = True):
        resources = Resources(10,10,5)
        super(Serie, self).__init__(activities, resources, with_logs)

    def schedule_activities(self):
        current_time = 0
        if self.with_logs: print('Scheduling activities')
        self.init_first_activity()
        
        all_scheduled: bool = False

        while not all_scheduled:
            actives = [act for act in self.activities if act.active]
            ## Completes all the activities that has been completed so far and set free the resources
            if(len(actives) > 0):
                [self.complete_activity(act) for act in actives if act.end <= current_time]

            all_scheduled = self.check_all_scheduled()
            completed = [act for act in self.activities if act.completed]

            ## Prints the completed activities so far.
            if self.with_logs:
                print(f'Current time: {current_time}')
                print('####  Activities Completed: ####')
                prnt.print_activities(completed)

            ## Evaluate elegible activities
            eleg = self.get_elegible_activities()
            max_end = 0
            while len(eleg)>0:

                ## Prints the current resources and the elegible activities
                if self.with_logs:
                    self.print_resources()
                    prnt.print_activities(eleg)

                # Schedule activities until there aren't any elegible.
                index = self.select_activities(eleg, current_time)
                end = self.schedule_activity(eleg[index], current_time)
                if(end>max_end):
                    max_end=end
            
                for act in eleg:
                    act.eleg = False

                eleg = self.get_elegible_activities()
        
            current_time = max_end
            


    def select_activities(self, activities: List[Activity], current_time:int):
        probs : List[int] = []

        ## Asigns a temporal ending to determine the probabilty.

        for act in activities:
            act.end = current_time + act.duration

        sum = self.sum_lft(activities)
        ## Sets the end time of the activity
        for act in activities:
            prob = act.end / sum
            probs.append(prob)
        
        ## The index of the activity is chosen.
        random_value = rand.random_sample()
        
        index = probs.index(num.max(probs))
        for i in range(0, len(probs)):
            if(random_value<=probs[i]):
                index=i

        if self.with_logs:
            ## Probability of being chosen Pj = LFTj/(sum(LFTj1+LFTjn)
            print('\nProbabilities of being chosen: ')
            print(probs)
            print(f'\nRandom number: {random_value}')
            print(f'\nChosen index: {index}')
        
        return index


    def check_all_scheduled(self):
        value: bool = True
        for act in self.activities:
            value&=act.completed
            if not value:
                return False
        return value


    def schedule_activity(self, act:Activity, currentTime:int):
        # Se reducen los recursos disponibles
        self.resources.reduce_resources(act.resources)
        act.reset_activity()
        act.active=True
        ## TODO Create a partial object that records the starttime
        act.start = currentTime
        return act.end

    def sum_lft(self, activities: List[Activity]):
        """Calculates the sum of the LFT"""
        sum = 0
        for a in activities:
            sum += a.end
        return sum

    def set_activities(self):
        for act in self.activities:
            act.duration = random_time.get_random_duration(act.index)
        self.print_activities()

    def run(self) -> List[Activity]:
        """Executes a SGS model and returns the List of Activities scheduled"""
        if self.with_logs: print('Running Serie SGS')
        # Sorts the activities
        self.sort_activities('index')
        self.set_activities()
        self.schedule_activities()
        [act.reset_activity() for act in self.activities]
        return self.activities