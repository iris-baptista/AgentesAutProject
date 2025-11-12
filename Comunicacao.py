from abc import ABC, abstractmethod

class Comunicacao(ABC):
    @abstractmethod
    def enviarAgente(self, msg, agente): #msg do tipo string, agente do tipo Agente
        pass

    @abstractmethod
    def enviarAmbiente(self, msg, ambiente): #msg to tipo string, ambiente do tipo Ambiente
        pass