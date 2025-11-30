from Agente import Agente
import random
import numpy as np

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

    def acaoBurro(self): #para ele fazer move para o farol especificamente
        choice= random.choice(self.actions)

        return choice

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
    def qLearning(self, goal, QTable, probExplorar, numEstados, numAcoes): #rede neuronal onde?
        learningRate = 0.7  # demais? a menos? #% de info nova
        recompensa = 0.7  # demais? a menos? #valor atribuido ao proximo estado (?)
        numEpisodios = 1000  # muito?

        for episodio in range(numEpisodios): #deviamos comecar sempre no mesmo estado?
            #escolhe um estado aleatoriamente
            currentState= np.random.randint(0, numEstados) #estados representados por o index!

            while(True):
                #escolher se vamos explorar ou aproveitar
                if(np.random.rand() <= probExplorar):
                    action= np.random.randint(0, numAcoes) #usar uma action nova/aleatoria
                else:
                    action= np.argmax(QTable[currentState]) #usar um maximo conhecido

                nextState= self.nextState(currentState, action)

                if(nextState == goal):
                    reward= 1
                else: #ter um elif para se for um obstaculo?
                    reward= 0

                #atualizar matriz
                QTable[currentState,action]= (
                        ( (1 - learningRate) * QTable[currentState, action] ) +
                        (learningRate * ( reward + ( recompensa * np.max(QTable[nextState])))))

                if(nextState == goal): #para quando encontra farol
                    break

                currentState= nextState
                #diminuir probabilidade de explorar?

        #queremos ver a tabela visualmente depois dos episodios?
        return QTable

    def nextState(self, estado, acao): #estado vai ser o mundo? ou o index
        pass