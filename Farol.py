import random
from Ambiente import Obstaculo, EspacoVazio, LightHouse
from Finder import Finder
from Coordenator import Coordenator

class Farol: #foraging
    # tem atributes sizeMap, obstaculos, farol, e agentes!

    def __init__(self, sizeMundo, dificuldade= 0.3, posFarol= None, posObstaculos= None, numFinders= 1, numCoords= 0): #queremos indicar as posicoes do farol ou do mapa?
        self.sizeMap= sizeMundo
        takenPos= [] #nao e uma atribute, so para facilitar esta parte das definicoes

        #adicionar farol
        if(posFarol == None): #se nao for dado, posicao aleatoria escolhida
            while(True):
                x= random.randint(0, sizeMundo-1)
                y= random.randint(0, sizeMundo-1)

                if((x, y) not in takenPos):
                    break

            posFarol= (x, y)

        takenPos.append(posFarol) #mind you not checking if the posGiven is available
        self.farol= LightHouse("F", posFarol[0], posFarol[1])

        #adicionar obstaculos
        if(posObstaculos == None): #se nao for dado, posicao aleatoria escolhida
            numToGenerate= (int) ((sizeMundo * sizeMundo) * dificuldade) #fazer baseado numa percentagem
            posObstaculos= []

            for i in range(0, numToGenerate):
                while(True):
                    x= random.randint(0, sizeMundo-1)
                    y= random.randint(0, sizeMundo-1)

                    if((x,y) not in takenPos):
                        break

                takenPos.append((x, y))
                posObstaculos.append((x, y))

        self.obstaculos= []
        for o in posObstaculos:
            self.obstaculos.append(Obstaculo(o[0], o[1]))

        self.agentes = []
        for i in range(0, numFinders):
            while (True):  # check position not taken
                finderPos = (random.randint(0, sizeMundo - 1), random.randint(0, sizeMundo - 1))

                if (finderPos not in takenPos):
                    break

            takenPos.append(finderPos)
            self.agentes.append(Finder(finderPos))

        for j in range(0, numCoords):
            while (True):  # check position not taken
                coordPos = (random.randint(0, sizeMundo - 1), random.randint(0, sizeMundo - 1))

                if (coordPos not in takenPos):
                    break

            takenPos.append(coordPos)
            self.agentes.append(Coordenator(coordPos))

    #devolve objeto na posicao dada
    def getObject(self, x, y):
        if x == self.farol.x and y == self.farol.y:
            # print("Encontrou o farol!")
            return self.farol

        for o in self.obstaculos:
            if x == o.x and y == o.y:
                # print("Foi contra um obstaculo...")
                return o

        return EspacoVazio(x, y) #se nao encontrou um obstaculo ou um farol segue (ignora q pode ser outro agente...)

    def getAgentes(self):
        return self.agentes

    #observacao para mandar ao agente dado?
    # def observacaoPara(self, agente): #agente do tipo Agente
    #     #devolve objeto do tipo Observation
    #     pass
    # #
    # #atualiza ambiente(mapa)
    # def atualizar(self):
    #     pass

    #movimenta o agente/faz a sua accao?
    # def agir(self, accao, agente): #accao do tipo accao, agente do tipo Agente
    #     pass