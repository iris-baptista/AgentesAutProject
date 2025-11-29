from Agente import Agente
import numpy as np
import time

class Dropper(Agente):
    recursosParaDepositar= []
    pontosDepositados= 0

    #construtor
    def __init__(self, posInitial):
        self.x= posInitial[0]
        self.y= posInitial[1]

    #vai pedir recursos ao forager
    def getRecursos(self):
        pass

    #depositar todos os recursos q pode
    def depositRecursos(self):
        self.getRecursos() #necessario?

        for r in self.recursosParaDepositar:
            self.pontosDepositados+= r.pontos
            print("Depositou o recurso ", r.name, "que valia ", r.pontos, " ponto(s)!")

        self.recursosParaDepositar= []

    def acaoBurro(self):
        pass

    def run_simulation(self):
        pass

    # fns q learning
    def qLearning(self, goal, QTable, probExplorar, numEstados, numAcoes):
        learningRate = 0.7  # demais? a menos? #% de info nova
        recompensa = 0.7  # demais? a menos? #valor atribuido ao proximo estado (?)
        numEpisodios = 1000  # muito?

        for episodio in range(numEpisodios):  # deviamos comecar sempre no mesmo estado?
            # escolhe um estado aleatoriamente
            currentState = np.random.randint(0, numEstados)  # estados representados por o index!

            initialTime = time.time()
            while (True):
                # escolher se vamos explorar ou aproveitar
                if (np.random.rand() <= probExplorar):
                    action = np.random.randint(0, numAcoes)  # usar uma action nova/aleatoria
                else:
                    action = np.argmax(QTable[currentState])  # usar um maximo conhecido

                nextState = self.nextState(currentState, action)

                if (nextState in goal):  # goal e lista de estados q tem fruta
                    reward = 1  # reward podia ser o valor do recurso mas nao sei como aceder aqui XD
                else:
                    reward = 0

                # atualizar matriz DOUBLE CHECK FIM BC I DONT TRUST
                QTable[currentState, action] = (
                        ((1 - learningRate) * QTable[currentState, action]) +
                        (learningRate * (reward + recompensa * np.max(QTable[nextState]))))

                if (time.time() - initialTime == 0.5):  # para depois do tempo acabar #como e q tenho acesso ao tempo ;(
                    break

                currentState = nextState
                # diminuir probabilidade de explorar?

        # queremos ver a tabela visualmente depois dos episodios?

    def nextState(self, estado, acao):  # estado vai ser o mundo? ou o index
        pass