from Agente import Agente
import numpy as np
import time
from Ambiente import EspacoVazio, Cesto

class Dropper(Agente):
    pontosDepositados= 0

    #construtor
    def __init__(self, posInitial, foragers):
        self.x= posInitial[0]
        self.y= posInitial[1]
        self.qTable= []
        self.foragers= foragers
        self.pontosDepositados= 0

    #vai pedir recursos ao forager
    def getRecursos(self):
        recursosParaDepositar = []
        for friend in self.foragers:
            recursosCollected= friend.sendRecursos()
            for recurso in recursosCollected:
                recursosParaDepositar.append(recurso)

        return recursosParaDepositar

    #depositar todos os recursos q pode
    def depositRecursos(self):
        recursosParaDepositar= self.getRecursos()

        totalDeposited= 0
        for r in recursosParaDepositar:
            totalDeposited += r.pontos
            print("Depositou o recurso ", r.name, "que valia ", r.pontos, " ponto(s)!")

        self.pontosDepositados += totalDeposited
        return totalDeposited

    def acao(self, action):
        newPos = (action[0] + self.x, action[1] + self.y)

        # so muda de posicao se for uma posicao valida/der para sobrepor!
        tamanho = self.mundoPertence.sizeMap
        if (newPos[0] < tamanho and newPos[0] >= 0 and newPos[1] < tamanho and newPos[1] >= 0):  # dentro do mapa
            obj = self.mundoPertence.getObject(newPos[0], newPos[1])
            match obj:  # pode sobrepor espacos vazios
                case EspacoVazio():
                    self.atualizarPosicao(newPos)
                    # print("Movido para", newPos)

                    surrounding = self.mundoPertence.observacaoPara(newPos)
                    for s in surrounding:
                        if (type(s) == Cesto):
                            self.depositRecursos()
                case _:  #nao pode sobrepor agentes ou obstaculos ou cestos ou recursos
                    # print("Obstaculo encontrado!")
                    return False

            return True
        else:
            # print("Out of Bounds!")
            return False

    def run_simulation(self):
        pass

    # fns q learning
    def qLearning(self, goals, QTable, probExplorar, numEstados, numAcoes):
        learningRate = 0.7  # demais? a menos? #% de info nova
        desconto = 0.9  # quanto mais alto maior a quantidade de info q passa para tras
        numEpisodios = 2000  # aumentar

        for episodio in range(numEpisodios):  # deviamos comecar sempre no mesmo estado?
            if (episodio % 100 == 0):
                print("Comecar episodio:", episodio + 1)
                learningRate -= 0.001

            # print("Comecar episodio:",episodio)
            # escolhe uma posicao aleatoria para comecar
            self.mundoPertence.resetStart()  # double check later
            currentState = self.nextState()  # get state for stating pos

            # print("starting while")
            initialTime = time.time()
            while (True):
                # escolher INDEX da proxima acao
                if (np.random.rand() <= probExplorar):  # escolher se vamos explorar ou aproveitar
                    action = np.random.randint(0, numAcoes)  # usar uma action nova/aleatoria
                else:
                    action = np.argmax(QTable[currentState])  # usar um maximo conhecido

                #acted= se moved ou depositou
                acted = self.acao(self.actions[action])
                # print("moved?", moved)

                # nextState= self.nextState(currentState, action)
                nextState = self.nextState()
                # print("nextState is", nextState)

                if (nextState in goals):
                    reward = 1
                elif (acted == False):
                    reward = -1
                else:
                    reward = 0

                # print("reward is", reward)
                # atualizar matriz
                QTable[currentState, action] = (
                        ((1 - learningRate) * QTable[currentState, action]) +
                        (learningRate * (reward + (desconto * np.max(QTable[nextState])))))

                # print("goal?")
                if (time.time() - initialTime == self.mundoPertence.tempo):  # para depois do tempo acabar #como e q tenho acesso ao tempo ;(
                    break
                # print("no")

                currentState = nextState

            probExplorar -= 0.0001  # pouco/mais? #diminuir probabilidade de explorar

            # print("Farol pos", (self.mundoPertence.farol.x,self.mundoPertence.farol.y), "current", (self.x, self.y))

        self.qTable = QTable
        print(QTable)

        # queremos ver a tabela visualmente depois dos episodios?

    def nextState(self, estado, acao):  # estado vai ser o mundo? ou o index
        pass