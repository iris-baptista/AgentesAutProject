from pyparsing import opAssoc

from Agente import Agente
import random
from Ambiente import Obstaculo, LightHouse, EspacoVazio
from Ambiente import EspacoVazio
import Farol
from Coordenator import Coordenator


class Finder(Agente):
    actions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    #construtor
    def __init__(self, posInitial, genotype=None): #genotype e o caminho q o agente utiliza, genotype= None
        self.x= posInitial[0]
        self.y= posInitial[1]
        self.found= False
        self.followed_hints = 0
        self.path= []
        self.total_steps = 0
        self.steps= 200
        self.collisions = 0
        self.behavior = set()
        self.genPolitic = []

        if genotype is None:
            self.genotype = [random.choice(self.actions) for _ in range(self.steps)]
        else:
            self.genotype = genotype

    def getGenotype(self):
        return self.genotype

    def getGenPolitic(self):
        return self.genPolitic

    def setGenPolitic(self, politic):
        self.genPolitic = politic

    def acao(self, action):
        newPos = (action[0] + self.x, action[1] + self.y)

        # so muda de posicao se for uma posicao valida/der para sobrepor!
        tamanho = self.mundoPertence.sizeMap

        if (newPos[0] < tamanho and newPos[0] >= 0 and newPos[1] < tamanho and newPos[1] >= 0):  # dentro do mapa
            obj = self.mundoPertence.getObject(newPos[0], newPos[1])
            match obj:  # pode sobrepor espacos vazios
                case EspacoVazio():
                    self.atualizarPosicao(newPos)
                    # print("Movido para", newPos)
                case LightHouse():
                    self.found = True
                    # print("Encontrou o farol!")
                case _: # nao pode sobrepor agentes ou obstaculos
                    # print("Obstaculo encontrado!")
                    return False, (self.x, self.y)

            return True, newPos
        else:
            # print("Out of Bounds!")
            return False, (self.x, self.y)

    #Fns genetic
    def calculate_objective_fitness(self):
        fitness = 0

        # Bônus principal por encontrar o farol
        if self.found:
            fitness += 1000

        # Explorar novas posições: cada posição única visitada dá pontos
        fitness += 50 * len(self.behavior)

        # Penalização menor por passos e colisões (para não reduzir demais)
        fitness -= 1 * len(self.path)
        fitness -= 10 * self.collisions

        # Seguir dicas do Coordenator
        if self.total_steps > 0:
            fitness += 50 * (self.followed_hints / self.total_steps)

        # Nunca deixar negativo
        return max(fitness, 0)

    def crossover(self, parent1, parent2):
        """Performs single-point crossover on two parent genotypes."""
        point = random.randint(1, len(parent1.genotype) - 1)
        child1_geno = parent1.genotype[:point] + parent2.genotype[point:]
        child2_geno = parent2.genotype[:point] + parent1.genotype[point:]
        return Finder((parent1.x, parent1.y), child1_geno), Finder((parent2.x, parent2.y), child2_geno) # !!incorrect!!!

    def addPolitic(self, topGenotype, worldSize):
        self.genPolitic.append(topGenotype)

        # Ordena a lista pelo fitness objetiva simulada
        self.genPolitic.sort(
            key=lambda g: self.simulate_genotype_fitness(g, worldSize),
            reverse=True
        )

        # Mantém apenas os 10 melhores genótipos
        self.genPolitic = self.genPolitic[:10]

    def simulate_genotype_fitness(self, genotype, worldSize):
        temp_agent = Finder((0, 0), genotype)
        temp_agent.run_simulation(worldSize)
        return temp_agent.calculate_objective_fitness()

    def run_simulation(self, world_size):
        """Runs the agent's genotype in a fresh environment to get its behavior."""
        env = Farol.Farol(world_size)
        coordinator = Coordenator((env.farol.x, env.farol.y))

        # --- Reset all state variables ---
        self.x, self.y = 0, 0
        self.found = False
        self.collisions = 0
        self.path = []
        self.behavior = set()
        self.followed_hints = 0
        self.total_steps = 0

        # Add starting position
        self.behavior.add((self.x, self.y))
        self.path.append((self.x, self.y))

        for action in self.genotype:
            hint = coordinator.toFarol(self.x, self.y)

            if action == hint:
                self.followed_hints += 1
            self.total_steps += 1

            # 1. Get new proposed position
            newx = self.x + action[0]
            newy = self.y + action[1]

            # 2. Check boundaries
            if not (0 <= newx < env.sizeMap and 0 <= newy < env.sizeMap):
                newx, newy = self.x, self.y

            # 3. Check object at new location
            obj = env.getObject(newx,newy)

            # 4. Update agent/env state
            if isinstance(obj, EspacoVazio):
                self.x, self.y = newx, newy
            elif isinstance(obj, Farol.Farol):
                self.x, self.y = newx, newy
                self.found = True
                self.path.append((self.x, self.y))
                self.behavior.add((self.x, self.y))
                break
            else:
                self.collisions += 1

            # 5. Record behavior
            self.behavior.add((self.x, self.y))
            self.path.append((self.x, self.y))
        return

    #Fns Q-Leaning
    def acaoQLearning(self):
        pass

    def nextState(self): # estados representados por o index!
        obs= self.mundoPertence.observacaoPara((self.x, self.y)) #observacao para novo index

        obstaculoCount= self.containsType(obs, Obstaculo)
        farolCount= self.containsType(obs, LightHouse)
        agentCount= self.containsType(obs, Agente)
        if(obstaculoCount >= 1):
            if(farolCount == 1): #so temos um farol em todos os casos
                if(agentCount >=  1):
                    match obs:
                        case [LightHouse(), Agente(), Obstaculo(), EspacoVazio()]:
                            return 117
                        case [LightHouse(), EspacoVazio(), Obstaculo(), Agente()]:
                            return 118
                        case [LightHouse(), Obstaculo(), Agente(), EspacoVazio()]:
                            return 119
                        case [LightHouse(), Obstaculo(), EspacoVazio(), Agente()]:
                            return 120
                        case [LightHouse(), EspacoVazio(), Agente(), Obstaculo()]:
                            return 121
                        case [LightHouse(), Agente(), EspacoVazio(), Obstaculo()]:
                            return 122
                        case [Obstaculo(), EspacoVazio(), Agente(), LightHouse()]:
                            return 123
                        case [Obstaculo(), Agente(), EspacoVazio(), LightHouse()]:
                            return 124
                        case [Agente(), EspacoVazio(), Obstaculo(), LightHouse()]:
                            return 125
                        case [EspacoVazio(), Agente(), Obstaculo(), LightHouse()]:
                            return 126
                        case [Agente(), Obstaculo(), EspacoVazio(), LightHouse()]:
                            return 127
                        case [EspacoVazio(), Obstaculo(), Agente(), LightHouse()]:
                            return 128
                        case [Agente(), LightHouse(), Obstaculo(), EspacoVazio()]:
                            return 129
                        case [EspacoVazio(), LightHouse(), Obstaculo(), Agente()]:
                            return 130
                        case [Obstaculo(), LightHouse(), Agente(), EspacoVazio()]:
                            return 131
                        case [Obstaculo(), LightHouse(), EspacoVazio(), Agente()]:
                            return 132
                        case [EspacoVazio(), LightHouse(), Agente(), Obstaculo()]:
                            return 133
                        case [Agente(), LightHouse(), EspacoVazio(), Obstaculo()]:
                            return 134
                        case [Obstaculo(), EspacoVazio(), LightHouse(), Agente()]:
                            return 135
                        case [Obstaculo(), Agente(), LightHouse(), EspacoVazio()]:
                            return 136
                        case [Agente(), EspacoVazio(), LightHouse(), Obstaculo()]:
                            return 137
                        case [EspacoVazio(), Agente(), LightHouse(), Obstaculo()]:
                            return 138
                        case [Agente(), Obstaculo(), LightHouse(), EspacoVazio()]:
                            return 139
                        case [EspacoVazio(), Obstaculo(), LightHouse(), Agente()]:
                            return 140
                else: #so farol, obstaculo, e espaco vazio
                    if(obstaculoCount == 1):
                        match obs:
                            case [LightHouse(), EspacoVazio(), EspacoVazio(), Obstaculo()]:
                                return 33
                            case [LightHouse(), Obstaculo(), EspacoVazio(), EspacoVazio()]:
                                return 34
                            case [LightHouse(), EspacoVazio(), Obstaculo(), EspacoVazio()]:
                                return 35
                            case [Obstaculo(), EspacoVazio(), EspacoVazio(), LightHouse()]:
                                return 39
                            case [EspacoVazio(), EspacoVazio(), Obstaculo(), LightHouse()]:
                                return 40
                            case [EspacoVazio(), Obstaculo(), EspacoVazio(), LightHouse()]:
                                return 41
                            case [EspacoVazio(), LightHouse(), Obstaculo(), EspacoVazio()]:
                                return 45
                            case [Obstaculo(), LightHouse(), EspacoVazio(), EspacoVazio()]:
                                return 46
                            case [EspacoVazio(), LightHouse(), EspacoVazio(), Obstaculo()]:
                                return 47
                            case [Obstaculo(), EspacoVazio(), LightHouse(), EspacoVazio()]:
                                return 51
                            case [EspacoVazio(), EspacoVazio(), LightHouse(), Obstaculo()]:
                                return 52
                            case [EspacoVazio(), Obstaculo(), LightHouse(), EspacoVazio()]:
                                return 53
                    else: #se for 2
                        match obs:
                            case [LightHouse(), Obstaculo(), Obstaculo(), EspacoVazio()]:
                                return 36
                            case [LightHouse(), Obstaculo(), EspacoVazio(), Obstaculo()]:
                                return 37
                            case [LightHouse(), EspacoVazio(), Obstaculo(), Obstaculo()]:
                                return 38
                            case [EspacoVazio(), Obstaculo(), Obstaculo(), LightHouse()]:
                                return 42
                            case [Obstaculo(), EspacoVazio(), Obstaculo(), LightHouse()]:
                                return 43
                            case [Obstaculo(), Obstaculo(), EspacoVazio(), LightHouse()]:
                                return 44
                            case [Obstaculo(), LightHouse(), Obstaculo(), EspacoVazio()]:
                                return 48
                            case [Obstaculo(), LightHouse(), EspacoVazio(), Obstaculo()]:
                                return 49
                            case [EspacoVazio(), LightHouse(), Obstaculo(), Obstaculo()]:
                                return 50
                            case [EspacoVazio(), Obstaculo(), LightHouse(), Obstaculo()]:
                                return 54
                            case [Obstaculo(), EspacoVazio(), LightHouse(), Obstaculo()]:
                                return 55
                            case [Obstaculo(), Obstaculo(), LightHouse(), EspacoVazio()]:
                                return 56
            elif(agentCount >= 1):
                if(obstaculoCount == 1):
                    if(agentCount == 1):
                        match obs:
                            case [Agente(), EspacoVazio(), EspacoVazio(), Obstaculo()]:
                                return 57
                            case [Agente(), Obstaculo(), EspacoVazio(), EspacoVazio()]:
                                return 58
                            case [Agente(), EspacoVazio(), Obstaculo(), EspacoVazio()]:
                                return 59
                            case [Obstaculo(), EspacoVazio(), EspacoVazio(), Agente()]:
                                return 60
                            case [EspacoVazio(), EspacoVazio(), Obstaculo(), Agente()]:
                                return 61
                            case [EspacoVazio(), Obstaculo(), EspacoVazio(), Agente()]:
                                return 62
                            case [EspacoVazio(), Agente(), Obstaculo(), EspacoVazio()]:
                                return 63
                            case [Obstaculo(), Agente(), EspacoVazio(), EspacoVazio()]:
                                return 64
                            case [EspacoVazio(), Agente(), EspacoVazio(), Obstaculo()]:
                                return 65
                            case [Obstaculo(), EspacoVazio(), Agente(), EspacoVazio()]:
                                return 66
                            case [EspacoVazio(), EspacoVazio(), Agente(), Obstaculo()]:
                                return 67
                            case [EspacoVazio(), Obstaculo(), Agente(), EspacoVazio()]:
                                return 68
                    else: #se for 2 agentes e 1 obstaculo
                        match obs:
                            case [Obstaculo(), Agente(), Agente(), EspacoVazio()]:
                                return 81
                            case [Obstaculo(), Agente(), EspacoVazio(), Agente()]:
                                return 82
                            case [Obstaculo(), EspacoVazio(), Agente(), Agente()]:
                                return 83
                            case [Agente(), EspacoVazio(), Agente(), Obstaculo()]:
                                return 84
                            case [EspacoVazio(), Agente(), Agente(), Obstaculo()]:
                                return 85
                            case [Agente(), Agente(), EspacoVazio(), Obstaculo()]:
                                return 86
                            case [Agente(), Obstaculo(), Agente(), EspacoVazio()]:
                                return 87
                            case [Agente(), Obstaculo(), EspacoVazio(), Agente()]:
                                return 88
                            case [EspacoVazio(), Obstaculo(), Agente(), Agente()]:
                                return 89
                            case [Agente(), EspacoVazio(), Obstaculo(), Agente()]:
                                return 90
                            case [EspacoVazio(), Agente(), Obstaculo(), Agente()]:
                                return 91
                            case [Agente(), Agente(), Obstaculo(), EspacoVazio()]:
                                return 92
                else: #se for 2 obstaculos so pode ser 1 agente
                    match obs:
                        case [Agente(), Obstaculo(), EspacoVazio(), Obstaculo()]:
                            return 69
                        case [Agente(), Obstaculo(), Obstaculo(), EspacoVazio()]:
                            return 70
                        case [Agente(), EspacoVazio(), Obstaculo(), Obstaculo()]:
                            return 71
                        case [Obstaculo(), EspacoVazio(), Obstaculo(), Agente()]:
                            return 72
                        case [EspacoVazio(), Obstaculo(), Obstaculo(), Agente()]:
                            return 73
                        case [Obstaculo(), Obstaculo(), EspacoVazio(), Agente()]:
                            return 74
                        case [Obstaculo(), Agente(), Obstaculo(), EspacoVazio()]:
                            return 75
                        case [Obstaculo(), Agente(), EspacoVazio(), Obstaculo()]:
                            return 76
                        case [EspacoVazio(), Agente(), Obstaculo(), Obstaculo()]:
                            return 77
                        case [Obstaculo(), EspacoVazio(), Agente(), Obstaculo()]:
                            return 78
                        case [EspacoVazio(), Obstaculo(), Agente(), Obstaculo()]:
                            return 79
                        case [Obstaculo(), Obstaculo(), Agente(), EspacoVazio()]:
                            return 80
            else: #so obstaculos e espacos vazios
                if(obstaculoCount == 1):
                    match obs:
                        case [Obstaculo(), EspacoVazio(), EspacoVazio(), EspacoVazio()]:
                            return 1
                        case [EspacoVazio(), Obstaculo(), EspacoVazio(), EspacoVazio()]:
                            return 3
                        case [EspacoVazio(), EspacoVazio(), Obstaculo(), EspacoVazio()]:
                            return 4
                        case [EspacoVazio(), EspacoVazio(), EspacoVazio(), Obstaculo()]:
                            return 2
                elif(obstaculoCount == 2):
                    match obs:
                        case [Obstaculo(), EspacoVazio(), EspacoVazio(), Obstaculo()]:
                            return 5
                        case [EspacoVazio(), Obstaculo(), EspacoVazio(), Obstaculo()]:
                            return 6
                        case [EspacoVazio(), Obstaculo(), Obstaculo(), EspacoVazio()]:
                            return 7
                        case [Obstaculo(), EspacoVazio(), Obstaculo(), EspacoVazio()]:
                            return 8
                        case [Obstaculo(), Obstaculo(), EspacoVazio(), EspacoVazio()]:
                            return 9
                        case [EspacoVazio(), EspacoVazio(), Obstaculo(), Obstaculo()]:
                            return 10
                else: #caso seja 3
                    match obs:
                        case [Obstaculo(), Obstaculo(), EspacoVazio(), Obstaculo()]:
                            return 11
                        case [EspacoVazio(), Obstaculo(), Obstaculo(), Obstaculo()]:
                            return 12
                        case [Obstaculo(), Obstaculo(), Obstaculo(), EspacoVazio()]:
                            return 13
                        case [Obstaculo(), EspacoVazio(), Obstaculo(), Obstaculo()]:
                            return 14
        elif(farolCount == 1):
            if(agentCount >= 1):
                if(agentCount == 1):
                    match obs:
                        case [LightHouse(), EspacoVazio(), EspacoVazio(), Agente()]:
                            return 93
                        case [LightHouse(), Agente(), EspacoVazio(), EspacoVazio()]:
                            return 94
                        case [LightHouse(), EspacoVazio(), Agente(), EspacoVazio()]:
                            return 95
                        case [Agente(), EspacoVazio(), EspacoVazio(), LightHouse()]:
                            return 96
                        case [EspacoVazio(), EspacoVazio(), Agente(), LightHouse()]:
                            return 97
                        case [EspacoVazio(), Agente(), EspacoVazio(), LightHouse()]:
                            return 98
                        case [EspacoVazio(), LightHouse(), EspacoVazio(), Agente()]:
                            return 99
                        case [Agente(), LightHouse(), EspacoVazio(), EspacoVazio()]:
                            return 100
                        case [EspacoVazio(), LightHouse(), Agente(), EspacoVazio()]:
                            return 101
                        case [Agente(), EspacoVazio(), LightHouse(), EspacoVazio()]:
                            return 102
                        case [EspacoVazio(), EspacoVazio(), LightHouse(), Agente()]:
                            return 103
                        case [EspacoVazio(), Agente(), LightHouse(), EspacoVazio()]:
                            return 104
                else: #se for 2s agentes
                    match obs:
                        case [LightHouse(), Agente(), Agente(), EspacoVazio()]:
                            return 105
                        case [LightHouse(), Agente(), EspacoVazio(), Agente()]:
                            return 106
                        case [LightHouse(), EspacoVazio(), Agente(), Agente()]:
                            return 107
                        case [Agente(), EspacoVazio(), Agente(), LightHouse()]:
                            return 108
                        case [EspacoVazio(), Agente(), Agente(), LightHouse()]:
                            return 109
                        case [Agente(), Agente(), EspacoVazio(), LightHouse()]:
                            return 110
                        case [Agente(), LightHouse(), Agente(), EspacoVazio()]:
                            return 111
                        case [Agente(), LightHouse(), EspacoVazio(), Agente()]:
                            return 112
                        case [EspacoVazio(), LightHouse(), Agente(), Agente()]:
                            return 113
                        case [Agente(), EspacoVazio(), LightHouse(), Agente()]:
                            return 114
                        case [EspacoVazio(), Agente(), LightHouse(), Agente()]:
                            return 115
                        case [Agente(), Agente(), LightHouse(), EspacoVazio()]:
                            return 116
            else: #so farol e espaco vazio
                match obs:
                    case [EspacoVazio(), EspacoVazio(), EspacoVazio(), LightHouse()]:
                        return 15
                    case [EspacoVazio(), LightHouse(), EspacoVazio(), EspacoVazio()]:
                        return 16
                    case [EspacoVazio(), EspacoVazio(), LightHouse(), EspacoVazio()]:
                        return 17
                    case [LightHouse(), EspacoVazio(), EspacoVazio(), EspacoVazio()]:
                        return 18
        elif(agentCount >= 1):
            if(agentCount == 1):
                match obs:
                    case [EspacoVazio(), EspacoVazio(), EspacoVazio(), Agente()]:
                        return 19
                    case [EspacoVazio(), Agente(), EspacoVazio(), EspacoVazio()]:
                        return 20
                    case [EspacoVazio(), EspacoVazio(), Agente(), EspacoVazio()]:
                        return 21
                    case [Agente(), EspacoVazio(), EspacoVazio(), EspacoVazio()]:
                        return 22
            elif(agentCount == 2):
                match obs:
                    case [EspacoVazio(), Agente(), EspacoVazio(), Agente()]:
                        return 23
                    case [EspacoVazio(), Agente(), Agente(), EspacoVazio()]:
                        return 24
                    case [Agente(), EspacoVazio(), Agente(), EspacoVazio()]:
                        return 25
                    case [Agente(), EspacoVazio(), EspacoVazio(), Agente()]:
                        return 26
                    case [EspacoVazio(), EspacoVazio(), Agente(), Agente()]:
                        return 27
                    case [Agente(), Agente(), EspacoVazio(), EspacoVazio()]:
                        return 28
            else: #se for 3
                match obs:
                    case [EspacoVazio(), Agente(), Agente(), Agente()]:
                        return 29
                    case [Agente(), Agente(), Agente(), EspacoVazio()]:
                        return 30
                    case [Agente(), EspacoVazio(), Agente(), Agente()]:
                        return 31
                    case [Agente(), Agente(), EspacoVazio(), Agente()]:
                        return 32
        else: #so espacos vazios
            return 0

    def inGoal(self, nextState):
        if (nextState >= 15 and nextState <= 18):
            return True
        elif (nextState >= 33 and nextState <= 56):
            return True
        elif (nextState >= 93):
            return True
        else:
            return False