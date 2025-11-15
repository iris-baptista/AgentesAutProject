import Agente

class Finder(Agente): #extends abstract Agente
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

    # @Override #diz para nao fazer override mas eu acho q se devia :(
    def age(self): #para ele fazer move para o farol especificamente
        # devolve objeto do tipo accao
        pass