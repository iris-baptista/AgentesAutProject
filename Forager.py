from Agente import Agente
import random

class Forager(Agente): #extends abstract Agente
    actions = [(0, 1), (1, 0), (0, -1), (-1, 0)] #pode ir para o agente abstrato

    #construtor
    def __init__(self, posInitial):
        self.x= posInitial[0]
        self.y= posInitial[1]
        self.points= 0 #initializar pontos
        self.recursosCollected= [] #comeca sem nada

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

    def run_simulation(self):
        pass