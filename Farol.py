import random

class LightHouse:
    def __init__(self, name, x, y):
        self.name= name
        self.x= x
        self.y= y

class Obstaculo:
    def __init__(self, x, y):
        self.x= x
        self.y= y

class EspacoVazio:
    def __init__(self, x, y):
        self.x= x
        self.y= y

class Farol: #foraging
    # tem atributes sizeMap, obstaculos, e farol

    def __init__(self, sizeMundo, dificuldade= 0.3, posFarol= None, posObstaculos= None): #queremos indicar as posicoes do farol ou do mapa?
        self.sizeMap= sizeMundo

        #adicionar farol
        if(posFarol == None): #se nao for dado, posicao aleatoria escolhida
            x= random.randint(0, sizeMundo-1)
            y= random.randint(0, sizeMundo-1)
            posFarol= (x, y)

        self.farol= LightHouse("F", posFarol[0], posFarol[1])

        #adicionar obstaculos
        if(posObstaculos == None): #se nao for dado, posicao aleatoria escolhida
            numToGenerate= (sizeMundo * sizeMundo) * dificuldade #fazer baseado numa percentagem
            posObstaculos= []
            for i in range(0, numToGenerate):
                x= random.randint(0, sizeMundo-1)
                y= random.randint(0, sizeMundo-1)
                posObstaculos.append((x, y))

        self.obstaculos= []
        for o in posObstaculos:
            self.obstaculos.append(Obstaculo(o[0], o[1]))

    #devolve objeto na posicao dada
    def getObject(self, x, y):
        if x == self.farol.x and y == self.farol.y:
            print("Encontrou o farol!")
            return self.farol

        for o in self.obstaculos:
            if x == o.x and y == o.y:
                print("Foi contra um obstaculo...")
                return o

        return EspacoVazio(x, y) #se nao encontrou um obstaculo ou um farol segue (ignora q pode ser outro agente...)

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