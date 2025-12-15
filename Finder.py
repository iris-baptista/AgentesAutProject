from Agente import Agente
import random
from Ambiente import EspacoVazio
import Farol

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
        self.behavior= set()

        if genotype is None:
            self.genotype = [random.choice(self.actions) for _ in range(self.steps)]
        else:
            self.genotype = genotype

    def acaoBurro(self): #para ele fazer move para o farol especificamente
        choice= random.choice(self.actions)

        return choice

    def calculate_objective_fitness(self):
        # recompensar mais por menos passos
        return len(self.behavior) * 1

    def crossover(self, parent1, parent2):
        """Performs single-point crossover on two parent genotypes."""
        point = random.randint(1, len(parent1.genotype) - 1)
        child1_geno = parent1.genotype[:point] + parent2.genotype[point:]
        child2_geno = parent2.genotype[:point] + parent1.genotype[point:]
        return Finder((parent1.x, parent1.y), child1_geno), Finder((parent2.x, parent2.y), child2_geno) # !!incorrect!!!

    def run_simulation(self, world_size):
        """Runs the agent's genotype in a fresh environment to get its behavior."""
        env = Farol.Farol(world_size)

        # --- Reset all state variables ---
        self.behavior = set()
        self.path = []
        self.found = False

        # Add starting position
        self.behavior.add((self.x, self.y))
        self.path.append((self.x, self.y))

        for action in self.genotype:
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
                self.found = True
            else:
                pass

            # 5. Record behavior
            self.behavior.add((self.x, self.y))
            self.path.append((self.x, self.y))