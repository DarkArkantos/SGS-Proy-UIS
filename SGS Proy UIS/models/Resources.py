class Resources():
    PL:int
    QA:int
    DE:int
    def __init__(self, PL, QA, DE):
        self.PL=PL
        self.QA=QA
        self.DE=DE

    def __modify_resources(self, resource, sign:int):
        self.DE+=resource.DE*sign
        self.QA+=resource.QA*sign
        self.PL+=resource.PL*sign

    def check_enough_resources(self, act_resources):
        """Verifica si hay suficientes recursos para programar una actividad"""
        return (self.DE>=act_resources.DE)and(self.PL>=act_resources.DE)and(self.QA>=act_resources.QA)

    def reduce_resources(self,resource):
        self.__modify_resources(resource, -1)

    def add_resources(self, resource):
        self.__modify_resources(resource, 1)

    