from Agente import Agente

class Coordenator(Agente):
    farol= (0, 0)

    # construtor
    def __init__(self, posInitial):
        self.x= posInitial[0]
        self.y= posInitial[1]

    #devolve direcao do farol para o agente
    def toFarol(self): #devia passar agente no parametro?
        pass

    #coordenador does not move
    def acaoBurro(self):
        pass

    def acao(self, action):
        pass

    # Fns genetic (coordenador is not trained!)
    def run_simulation(self):
        pass

    # Fns Q-Leaning (coordenador is not trained!)
    def acaoQLearning(self):
        pass

    def nextState(self):
        pass