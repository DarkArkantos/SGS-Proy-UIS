from typing import List


class Resources():
    resources: List[int]
    def __init__(self, resources: List[int]):
        self.resources = resources

    def __modify_resources(self, resource: List[int], sign:int):
        for index in range(len(self.resources)):
            self.resources[index]+= resource[index] * sign

    def check_enough_resources(self, act_resources: List[int]) -> bool:
        """Verifica si hay suficientes recursos para programar una actividad"""
        result: bool = True
        for index in range(len(self.resources)):
            result &= self.resources[index]>=act_resources[index]
        return result

    def reduce_resources(self,resource):
        self.__modify_resources(resource, -1)

    def add_resources(self, resource):
        self.__modify_resources(resource, 1)

    