from Agente import Agente
from Ambiente import EspacoVazio, Recurso, Obstaculo, Cesto


class Forager(Agente): #extends abstract Agente
    #construtor
    def __init__(self, posInitial):
        self.x= posInitial[0]
        self.y= posInitial[1]
        #self.points= 0 #initializar pontos
        self.recursosCollected= [] #comeca sem nada

    #adicionar um recurso encontrado ao inventario
    def collectRecurso(self, r):
        self.recursosCollected.append(r)

    #manda recursos a um agente dropper para ser depositado
    def sendRecursos(self):
        toSend= self.recursosCollected
        self.recursosCollected= [] #empty out inventory

        return toSend

    def acao(self, action):
        newPos = (action[0] + self.x, action[1] + self.y)

        # so muda de posicao se for uma posicao valida/der para sobrepor!
        tamanho = self.mundoPertence.sizeMap
        if (newPos[0] < tamanho and newPos[0] >= 0 and newPos[1] < tamanho and newPos[1] >= 0):  # dentro do mapa
            obj = self.mundoPertence.getObject(newPos[0], newPos[1])
            match obj:  # pode sobrepor espacos vazios e recursos
                case EspacoVazio():
                    self.atualizarPosicao(newPos)
                    # print("Movido para", newPos)
                case Recurso():
                    self.collectRecurso(obj)
                    self.atualizarPosicao(newPos)
                    self.mundoPertence.removeRecurso(obj)
                case _:  # nao pode sobrepor agentes ou obstaculos ou cestos
                    # print("Obstaculo encontrado!")
                    return False

            return True
        else:
            # print("Out of Bounds!")
            return False

    #fns genetic
    def run_simulation(self):
        pass

    #fns q learning
    def nextState(self):  # estado vai ser o mundo? ou o index
        obs = self.mundoPertence.observacaoPara((self.x, self.y))  # observacao para novo index
        if (self.containsType(obs, Obstaculo)):
            if (self.containsType(obs, Recurso)):
                if (self.containsType(obs, Cesto)):
                    return 11
                elif (self.containsType(obs, Agente)):
                    return 12
                else:
                    return 5
            elif (self.containsType(obs, Agente)):
                return 6
            elif (self.containsType(obs, Cesto)):
                if (self.containsType(obs, Agente)):
                    return 14
                else:
                    return 7
            else:
                return 1
        elif (self.containsType(obs, Recurso)):
            if (self.containsType(obs, Cesto)):
                if(self.containsType(obs, Agente)):
                    return 13
                else:
                    return 8
            elif (self.containsType(obs, Agente)):
                return 9
            else:
                return 2
        elif (self.containsType(obs, Agente)):
            if (self.containsType(obs, Cesto)):
                return 10
            else:
                return 3
        elif (self.containsType(obs, Cesto)):
            return 4
        else:  # so espacos vazios
            return 0