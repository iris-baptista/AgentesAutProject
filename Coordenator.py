import Agente

class Coordenator(Agente):
    farol= (0, 0)

    # construtor
    def __init__(self, nomeFicheiro):
        # acho q isto esta mal
        return super().criar(nomeFicheiro)

    # processa observacao?
    def observacao(self, obs):  # obs da class Observation
        pass

    # avalia o estado atual
    def avaliacao(self, recompensa):  # recompensa e um double
        pass

    #devolve proxima coord na direcao do farol para o agente
    def toFarol(self): #devia passar agente no parametro?
        pass

    # def getPosicaoAgente(self):
    #     pass