from abc import ABC, abstractmethod
import random

class Agente(ABC):
    actions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    mundoPertence= None
    qTable = None #sera por isto?

    def acaoBurro(self):
        choice = random.choice(self.actions)
        return choice

    @abstractmethod
    def acao(self, action):
        pass

    @abstractmethod
    def run_simulation(self, world_size):
        pass

    def atualizarPosicao(self, pos):
        self.x= pos[0]
        self.y= pos[1]

    @abstractmethod
    def calculate_objective_fitness(self):
        pass

    def crossover(self, parent1, parent2):
        pass

    def mutate(self, mutation_rate):
        """Randomly changes some actions in the genotype."""
        for i in range(len(self.genotype)):
            if random.random() < mutation_rate:
                self.genotype[i] = random.choice(self.actions)

    def select_parent(population, tournament_size):
        """Selects a parent using tournament selection based on *combined_fitness*."""
        # must select the same number of different agents in population
        tournament = random.sample(population, tournament_size)
        tournament.sort(key=lambda x: x.combined_fitness, reverse=True)
        return tournament[0], tournament[1]

    # --- Q Learning ---
    def setMundo(self, m):
        self.mundoPertence= m

    @abstractmethod
    def nextState(self, estado, acao):
        pass

    def containsType(self, list, type):
        for item in list:
            if isinstance(item, type):
                return True

        return False