import Agente
import random

class Finder(Agente): #extends abstract Agente
    #construtor
    def __init__(self, genotype= None): #genotype e o caminho q o agente utiliza
        self.actions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        self.farolFound= False #nao sei se e necessario
        self.fitness= 0
        self.novelty
        self.path= []
        self.steps= 50
        # nao percebi behaviour

        if(genotype != None):
            self.genotype= genotype
        else:
            self.genotype= []
            for i in range(0, self.steps):
                self.genotype.append(random.choice(self.actions))


    def criar(self):
        return Finder()

    def evoluir(self, mundo, currentPos): #neste caso quando e passado e a posicao initial
        self.path.append(currentPos)

        for a in self.genotype: #vai atualizar o genotype
            #nova posicao posicao sendo a antiga + a

            #verificar q a nova e valida

            #get object na possivel nova posicao

            #update coisas

            #adicionar path
            pass

    # #processa observacao?
    # def observacao(self, obs):  # obs da class Observation
    #     pass
    #
    # #avalia o estado atual
    # def avaliacao(self, recompensa):  # recompensa e um double
    #     pass
    #
    # # @Override #diz para nao fazer override mas eu acho q se devia :(
    # def age(self): #para ele fazer move para o farol especificamente
    #     # devolve objeto do tipo accao
    #     pass