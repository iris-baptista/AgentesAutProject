import Agente

class AForaging(Agente): #extends abstract Agente
    recursosCollected= [] #lista Coord

    #construtor
    def __init__(self, nomeFicheiro):
        # acho q isto esta mal
        return super().criar(nomeFicheiro)

    #processa observacao?
    def observacao(self, obs):  # obs da class Observation
        pass

    #avalia o estado atual
    def avaliacao(self, recompensa):  # recompensa e um double
        pass

    #adicionar um recurso encontrado ao inventario
    def addRecurso(self, r):
        self.recursosCollected.append(r)

    #manda recursos a um agente dropper para ser depositado
    def sendRecursos(self):
        toSend= self.recursosCollected
        self.recursosCollected= []

        #acho q vai haver algo de msgs aqui
        return toSend

