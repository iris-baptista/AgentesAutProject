from abc import ABC, abstractmethod
import random
import matplotlib.pyplot as plt
import numpy as np


class Agente(ABC):
    actions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    mundoPertence= None
    qTable = []

    def acaoBurro(self):
        choice = random.choice(self.actions)

        return choice

    @abstractmethod
    def acao(self, action):
        pass

    def atualizarPosicao(self, pos):
        self.x= pos[0]
        self.y= pos[1]

    # --- Genetic Algorithm ---
    @abstractmethod
    def run_simulation(self):
        pass

    def calculate_objective_fitness(self): #pode ser abstrato???
        """Calculates the agent's goal-oriented fitness score."""
        key_reward = len(self.keys_found) * 100
        treasure_reward = len(self.treasures_opened) * 500
        exploration_reward = len(self.behavior) * 1

        return key_reward + treasure_reward + exploration_reward

    def crossover(self, parent1, parent2):
        """Performs single-point crossover on two parent genotypes."""
        point = random.randint(1, len(parent1.genotype) - 1)
        child1_geno = parent1.genotype[:point] + parent2.genotype[point:]
        child2_geno = parent2.genotype[:point] + parent1.genotype[point:]
        return Agente(child1_geno), Agente(child2_geno) #nao deixa fazer import a Finder por q cria um loop

    def mutate(self, mutation_rate):
        """Randomly changes some actions in the genotype."""
        for i in range(len(self.genotype)):
            if random.random() < mutation_rate:
                self.genotype[i] = random.choice(self.actions)

    def select_parent(self, population, tournament_size):
        """Selects a parent using tournament selection based on *combined_fitness*."""
        tournament = random.sample(population, tournament_size)
        tournament.sort(key=lambda x: x.combined_fitness, reverse=True)
        return tournament[0]

    # --- Q Learning ---
    def setMundo(self, m):
        self.mundoPertence= m

    @abstractmethod
    def qLearning(self, goal, QTable, probExplorar, numEstados, numAcoes):  # rede neuronal onde?
        pass

    @abstractmethod
    def nextState(self, estado, acao):
        pass

    def containsType(self, list, type):
        for item in list:
            if isinstance(item, type):
                return True

        return False

    def showGraph(self):
        plt.figure(figsize=(6, 6))
        plt.title('Q-Values')

        plt.imshow(self.qTable, 'magma', interpolation='nearest')  #Spectral, magma, plasma, YlOrRd, RdBu, PiYG
        plt.xticks(np.arange(4), ['Up', 'Right', 'Down', 'Left'])
        plt.xlabel('Action')
        plt.yticks(np.arange(8), ['0', '1', '2', '3', '4', '5', '6', '7'])
        plt.ylabel('Estado')
        plt.gca().invert_yaxis()

        for i in range(8):
            for j in range(4):
                value = self.qTable[i][j]
                if (value <= np.max(self.qTable) / 2):
                    plt.text(j, i, f'{value:.2f}', ha='center', va='center', color='white')
                else:
                    plt.text(j, i, f'{value:.2f}', ha='center', va='center', color='black')

        plt.colorbar()
        plt.show()
