from Agente import Agente
import random
import numpy as np
from Ambiente import Obstaculo, LightHouse, EspacoVazio

class Finder(Agente):
    #construtor
    def __init__(self, posInitial): #genotype e o caminho q o agente utiliza, genotype= None
        self.x= posInitial[0]
        self.y= posInitial[1]
        self.found= False
        # self.fitness= 0
        # self.novelty
        self.path= []
        self.steps= 50
        # # nao percebi behaviour

        self.genotype = []
        for i in range(0, self.steps):
            self.genotype.append(random.choice(self.actions))

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
                case LightHouse():
                    self.found = True
                    # print("Encontrou o farol!")
                case _: # nao pode sobrepor agentes ou obstaculos
                    # print("Obstaculo encontrado!")
                    return False

            return True
        else:
            # print("Out of Bounds!")
            return False

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

    #Fns Q-Leaning
    def qLearning(self, goals, QTable, probExplorar, numEstados, numAcoes): #rede neuronal onde?
        learningRate = 0.7  # demais? a menos? #% de info nova
        desconto = 0.9  # quanto mais alto maior a quantidade de info q passa para tras
        numEpisodios = 2000  # aumentar

        for episodio in range(numEpisodios): #deviamos comecar sempre no mesmo estado?
            # if(episodio % 100 == 0):
            #     print("Comecar episodio:",episodio+1)
            #     print("QTable atual", QTable)
            #     learningRate-= 0.001

            print("Comecar episodio:",episodio)

            #escolhe uma posicao aleatoria para comecar
            self.mundoPertence.resetStart() #double check later
            currentState= self.nextState() #get state for stating pos

            print("starting while")
            while(True):
                #escolher INDEX da proxima acao
                if(np.random.rand() <= probExplorar): #escolher se vamos explorar ou aproveitar
                    action= np.random.randint(0, numAcoes) #usar uma action nova/aleatoria
                else:
                    action= np.argmax(QTable[currentState]) #usar um maximo conhecido

                # print("Index is", action)
                # print("Action is", self.actions[action])
                moved= self.acao(self.actions[action])
                # print("moved?", moved)

                # nextState= self.nextState(currentState, action)
                nextState= self.nextState()
                # print("nextState is", nextState)

                if(nextState in goals):
                    reward= 1
                elif(moved == False):
                    reward= -1
                else:
                    reward= 0

                # print("reward is", reward)
                #atualizar matriz
                QTable[currentState,action]= (
                        ( (1 - learningRate) * QTable[currentState, action] ) +
                        (learningRate * ( reward + ( desconto * np.max(QTable[nextState])))))

                # print("goal?")
                if(nextState in goals): #para quando encontra farol
                    # print("yes")
                    break
                # print("no")

                currentState= nextState

            probExplorar-= 0.0001 #pouco/mais? #diminuir probabilidade de explorar

        self.qTable= QTable
        print(QTable)
        self.showGraph()

    # def nextState(self, estado, acao): #estado e index
    #     #obs resultado de action
    #     #depending on sensors return next
    #     pass

    def nextState(self): # estados representados por o index!
        obs= self.mundoPertence.observacaoPara((self.x, self.y)) #observacao para novo index
        if(self.containsType(obs, Obstaculo)):
            if(self.containsType(obs, LightHouse)):
                if(self.containsType(obs, Agente)):
                    return 7
                else: #so farol, obstaculo, e espaco vazio
                    return 4
            elif(self.containsType(obs, Agente)):
                return 5
            else: #so obstaculos e espacos vazios
                return 1
        elif(self.containsType(obs, LightHouse)):
            if(self.containsType(obs, Agente)):
                return 6
            else: #so farol e espaco vazio
                return 2
        elif(self.containsType(obs, Agente)):
            return 3
        else: #so espacos vazios
            return 0