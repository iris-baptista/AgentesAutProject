import random
from Ambiente import Obstaculo, EspacoVazio, Cesto, Recurso

class Foraging: #ambiente
    #tem atributes sizeMap, obstaculos, cestos, e recursos

    def __init__(self, sizeMundo, dificuldade= 0.3, posObstaculos= None, posCestos= None, posRecursos= None): #queremos indicar as posicoes do farol ou do mapa?
        self.sizeMap= sizeMundo

        # adicionar obstaculos
        if (posObstaculos == None):  # se nao for dado, posicao aleatoria escolhida
            numToGenerate = (int) (sizeMundo * sizeMundo) * dificuldade  # fazer baseado numa percentagem
            posObstaculos = []
            for i in range(0, numToGenerate):
                x = random.randint(0, sizeMundo - 1)
                y = random.randint(0, sizeMundo - 1)
                posObstaculos.append((x, y))

        self.obstaculos = []
        for o in posObstaculos:
            self.obstaculos.append(Obstaculo(o[0], o[1]))

        #adicionar cestos
        if(posCestos == None): #se nao for dado, posicao aleatoria escolhida
            numToGenerate = (int) (sizeMundo * sizeMundo) * 0.1  # fazer baseado numa percentagem
            posCestos = []
            for i in range(0, numToGenerate):
                x = random.randint(0, sizeMundo - 1)
                y = random.randint(0, sizeMundo - 1)
                posCestos.append((x, y))

        self.cestos = []
        index= 1
        for c in posCestos:
            self.cestos.append(Cesto(f"C{index}", c[0], c[1]))
            index+= 1

        #adicionar recursos
        if(posRecursos == None): #se nao for dado, posicao aleatoria escolhida
            numToGenerate = (int) (sizeMundo * sizeMundo) * 0.2  # fazer baseado numa percentagem
            posRecursos = []
            for i in range(0, numToGenerate):
                x = random.randint(0, sizeMundo - 1)
                y = random.randint(0, sizeMundo - 1)
                posRecursos.append((x, y))

        self.recursos = []
        index = 1
        for r in posRecursos:
            self.recursos.append(Recurso(f"R{index}", r[0], r[1]))
            index += 1

    #devolve objeto na posicao dada
    def getObject(self, x, y):
        for c in self.cestos:
            if x == c.x and y == c.y:
                #print(f"Encontrou o cesto {c.name}")
                return c

        for r in self.recursos:
            if x == r.x and y == r.y:
                #print(f"Encontrou o recurso {r.name}")
                return r

        for o in self.obstaculos:
            if x == o.x and y == o.y:
                print("Foi contra um obstaculo...")
                return o

        return EspacoVazio(x, y) #se nao encontrou um obstaculo ou um farol segue (ignora q pode ser outro agente...)


    # #observacao para mandar ao agente dado?
    # def observacaoPara(self, agente): #agente do tipo Agente
    #     #devolve objeto do tipo Observation
    #     pass
    #
    # #atualiza ambiente
    # def atualizar(self):
    #     pass
    #
    # #movimenta o agente/faz a sua accao?
    # def agir(self, accao, agente): #accao do tipo accao, agente do tipo Agente
    #     pass