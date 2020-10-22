from typing import List
from models import actividad


class SerieSGS:
    activities: List[Actividad]

    def __init__(self, activities:List[Actividad]):
        self.activities = activities

    def schedule_activities():
        print('Schudeling activities')

    def sort_activities():
        print('############ Activities ordered by its starting time ##########')
        activities.sort(key=operator.attrgetter('start'))