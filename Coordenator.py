from Agente import Agente

class Coordenator(Agente):
    farol= (0, 0)

    # construtor
    def __init__(self, posInitial):
        self.x= posInitial[0]
        self.y= posInitial[1]

    #devolve proxima coord na direcao do farol para o agente
    def toFarol(self): #devia passar agente no parametro?
        pass

    def acaoBurro(self):
        pass

    def calculate_objective_fitness(self):
        pass

    def run_simulation(self, world_size):
        pass