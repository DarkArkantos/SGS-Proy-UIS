from typing import List
from models.activity import Activity
from sgs.base_model import BaseModel
import utils.randtime as rand
from models.Resources import Resources


class Serie(BaseModel):

    def __init__(self, activities:List[Activity]):
        resources = Resources(10,10,5)
        super(Serie, self).__init__(activities, resources)

    def schedule_activities(self):
        current_time = 0
        next_step = 1
        print('Schudeling activities')
        self.init_first_activity()
        

        actives = [act for act in self.activities if act.active]

        if(len(actives) > 0):
            [act.complete_activity() for act in actives if act.end < next_step]


        self.print_activities()
        ## Evaluate elegible activities
        eleg = self.get_elegible_activities()
        # Schedule activities until there aren't any elegible.
        self.select_activities(eleg, current_time)


    def select_activities(self, activities: List[Activity], current_time:int):
        probs : List[int] = []
        sum = self.sum_lft(activities)
        ## Sets the end time of the activity
        for act in activities:
            act.end = current_time + act.duration
            # TODO: End must be asign before, or the division will resutl in 0.
            prob = act.end / sum
            probs.append(prob)
        ## Probability of being chosen Pj = LFTj/(sum(LFTj1+LFTjn)
        print(probs)

    def sum_lft(self, activities: List[Activity]):
        """Calculates the sum of the LFT"""
        sum = 0
        for a in activities:
            sum += a.end
        return sum

    def set_activities(self):
        for act in self.activities:
            act.duration = rand.get_random_duration(act.index)
        self.print_activities()

    def run(self):
        print('Running Serie SGS')
        # Sorts the activities
        self.sort_activities('index')
        self.set_activities()
        self.schedule_activities()