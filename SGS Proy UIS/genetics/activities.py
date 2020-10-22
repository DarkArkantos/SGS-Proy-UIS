from typing import List

# Models
from models.activity import Activity
from models.Resources import Resources

# Utilities
import utils.randtime as rand
import utils.print as prt

def gen_activities() -> List[Activity] :
    activities: List[Activity] =[]
     #                        Index Strt Prio Prece         Recursos              Activo Coplet Elegi  end
    activities.append(Activity(1,  0,  0, [0],           Resources(0,0,0),     False, False, False, 0))
    activities.append(Activity(2,  0,  0, [1],           Resources(5,0,0),     False, False, False, 0))
    activities.append(Activity(3,  0,  0, [1],           Resources(0,0,5),     False, False, False, 0))
    activities.append(Activity(4,  4,  0, [1],           Resources(2,0,5),     False, False, False, 0))
    activities.append(Activity(5,  6,  0, [2,3,4],       Resources(8,0,0),     False, False, False, 0))
    activities.append(Activity(6,  7,  0, [5],           Resources(5,0,0),     False, False, False, 0))
    activities.append(Activity(7,  0,  0, [1],           Resources(4,0,0),     False, False, False, 0))
    activities.append(Activity(8,  8,  0, [6,7],         Resources(0,0,0),     False, False, False, 0))
    activities.append(Activity(9,  10, 0, [8],           Resources(0,0,0),     False, False, False, 0))
    activities.append(Activity(10, 28, 0, [9],           Resources(0,10,0),    False, False, False, 0))
    activities.append(Activity(11, 30, 0, [9],           Resources(0,10,0),    False, False, False, 0))
    activities.append(Activity(12, 32, 0, [9],           Resources(0,0,0),     False, False, False, 0))
    activities.append(Activity(13, 33, 0, [10,11],       Resources(0,0,0),     False, False, False, 0))
    activities.append(Activity(14, 39, 0, [12,13],       Resources(0,0,0),     False, False, False, 0))
    activities.append(Activity(15, 41, 0, [14],          Resources(10,0,0),    False, False, False, 0))
    activities.append(Activity(16, 42, 0, [15],          Resources(0,0,0),     False, False, False, 0))
    activities.append(Activity(17, 42, 0, [15],          Resources(0,0,0),     False, False, False, 0))
    activities.append(Activity(18, 54, 0, [17],          Resources(0,0,0),     False, False, False, 0))
    activities.append(Activity(19, 42, 0, [15],          Resources(0,0,0),     False, False, False, 0))
    activities.append(Activity(20, 42, 0, [15],          Resources(0,0,0),     False, False, False, 0))
    activities.append(Activity(21, 52, 0, [20],          Resources(0,0,0),     False, False, False, 0))
    activities.append(Activity(22, 60, 0, [16,18,19,21], Resources(5,0,0),     False, False, False, 0))
    activities.append(Activity(23, 58, 0, [15],          Resources(5,0,0),     False, False, False, 0))
    activities.append(Activity(24, 56, 0, [15],          Resources(0,10,0),    False, False, False, 0))
    activities.append(Activity(25, 64, 0, [22,24,23],    Resources(10,0,0),    False, False, False, 0))
    activities.append(Activity(26, 66, 0, [25],          Resources(0,0,0),     False, False, False, 0))
    activities.append(Activity(27, 70, 0, [26],          Resources(2,0,0),     False, False, False, 0))
    activities.append(Activity(28, 90, 0, [27],          Resources(0,0,0),     False, False, False, 0))
    print('############   Actividades a usar:  ##############')
    prt.print_activities(activities)

    return activities

