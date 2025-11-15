import Agente

class Dropper(Agente):
    recursosParaDepositar= []
    totalDepositado= 0

    #construtor
    def __init__(self, nomeFicheiro):
        #acho q isto esta mal
        return super().criar(nomeFicheiro)

    #processa observacao?
    def observacao(self, obs):  # obs da class Observation
        pass

    #avalia o estado atual
    def avaliacao(self, recompensa):  # recompensa e um double
        pass

    #vai pedir recursos ao forager
    def getRecursos(self):
        pass

    #depositar todos os recursos q pode
    def depositRecursos(self):
        self.getRecursos() #necessario?

        for r in self.recursosParaDepositar:
            self.totalDepositado+= 1

        self.recursosParaDepositar= []