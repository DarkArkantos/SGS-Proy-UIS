import numpy.random as rand


dic = {
        1: 0,
        2: round(rand.normal(1, 0.9)),
        3: round(rand.normal(4, 0.4)),
        4: round(rand.normal(2, 0.2)),
        5: round(rand.normal(1, 0.1)),
        6: round(rand.normal(1, 0.1)),
        7: round(rand.normal(6, 0.6)),
        8: round(rand.normal(2, 0.2)),
        9: round(rand.normal(16, 1.6)),
        10: round(rand.normal(2, 0.2)),
        11: round(rand.normal(2, 0.2)),
        12: round(rand.normal(6, 0.6)),
        13: round(rand.normal(4, 0.4)),
        14: round(rand.normal(1, 0.1)),
        15: round(rand.normal(1, 0.1)),
        16: round(rand.normal(8, 0.8)),
        17: round(rand.normal(12, 1.2)),
        18: round(rand.normal(10, 1)),
        19: round(rand.normal(10, 1)),
        20: round(rand.normal(10, 1)),
        21: round(rand.normal(8, 0.8)),
        22: round(rand.normal(1, 0.1)),
        23: round(rand.normal(4, 0.4)),
        24: round(rand.normal(8, 0.8)),
        25: round(rand.normal(2, 0.2)),
        26: round(rand.normal(4, 0.4)),
        27: round(rand.normal(8, 0.8)),
        28: 0
        }


def get_random_duration(index: int):
    if(index==28 or index==1):
        return 0
    return (rand.beta(a= 11.0/20.0, b= 28.0/8.0)*5)+2

"""ddfd
    dic = {
            1: 0,
            2: round(rand.normal(1, 1.0)),
            3: round(rand.normal(4, 0.4)),
            4: round(rand.normal(2, 0.2)),
            5: round(rand.normal(1, 0.1)),
            6: round(rand.normal(1, 0.1)),
            7: round(rand.normal(6, 0.6)),
            8: round(rand.normal(2, 0.2)),
            9: round(rand.normal(16, 1.6)),
            10: round(rand.normal(2, 0.2)),
            11: round(rand.normal(2, 0.2)),
            12: round(rand.normal(6, 0.6)),
            13: round(rand.normal(4, 0.4)),
            14: round(rand.normal(1, 0.1)),
            15: round(rand.normal(1, 0.1)),
            16: round(rand.normal(8, 0.8)),
            17: round(rand.normal(12, 1.2)),
            18: round(rand.normal(10, 1)),
            19: round(rand.normal(10, 1)),
            20: round(rand.normal(10, 1)),
            21: round(rand.normal(8, 0.8)),
            22: round(rand.normal(1, 0.1)),
            23: round(rand.normal(4, 0.4)),
            24: round(rand.normal(8, 0.8)),
            25: round(rand.normal(2, 0.2)),
            26: round(rand.normal(4, 0.4)),
            27: round(rand.normal(8, 0.8)),
            28: 0
            }
"""