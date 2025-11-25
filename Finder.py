import Agente
import random

class Finder(Agente): #extends abstract Agente
    actions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    #construtor
    def __init__(self, posInitial): #genotype e o caminho q o agente utiliza, genotype= None
        self.x= posInitial[0]
        self.y= posInitial[1]
        self.found= False
        # self.fitness= 0
        # self.novelty
        # self.path= []
        # self.steps= 50
        # # nao percebi behaviour
        #
        # if(genotype != None):
        #     self.genotype= genotype
        # else:
        #     self.genotype= []
        #     for i in range(0, self.steps):
        #         self.genotype.append(random.choice(self.actions))


    def criar(self, posInitial):
        return Finder(posInitial)

    #@Override #diz para nao fazer override mas eu acho q se devia :(
    def acaoBurro(self): #para ele fazer move para o farol especificamente
        choice= random.choice(self.actions)
        return choice

    def atualizarPosicao(self, pos):
        self.x= pos[0]
        self.y= pos[1]

    # def evoluir(self, mundo):
    #
    #     #self.path.append(currentPos)
    #
    #     # for a in self.genotype: #vai atualizar o genotype
    #         #nova posicao posicao sendo a antiga + a
    #
    #         #verificar q a nova e valida
    #
    #         #get object na possivel nova posicao
    #
    #         #update coisas
    #
    #         #adicionar path
    #         pass

    # #processa observacao?
    # def observacao(self, obs):  # obs da class Observation
    #     pass
    #
    # #avalia o estado atual
    # def avaliacao(self, recompensa):  # recompensa e um double
    #     pass
    #