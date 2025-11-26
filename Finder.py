import Agente
import random

class Finder(Agente): #extends abstract Agente
    #construtor
    def __init__(self, genotype= None): #genotype e o caminho q o agente utiliza
        self.actions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        self.steps = 50
        self.farolFound= False
        self.fitness= 0
        self.novelty
        self.path= []
        self.behavior = set()

        if(genotype != None):
            self.genotype= genotype
        else:
            self.genotype= []
            for i in range(0, self.steps):
                self.genotype.append(random.choice(self.actions))


    def criar(self):
        return Finder()

    def evoluir(self, mundo, currentPos): #neste caso quando e passado e a posicao initial
        self.path.append(currentPos)

        for a in self.genotype: #vai atualizar o genotype
            #nova posicao posicao sendo a antiga + a

            #verificar q a nova e valida

            #get object na possivel nova posicao

            #update coisas

            #adicionar path
            pass

    # #processa observacao?
    # def observacao(self, obs):  # obs da class Observation
    #     pass
    #
    # #avalia o estado atual
    # def avaliacao(self, recompensa):  # recompensa e um double
    #     pass
    #
    # # @Override #diz para nao fazer override mas eu acho q se devia :(
    # def age(self): #para ele fazer move para o farol especificamente
    #     # devolve objeto do tipo accao
    #     pass


    # --- Genetic Algorithm ---
    def calculate_objective_fitness(self):
        """Calculates the agent's goal-oriented fitness score."""
        key_reward = len(self.keys_found) * 100
        treasure_reward = len(self.treasures_opened) * 500
        exploration_reward = len(self.behavior) * 1

        return key_reward + treasure_reward + exploration_reward

    def crossover(parent1, parent2):
        """Performs single-point crossover on two parent genotypes."""
        point = random.randint(1, len(parent1.genotype) - 1)
        child1_geno = parent1.genotype[:point] + parent2.genotype[point:]
        child2_geno = parent2.genotype[:point] + parent1.genotype[point:]
        return Finder(child1_geno), Finder(child2_geno)

    def mutate(self, mutation_rate):
        """Randomly changes some actions in the genotype."""
        for i in range(len(self.genotype)):
            if random.random() < mutation_rate:
                self.genotype[i] = random.choice(self.actions)

    def select_parent(population, tournament_size):
        """Selects a parent using tournament selection based on *combined_fitness*."""
        tournament = random.sample(population, tournament_size)
        tournament.sort(key=lambda x: x.combined_fitness, reverse=True)
        return tournament[0]

    def run_simulation(self):
        """Runs the agent's genotype in a fresh environment to get its behavior."""
        env = Farol()

        # --- Reset all state variables ---
        self.behavior = set()
        self.path = []
        self.farolFound = False

        # Add starting position
        self.behavior.add((env.agentx, env.agenty))
        self.path.append((env.agentx, env.agenty))

        # We need to track the keys *this agent* has for this run
        local_found_keys = []

        for action in self.genotype:
            # 1. Get new proposed position
            newx = env.agentx + action[0]
            newy = env.agenty + action[1]

            # 2. Check boundaries
            if not (0 <= newx < env.size and 0 <= newy < env.size):
                newx, newy = env.agentx, env.agenty

            # 3. Check object at new location
            obj = env.get_object_here(newx, newy)

            # 4. Update agent/env state
            if isinstance(obj, Ground):
                env.agentx, env.agenty = newx, newy
            elif isinstance(obj, Key):
                env.keys.remove(obj)
                local_found_keys.append(obj)
                self.keys_found.append(obj)
                env.agentx, env.agenty = newx, newy
            elif isinstance(obj, Treasure):
                for key in local_found_keys:
                    if key.treasure == obj.name:
                        obj.opened = True
                        env.treasures.remove(obj)
                        self.treasures_opened.append(obj)
                        env.agentx, env.agenty = newx, newy

            # 5. Record behavior
            self.behavior.add((env.agentx, env.agenty))
            self.path.append((env.agentx, env.agenty))