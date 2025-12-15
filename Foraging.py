from Ambiente import Obstaculo, EspacoVazio, Cesto, Recurso
from Forager import Forager
from Dropper import Dropper
import random

class Foraging: #ambiente
    #tem atributes sizeMap, obstaculos, cestos, recursos, agentes, posicao initial dos agentes, recursosOriginais e tempo a correr

    def __init__(self, sizeMundo):
        self.sizeMap= sizeMundo
        takenPos= []

        file= open("config_foraging.txt", "r")
        dificuldade = float((file.readline()).split("=")[1])

        posObstaculos = ((file.readline()).split("=")[1]).split("\n")[0]  # adicionar obstaculos
        if (posObstaculos == "None"):  # se nao for dado, posicao aleatoria escolhida
            numToGenerate = (int) ((sizeMundo * sizeMundo) * dificuldade)  # fazer baseado numa percentagem
            posObstaculos = []
            for i in range(0, numToGenerate):
                while(True):
                    x = random.randint(0, sizeMundo - 1)
                    y = random.randint(0, sizeMundo - 1)

                    if((x, y) not in takenPos):
                        break

                takenPos.append((x, y))
                posObstaculos.append((x, y))

        else:
            posObstaculos = []

            toConvert = posObstaculos[2:-2].split("),(")
            for toC in toConvert:
                numbers = toC.split(",")
                x = int(numbers[0])
                y = int(numbers[1])

                takenPos.append((x, y))
                posObstaculos.append((x, y))

        self.obstaculos = []
        for o in posObstaculos:
            self.obstaculos.append(Obstaculo(o[0], o[1]))

        posCestos = ((file.readline()).split("=")[1]).split("\n")[0]  #adicionar cestos
        if(posCestos == "None"): #se nao for dado, posicao aleatoria escolhida
            numToGenerate = (int) ((sizeMundo * sizeMundo) * 0.1)  # fazer baseado numa percentagem
            posCestos = []
            for i in range(0, numToGenerate):
                while(True):
                    x = random.randint(0, sizeMundo - 1)
                    y = random.randint(0, sizeMundo - 1)

                    if((x, y) not in takenPos):
                        break

                takenPos.append((x, y))
                posCestos.append((x, y))

        else:
            posCestos = []

            toConvert = posCestos[2:-2].split("),(")
            for toC in toConvert:
                numbers = toC.split(",")
                x = int(numbers[0])
                y = int(numbers[1])

                takenPos.append((x, y))
                posCestos.append((x, y))

        self.cestos = []
        index= 1
        for c in posCestos:
            self.cestos.append(Cesto(f"C{index}", c[0], c[1]))
            index+= 1

        posRecursos = ((file.readline()).split("=")[1]).split("\n")[0] #adicionar recursos
        if(posRecursos == "None"): #se nao for dado, posicao aleatoria escolhida
            numToGenerate = (int) ((sizeMundo * sizeMundo) * 0.2)  # fazer baseado numa percentagem
            posRecursos = []
            for i in range(0, numToGenerate):
                while(True):
                    x = random.randint(0, sizeMundo - 1)
                    y = random.randint(0, sizeMundo - 1)

                    if((x, y) not in takenPos):
                        break

                takenPos.append((x, y))
                posRecursos.append((x, y))

        else:
            posRecursos = []

            toConvert = posCestos[2:-2].split("),(")
            for toC in toConvert:
                numbers = toC.split(",")
                x = int(numbers[0])
                y = int(numbers[1])

                takenPos.append((x, y))
                posRecursos.append((x, y))

        self.recursos = []
        self.ogRecursos = []
        index = 1
        for r in posRecursos:
            novoRecurso= Recurso(f"R{index}", r[0], r[1])
            self.recursos.append(novoRecurso)
            self.ogRecursos.append(novoRecurso)
            index += 1

        self.agentes = []
        self.ogPosAgentes = []
        numForagers = int(((file.readline()).split("=")[1]).split("\n")[0])
        posForagers = ((file.readline()).split("=")[1]).split("\n")[0]
        foragers= []
        for i in range(0, numForagers):
            if(posForagers == "None"):
                while (True):  # check position not taken
                    foragerPos = (random.randint(0, sizeMundo - 1), random.randint(0, sizeMundo - 1))

                    if (foragerPos not in takenPos):
                        break

                takenPos.append(foragerPos)
                self.ogPosAgentes.append(foragerPos)
                newForager= Forager(foragerPos)
                self.agentes.append(newForager)
                foragers.append(newForager)
            else:
                toConvert = posForagers[2:-2].split("),(")
                for toC in toConvert:
                    numbers = toC.split(",")
                    foragerPos = (int(numbers[0]), int(numbers[1]))

                    takenPos.append(foragerPos)
                    self.ogPosAgentes.append(foragerPos)
                    newForager = Forager(foragerPos)
                    self.agentes.append(newForager)
                    foragers.append(newForager)

        numDroppers = int(((file.readline()).split("=")[1]).split("\n")[0])
        posDroppers = ((file.readline()).split("=")[1]).split("\n")[0]
        for j in range(0, numDroppers):
            if(posDroppers == "None"):
                while (True):  # check position not taken
                    dropperPos = (random.randint(0, sizeMundo - 1), random.randint(0, sizeMundo - 1))

                    if (dropperPos not in takenPos):
                        break

                takenPos.append(dropperPos)
                self.ogPosAgentes.append(dropperPos)
                self.agentes.append(Dropper(dropperPos, foragers))
            else:
                toConvert = posDroppers[2:-2].split("),(")
                for toC in toConvert:
                    numbers = toC.split(",")
                    dropperPos = (int(numbers[0]), int(numbers[1]))

                    takenPos.append(dropperPos)
                    self.ogPosAgentes.append(dropperPos)
                    self.agentes.append(Dropper(dropperPos, foragers))

        self.tempo= float(((file.readline()).split("=")[1]).split("\n")[0])
        file.close()

    #devolve objeto na posicao dada
    def getObject(self, x, y):
        for a in self.agentes: #agente primeiro para sobrepor recursos (get rid of?)
            if x == a.x and y == a.y:
                return a
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
                #print("Foi contra um obstaculo...")
                return o

        return EspacoVazio(x, y) #se nao encontrou um obstaculo ou um farol segue (ignora q pode ser outro agente...)

    def getAgentes(self):
        return self.agentes

    def getOGPosAgentes(self):
        return self.ogPosAgentes

    def removeRecurso(self, r):
        self.recursos.remove(r)

    # observacao para mandar a posicao dada (valores dos sensores da posicao dada)
    def observacaoPara(self, pos):  # devolve array com objetos a volta do agente
        above = self.getObject(pos[0], pos[1] + 1)
        bellow = self.getObject(pos[0], pos[1] - 1)
        left = self.getObject(pos[0] - 1, pos[1])
        right = self.getObject(pos[0] + 1, pos[1])

        return [above, bellow, left, right]

    def resetMundo(self):
        for i in range(0, len(self.getAgentes())):
            a= self.getAgentes()[i]
            a.atualizarPosicao(self.ogPosAgentes[i])

            #resetting atributes
            if(type(a) == Forager):
                a.recursosCollected= []
            else:
                a.pontosDepositados= 0

        self.recursos = self.ogRecursos.copy()

    def resetStart(self): #vai por os agentes em posicoes aleatorias para comecar
        for a in self.getAgentes():
            while (True):  # check position not taken
                newPos = (random.randint(0, self.sizeMap - 1), random.randint(0, self.sizeMap - 1))

                if (type(self.getObject(newPos[0], newPos[1])) == EspacoVazio):
                    break

            a.atualizarPosicao(newPos)