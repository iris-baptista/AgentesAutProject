from Ambiente import Obstaculo, EspacoVazio, LightHouse
from Finder import Finder
from Coordenator import Coordenator
import random

class Farol: #foraging
    # tem atributes sizeMap, obstaculos, farol, agentes, e a posicao initial dos agentes!

    def __init__(self, sizeMundo): #nao passei o nome do ficheiro ja q e sempre o mesmo para o farol
        self.sizeMap = sizeMundo
        self.obstaculos = []
        self.agentes = []
        self.ogPosAgentes = []
        self.genPolitic = []
        takenPos = [] #nao e uma atribute, so para facilitar esta parte das definicoes

        file= open("config_farol1.txt", "r") #comecar leitura de configuracoes
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
                        if(self.createsBlock(posObstaculos, x, y) == False): # verificar q nao cria bloqueios
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

        for o in posObstaculos:
            self.obstaculos.append(Obstaculo(o[0], o[1]))

        numFinders= int(((file.readline()).split("=")[1]).split("\n")[0])
        posFinders= ((file.readline()).split("=")[1]).split("\n")[0]
        for i in range(0, numFinders):
            if(posFinders == "None"):
                while (True):  # check position not taken
                    finderPos = (random.randint(0, sizeMundo - 1), random.randint(0, sizeMundo - 1))

                    if (finderPos not in takenPos):
                        break

                takenPos.append(finderPos)
                self.ogPosAgentes.append(finderPos)
                self.agentes.append(Finder(finderPos))

            else: #no formato [(num,num),(num,num)...]
                toConvert = posFinders[2:-2].split("),(")
                for toC in toConvert:
                    numbers = toC.split(",")
                    finderPos= (int(numbers[0]), int(numbers[1]))

                    takenPos.append(finderPos)
                    self.ogPosAgentes.append(finderPos)
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
                self.ogPosAgentes.append(coordPos)
                self.agentes.append(Coordenator(coordPos))

            else: #no formato [(num,num),(num,num)...]
                toConvert = posCoords[2:-2].split("),(")
                for toC in toConvert:
                    numbers = toC.split(",")
                    coordPos= (int(numbers[0]), int(numbers[1]))

                    takenPos.append(coordPos)
                    self.ogPosAgentes.append(coordPos)
                    self.agentes.append(Coordenator(coordPos))

        file.close()

    def setGenPolitic(self, politic):
        self.genPolitic = politic

    def createsBlock(self, posObstaculos, x, y):
        # print("Obstaculos ", posObstaculos)
        surroundingActions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, 1), (1, -1), (-1, 1)]  # 8 espacos a volta
        connectedActions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        possibleGrupos = []
        for s in surroundingActions:
            coord = (s[0] + x, s[1] + y)

            if (coord[0] >= 0 and coord[0] < self.sizeMap and coord[1] < self.sizeMap and coord[1] >= 0):  # para so ser validos!
                if ((coord not in posObstaculos) and (type(self.getObject(coord[0], coord[1])) != LightHouse)): #encontrar espacos vazios ao lado da posicao nova
                    possibleGrupos.append(coord)

        gruposFound = []
        for g in possibleGrupos: #encontrar grupos de espacos vazios
            grupo = [g]
            for member in grupo:
                for s in connectedActions:
                    coord = (s[0] + member[0], s[1] + member[1])

                    if (coord[0] < self.sizeMap and coord[0] >= 0 and coord[1] < self.sizeMap and coord[1] >= 0): #coordenada valida
                        if (type(self.getObject(coord[0], coord[1])) != LightHouse): #nao e o farol
                            if ((coord not in posObstaculos) and (coord not in grupo) and (coord != (x, y))): #novo espaco vazio
                                grupo.append(coord)

            gruposFound.append(grupo)
            if (len(grupo) != len(gruposFound[0])):  # se o atual for diferente do primeiro grupo esta
                return True

        return False  # se nada esta surrounded

    def getObject(self, x, y):  #devolve objeto na posicao dada
        if x == self.farol.x and y == self.farol.y:
            return self.farol

        for o in self.obstaculos:
            if x == o.x and y == o.y:
                return o

        for a in self.agentes:
            if x == a.x and y == a.y:
                return a

        return EspacoVazio(x, y) #se nao encontrou um obstaculo ou um farol segue

    def getAgentes(self):
        return self.agentes

    def getOGPosAgentes(self):
        return self.ogPosAgentes

    #observacao para mandar a posicao dada
    def observacaoPara(self, pos): #devolve array com objetos a volta do agente
        above= self.getObject(pos[0], pos[1]+1)
        bellow= self.getObject(pos[0], pos[1]-1)
        left= self.getObject(pos[0]-1, pos[1])
        right= self.getObject(pos[0]+1, pos[1])

        return [above, bellow, left, right]

    def resetMundo(self):
        for i in range(0, len(self.getAgentes())):
            a= self.getAgentes()[i]
            a.atualizarPosicao(self.ogPosAgentes[i])
            a.setGenPolitic(self.genPolitic)
            a.found= False
            a.followed_hints = 0
            a.path= []
            a.total_steps = 0
            a.steps= 200
            a.collisions = 0

    def resetStart(self): #vai por os agentes em posicoes aleatorias para comecar
        for a in self.getAgentes():
            while (True):  # check position not taken
                newFinderPos = (random.randint(0, self.sizeMap - 1), random.randint(0, self.sizeMap - 1))

                if (type(self.getObject(newFinderPos[0], newFinderPos[1])) == EspacoVazio):
                    break

            a.atualizarPosicao(newFinderPos)