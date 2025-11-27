import random
from Ambiente import Obstaculo, EspacoVazio, Cesto, Recurso
from Forager import Forager
from Dropper import Dropper

class Foraging: #ambiente
    #tem atributes sizeMap, obstaculos, cestos, recursos, e agentes

    #okay tb devia ter as posicoes q queria q eles comecarem...
    #ver do ficheiro
    #ter uma atribute para o tempo a correr
    def __init__(self, sizeMundo, dificuldade= 0.3, posObstaculos= None, posCestos= None, posRecursos= None, numForagers= 1, numDroppers= 0, tempo= 5): #queremos indicar as posicoes do farol ou do mapa?
        self.sizeMap= sizeMundo
        self.tempo= tempo #tempo default e 30 segs i guess
        takenPos= []

        # adicionar obstaculos
        if (posObstaculos == None):  # se nao for dado, posicao aleatoria escolhida
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

        self.obstaculos = []
        for o in posObstaculos:
            self.obstaculos.append(Obstaculo(o[0], o[1]))

        #adicionar cestos
        if(posCestos == None): #se nao for dado, posicao aleatoria escolhida
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

        self.cestos = []
        index= 1
        for c in posCestos:
            self.cestos.append(Cesto(f"C{index}", c[0], c[1]))
            index+= 1

        #adicionar recursos
        if(posRecursos == None): #se nao for dado, posicao aleatoria escolhida
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

        self.recursos = []
        index = 1
        for r in posRecursos:
            self.recursos.append(Recurso(f"R{index}", r[0], r[1]))
            index += 1

        self.agentes = []
        for i in range(0, numForagers):
            while (True):  # check position not taken
                foragerPos = (random.randint(0, sizeMundo - 1), random.randint(0, sizeMundo - 1))

                if (foragerPos not in takenPos):
                    break

            takenPos.append(foragerPos)
            self.agentes.append(Forager(foragerPos))

        for j in range(0, numDroppers):
            while (True):  # check position not taken
                dropperPos = (random.randint(0, sizeMundo - 1), random.randint(0, sizeMundo - 1))

                if (dropperPos not in takenPos):
                    break

            takenPos.append(dropperPos)
            self.agentes.append(Dropper(dropperPos))

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
                #print("Foi contra um obstaculo...")
                return o

        return EspacoVazio(x, y) #se nao encontrou um obstaculo ou um farol segue (ignora q pode ser outro agente...)

    def getAgentes(self):
        return self.agentes

    def removeRecurso(self, r):
        self.recursos.remove(r)

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