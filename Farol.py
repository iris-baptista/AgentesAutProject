from Ambiente import Obstaculo, EspacoVazio, LightHouse
from Finder import Finder
from Coordenator import Coordenator
import random

class Farol: #foraging
    # tem atributes sizeMap, obstaculos, farol, e agentes!

    def __init__(self, sizeMundo): #nao passei o nome do ficheiro ja q e sempre o mesmo para o farol
        self.sizeMap = sizeMundo
        takenPos = [] #nao e uma atribute, so para facilitar esta parte das definicoes

        file= open("config_farol.txt", "r") #comecar leitura de configuracoes
        dificuldade= float((file.readline()).split("=")[1])

        posFarol= ((file.readline()).split("=")[1]).split("\n")[0] #"(0,0)" or "None"
        if (posFarol == "None"): #se nao for dado, posicao aleatoria escolhida
            done= False
            while (done == False):
                x = random.randint(0, sizeMundo - 1)
                y = random.randint(0, sizeMundo - 1)

                if ((x, y) not in takenPos):
                    done= True

            posFarol = (x, y)
        else: #se no formato (num,num)
            converting= posFarol[1:-1].split(",")
            posFarol= (int(converting[0]),int(converting[1]))

        takenPos.append(posFarol)  # mind you not checking if the posGiven is available
        self.farol = LightHouse("F", posFarol[0], posFarol[1])

        posObstaculos = ((file.readline()).split("=")[1]).split("\n")[0] #adicionar obstaculos
        if (posObstaculos == "None"):  # se nao for dado, posicao aleatoria escolhida
            numToGenerate = (int)((sizeMundo * sizeMundo) * dificuldade)  # fazer baseado numa percentagem
            posObstaculos = []

            for i in range(0, numToGenerate):
                while (True):
                    x = random.randint(0, sizeMundo - 1)
                    y = random.randint(0, sizeMundo - 1)

                    if ((x, y) not in takenPos):
                        break

                takenPos.append((x, y))
                posObstaculos.append((x, y))

        else: #formato [(num,num),(num,num)...]
            posObstaculos = []

            toConvert= posObstaculos[2:-2].split("),(")
            for toC in toConvert:
                numbers= toC.split(",")
                x= int(numbers[0])
                y= int(numbers[1])

                takenPos.append((x, y))
                posObstaculos.append((x, y))

        self.obstaculos = []
        for o in posObstaculos:
            self.obstaculos.append(Obstaculo(o[0], o[1]))

        numFinders= int(((file.readline()).split("=")[1]).split("\n")[0])
        posFinders= ((file.readline()).split("=")[1]).split("\n")[0]
        self.agentes = []
        for i in range(0, numFinders):
            if(posFinders == "None"):
                while (True):  # check position not taken
                    finderPos = (random.randint(0, sizeMundo - 1), random.randint(0, sizeMundo - 1))

                    if (finderPos not in takenPos):
                        break

                takenPos.append(finderPos)
                self.agentes.append(Finder(finderPos))

            else: #no formato [(num,num),(num,num)...]
                toConvert = posFinders[2:-2].split("),(")
                for toC in toConvert:
                    numbers = toC.split(",")
                    finderPos= (int(numbers[0]), int(numbers[1]))

                    takenPos.append(finderPos)
                    self.agentes.append(Finder(finderPos))

        numCoords= int(((file.readline()).split("=")[1]).split("\n")[0])
        posCoords= ((file.readline()).split("=")[1]).split("\n")[0]
        for j in range(0, numCoords):
            if(posCoords == "None"):
                while (True):  # check position not taken
                    coordPos = (random.randint(0, sizeMundo - 1), random.randint(0, sizeMundo - 1))

                    if (coordPos not in takenPos):
                        break

                takenPos.append(coordPos)
                self.agentes.append(Coordenator(coordPos))

            else: #no formato [(num,num),(num,num)...]
                toConvert = posCoords[2:-2].split("),(")
                for toC in toConvert:
                    numbers = toC.split(",")
                    coordPos= (int(numbers[0]), int(numbers[1]))

                    takenPos.append(coordPos)
                    self.agentes.append(Coordenator(coordPos))

        file.close()

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