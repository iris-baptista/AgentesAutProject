from abc import ABC, abstractmethod

class Agente(ABC): #implements interface aa
    #criar um agente novo
    def criar(self, nomeFicheiro):  # nomeFicheiro do tipo string
        #devolve objeto agente
        pass

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

    #comunica com o agente dado? ou processa a msg recebida?
    def comunica(self, msg, deAgente):  # msg do tipo string, deAgente do tipo Agente
        pass