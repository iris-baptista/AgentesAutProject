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

    def atualizarPosicao(self, pos):
        self.x= pos[0]
        self.y= pos[1]

    # --- Algoritmo Genetico ---
    @abstractmethod
    def run_simulation(self, world_size):
        pass

    @abstractmethod
    def calculate_objective_fitness(self):
        pass

    def mutate(self, mutation_rate):
        if random.random() < mutation_rate:
            start = random.randint(0, len(self.genotype) - 1)
            length = random.randint(2, 6)

            for i in range(start, min(start + length, len(self.genotype))):
                current = self.genotype[i]
                self.genotype[i] = random.choice(
                    [a for a in self.actions if a != current]
                )

    def select_parent(population, tournament_size):
        """Selects a parent using tournament selection based on *combined_fitness*."""
        # must select the same number of different agents in population
        tournament = random.sample(population, tournament_size)
        tournament.sort(key=lambda x: x.combined_fitness, reverse=True)
        return tournament[0], tournament[1]

    # --- Q Learning ---
    def setMundo(self, m):
        self.mundoPertence= m

    # @abstractmethod
    # def acaoQLearning(self):
    #     pass

    @abstractmethod
    def nextState(self):
        pass

    @abstractmethod
    def inGoal(self, nextState):
        pass

    def containsType(self, list, type):
        itemCount= 0
        for item in list:
            if isinstance(item, type):
                itemCount+= 1

        return itemCount