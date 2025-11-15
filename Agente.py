from abc import ABC, abstractmethod

class Agente(ABC):
    posicao= (0, 0) #posicao vai ser alterada, isto e so para instanciar

    #criar um agente novo
    #deve ser abstractmethod???
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