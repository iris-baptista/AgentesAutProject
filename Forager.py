from Agente import Agente
from Ambiente import EspacoVazio, Recurso, Obstaculo, Cesto
import random

class Forager(Agente): #extends abstract Agente
    actions = [(0, 1), (1, 0), (0, -1), (-1, 0)] #pode ir para o agente abstrato

    #construtor
    def __init__(self, posInitial):
        self.x= posInitial[0]
        self.y= posInitial[1]
        self.points= 0 #initializar pontos (somente para o modelo burro)
        self.recursosCollected= [] #comeca sem nada
        self.behavior = set()

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
                    return False, (self.x, self.y)

            return True, newPos
        else:
            # print("Out of Bounds!")
            return False, (self.x, self.y)

    #fns genetic
    def calculate_objective_fitness(self):
        recursos_reward = len(self.recursosCollected) * 100
        exploration_reward = len(self.behavior) * 1
        return recursos_reward + exploration_reward

    def crossover(self, parent1, parent2):
        point = random.randint(1, len(parent1.genotype) - 1)
        child1_geno = parent1.genotype[:point] + parent2.genotype[point:]
        child2_geno = parent2.genotype[:point] + parent1.genotype[point:]
        return Forager(child1_geno), Forager(child2_geno)

    def run_simulation(self):
        pass

    #fns q learning
    def acaoQLearning(self):
        pass

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