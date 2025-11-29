from Agente import Agente
import numpy as np

class Coordenator(Agente):
    farol= (0, 0)

    # construtor
    def __init__(self, posInitial):
        self.x= posInitial[0]
        self.y= posInitial[1]

    #devolve proxima coord na direcao do farol para o agente
    def toFarol(self): #devia passar agente no parametro?
        pass

    def acaoBurro(self):
        pass

    def run_simulation(self):
        pass

    # Fns Q-Leaning
    def qLearning(self, goal, QTable, probExplorar, numEstados, numAcoes):  # rede neuronal onde?
        learningRate = 0.7  # demais? a menos? #% de info nova
        recompensa = 0.7  # demais? a menos? #valor atribuido ao proximo estado (?)
        numEpisodios = 1000  # muito?

        for episodio in range(numEpisodios):  # deviamos comecar sempre no mesmo estado?
            # escolhe um estado aleatoriamente
            currentState = np.random.randint(0, numEstados)  # estados representados por o index!

            while (True):
                # escolher se vamos explorar ou aproveitar
                if (np.random.rand() <= probExplorar):
                    action = np.random.randint(0, numAcoes)  # usar uma action nova/aleatoria
                else:
                    action = np.argmax(QTable[currentState])  # usar um maximo conhecido

                nextState = self.nextState(currentState, action)

                if (nextState == goal): #ele nao se mexe... not sure how to do this?
                    reward = 1
                else:  # ter um elif para se for um obstaculo?
                    reward = 0

                # atualizar matriz DOUBLE CHECK FIM BC I DONT TRUST
                QTable[currentState, action] = (
                        ((1 - learningRate) * QTable[currentState, action]) +
                        (learningRate * (reward + recompensa * np.max(QTable[nextState]))))

                if (nextState == goal):  # para quando encontra farol
                    break

                currentState = nextState
                # diminuir probabilidade de explorar?

        # queremos ver a tabela visualmente depois dos episodios?

    def nextState(self, estado, acao):  # estado vai ser o mundo? ou o index
        pass