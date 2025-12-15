from Agente import Agente
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

        #acho q vai haver algo de msgs aqui
        return toSend

    def acaoBurro(self): #isto pode ser no abstrato tb
        choice= random.choice(self.actions)

        return choice

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