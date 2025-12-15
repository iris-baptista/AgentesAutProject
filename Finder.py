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
        # self.fitness= 0
        # self.novelty
        self.path= []
        self.steps= 50
        self.collisions = 0
        self.behavior = set()
        self.genPolitic = []

        if genotype is None:
            self.genotype = [random.choice(self.actions) for _ in range(self.steps)]
        else:
            self.genotype = genotype

    def getGenotype(self):
        return self.genotype

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
                    return False

            return True
        else:
            # print("Out of Bounds!")
            return False

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
    def nextState(self): # estados representados por o index!
        obs= self.mundoPertence.observacaoPara((self.x, self.y)) #observacao para novo index
        if(self.containsType(obs, Obstaculo)):
            if(self.containsType(obs, LightHouse)):
                if(self.containsType(obs, Agente)):
                    return 7
                else: #so farol, obstaculo, e espaco vazio
                    return 4
            elif(self.containsType(obs, Agente)):
                return 5
            else: #so obstaculos e espacos vazios
                return 1
        elif(self.containsType(obs, LightHouse)):
            if(self.containsType(obs, Agente)):
                return 6
            else: #so farol e espaco vazio
                return 2
        elif(self.containsType(obs, Agente)):
            return 3
        else: #so espacos vazios
            return 0