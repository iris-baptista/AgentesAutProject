from abc import ABC, abstractmethod
import random

class Agente(ABC):
    #criar um agente novo
    # @abstractmethod
    # def criar(self, posInitial):  #nao se tem de usar ficheiro, mais tarde se quiseremos podemos ir ver
    #     pass

    @abstractmethod
    def observacao(self, obs):  # obs da class Observation
        pass

    #devolve accao q o agente vai fazer
    def age(self):
        #devolve objeto do tipo accao
        pass

    @abstractmethod
    def avaliacao(self, recompensa):  # recompensa e um double
        pass

    #???
    def instala(self, sensor):  # sensor da class Sensor
        pass

    #comunica com o agente dado
    def comunica(self, msg, recetor):  # msg do tipo string, recetior do tipo Agente
        pass