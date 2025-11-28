from Agente import Agente

class Dropper(Agente):
    recursosParaDepositar= []
    totalDepositado= 0

    #construtor
    def __init__(self, posInitial):
        self.x= posInitial[0]
        self.y= posInitial[1]

    #vai pedir recursos ao forager
    def getRecursos(self):
        pass

    #depositar todos os recursos q pode
    def depositRecursos(self):
        self.getRecursos() #necessario?

        for r in self.recursosParaDepositar:
            self.totalDepositado+= 1
            print("Depositou o recurso ", r.name)

        self.recursosParaDepositar= []

    def acaoBurro(self):
        pass

    def run_simulation(self):
        pass