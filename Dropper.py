import random

from Agente import Agente

class Dropper(Agente):


    #construtor
    def __init__(self, posInitial):
        self.x= posInitial[0]
        self.y= posInitial[1]

        self.behavior = set()
        self.recursosParaDepositar = []
        self.pontosDepositados = 0

    #vai pedir recursos ao forager
    def getRecursos(self):
        pass

    #depositar todos os recursos q pode
    def depositRecursos(self):
        self.getRecursos() #necessario?

        for r in self.recursosParaDepositar:
            self.pontosDepositados+= r.pontos
            print("Depositou o recurso ", r.name, "que valia ", r.pontos, " pontos!")

        self.recursosParaDepositar= []

    def acaoBurro(self):
        pass

    def calculate_objective_fitness(self):
        """Calculates the agent's goal-oriented fitness score."""
        recursos_reward = len(self.recursosParaDepositar) * 100
        depositados_reward = self.pontosDepositados * 500
        exploration_reward = len(self.behavior) * 1
        return recursos_reward + depositados_reward + exploration_reward

    def crossover(self, parent1, parent2):
        """Performs single-point crossover on two parent genotypes."""
        point = random.randint(1, len(parent1.genotype) - 1)
        child1_geno = parent1.genotype[:point] + parent2.genotype[point:]
        child2_geno = parent2.genotype[:point] + parent1.genotype[point:]
        return Dropper(child1_geno), Dropper(child2_geno)

    def run_simulation(self, world_size):
        pass