from Ambiente import LightHouse, Obstaculo, EspacoVazio, Cesto, Recurso
from Coordenator import Coordenator
from Farol import Farol
from Forager import Forager
from Foraging import Foraging
from Agente import Agente
from Finder import Finder
from Dropper import Dropper
import time
import random
import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable

def jaccard_distance(set1, set2):
    intersection = len(set1 & set2)
    union = len(set1 | set2)
    return 1 - intersection / union if union != 0 else 0

def compute_novelty(current_behavior, archive, k=5):
    # Handle the empty archive case
    if not archive:
        # The first item is, by definition, maximally novel
        return 1.0

    distances = [jaccard_distance(current_behavior, b) for b in archive]
    distances.sort()

    # Your original logic is now safe because we know len(distances) > 0
    return sum(distances[:k]) / k if len(distances) >= k else sum(distances) / len(distances)

class MotorSimulator:
    mundo= None #instancia inicial

    def __init__(self, worldSize):
        self.worldSize= worldSize

    def mainMenu(self):
        while True:
            print("\n======= Projeto de Agentes Autónomos =======")
            print("Feito por Constança Ferreira e Íris Baptista")
            print("  1. Problema do Farol")
            print("  2. Problema da Recoleção (Foraging)")
            print("  0. Sair")

            choice = input("Selecione a opção: ")

            if choice == "1": #problema do Farol
                self.mundo = Farol(self.worldSize)
                print("Mundo Farol: ")
                self.displayMundo()
                self.subMenu()
            elif choice == "2": #problema Foraging
                self.mundo = Foraging(self.worldSize)
                print("Mundo Foraging: ")
                self.displayMundo()
                self.subMenu()
            elif choice == "0": #fechar programa
                print("A terminar...")
                break
            else:
                print("Opção inválida, por favor tente novamente")

    def subMenu(self):
        while(True):
            self.mundo.resetMundo()

            print("\n==== Modo de Execução ====")
            print("  1. Modo de Aprendizagem (Learning Mode)")
            print("  2. Modo de Teste (Testing Mode)")
            print("  3. Solução Burra")
            print("  0. Sair")

            choice1 = input("Selecione a opção: ")
            if choice1 == "1": #learning mode
                print("\n==== Política do Agente ====")
                print("  1. Algoritmo Genético")
                print("  2. Algoritmo Q-Learning")

                choice2 = input("Selecione a opção: ")

                if choice2 == "1": #genetico
                    match self.mundo:
                        case Farol():
                            population = input("Selecione o tamanho da população: ")
                            gen = input("Selecione o número de gerações: ")
                            self.genetic(population, gen)
                        case Foraging():
                            print("Under development!")
                elif choice2 == "2": #q learning
                    print("A aprender com algoritmo Q-learning!")
                    learningRate = 0.7  # demais? a menos? #% de info nova
                    desconto = 0.99  # quanto mais alto maior a quantidade de info q passa para tras
                    probExplorar = 0.6  # demais?

                    if(type(self.mundo) == Farol):
                        print("Under development!")
                        for a in self.mundo.getAgentes():
                            if (type(a) != Coordenator):  # coordenador nao treina
                                a.setMundo(self.mundo)

                                if (a.qTable is None): #se e a primeira vez a correr o algoritmo
                                    a.qTable = np.zeros((142, len(Agente.actions))) #141 estados

                        #self.qLearningFarol(learningRate, desconto, probExplorar)
                    else:
                        for a in self.mundo.getAgentes():
                            if (type(a) != Coordenator):  # coordenador nao treina
                                a.setMundo(self.mundo)

                                if (a.qTable is None): #se e a primeira vez a correr o algoritmo
                                    a.qTable = np.zeros((370, len(Agente.actions))) #369 variacoes possiveis para os sensores

                        self.qLearningForaging(learningRate, desconto, probExplorar)

                    index = 0
                    for a in self.mundo.getAgentes():
                        print("QTable final do Agente", (index + 1), ":", type(a).__name__, "\n", a.qTable)
                        index += 1

                    self.showGraphs()
                else:
                    print("Opção inválida, por favor tente novamente")
            elif choice1 == "2": #modo teste
                print("a executar em modo de teste!")

                if(type(self.mundo) == Farol):
                    # com burro
                    metricBurro = self.farolBurro()

                    # com genetic
                    for a in self.mundo.getAgentes():
                        a.setMundo(self.mundo)
                    self.mundo.resetMundo()
                    metricGenetic = self.testGenetic()

                    points= []
                    for valor in range(len(metricBurro)):
                        points.append([metricBurro[valor], metricGenetic[valor]])

                    self.showTableFarol(points)
                else: #foraging tests
                    points= []
                    for test in range(5):
                        burro = self.foragingBurro() # com burro
                        print("Burro",burro)
                        qLearning = self.testQLearningForaging() # com q learning
                        print("Q",qLearning)

                        points.append([burro, qLearning])

                    self.showTableForaging(points)
            elif choice1 == "3": #modo burro
                if(type(self.mundo) == Farol):
                    self.farolBurro()
                else:
                    self.foragingBurro()
            elif choice1 == "0": #sair
                break
            else:
                print("Opção inválida, por favor tente novamente")

    def displayMundo(self):
        s= self.mundo.sizeMap
                                 
        for i in range(0, s):
            row = ""
            for j in range(0, s):
                obj= self.mundo.getObject(i, j)
                match obj:
                    case LightHouse():
                        row+= "𖤓  "
                    case Obstaculo():
                        row+= "■  "
                    case Recurso():
                        row+= "*  "
                    case Cesto():
                        row+= "u  "
                    case Agente():
                        row += "A  "
                    case _:
                        found = False
                        for a in self.mundo.getAgentes():  # verificar se agente esta na posicao atual
                            if (a.x == i and a.y == j and found == False):
                                row += "A  "
                                found = True
                        if (found == False):
                            row += "•  "

            print(row)

    def farolBurro(self):
        steps= []
        for a in self.mundo.getAgentes():
            steps.append(0)

        while(True):
            done= True
            agentIndex= 0
            for a in self.mundo.getAgentes():
                if(a.found == False):
                    done= False
                    while(True): #verificar q posicao gerada seja dentro do mapa
                        newAccao= a.acaoBurro()
                        newPos= (newAccao[0]+a.x, newAccao[1]+a.y)

                        if(newPos[0] < self.mundo.sizeMap and newPos[0] >= 0 and newPos[1] < self.mundo.sizeMap and newPos[1] >= 0):
                            break

                    steps[agentIndex]+= 1
                    obj = self.mundo.getObject(newPos[0], newPos[1])
                    if (type(obj) == EspacoVazio):
                        a.atualizarPosicao(newPos)

                        surrounding = self.mundo.observacaoPara(newPos)
                        for s in surrounding:
                            if (type(s) == LightHouse):
                                a.found = True
                                print("Encontrou o farol!")
                    else:  # obstaculo ou agente
                        print("Obstaculo encontrado!")
                else:
                    a.atualizarPosicao((-1, -1)) #para nao estar no mapa

                agentIndex+= 1

            self.displayMundo()
            print("")

            if (done == True):
                break

        index= 0
        for a in self.mundo.getAgentes():
            print(f"Agente {index+1} precisou de {steps[index]} passos para encontrar o farol!")
            index+= 1

        return steps

    def foragingBurro(self):
        initialTime= currentTime= time.time() #time() devolve tempo atual em segundos (desde epoch)
        while( (currentTime - initialTime) <= self.mundo.tempo): #"timer" para correr a quantidade de tempo dada
            for a in self.mundo.getAgentes():
                while (True):  # verificar q posicao gerada seja dentro do mapa
                    newAccao = a.acaoBurro()
                    newPos = (newAccao[0] + a.x, newAccao[1] + a.y)

                    if (newPos[0] < self.mundo.sizeMap and newPos[0] >= 0 and newPos[1] < self.mundo.sizeMap and newPos[1] >= 0):
                        break

                moved= False
                obj = self.mundo.getObject(newPos[0], newPos[1])
                match obj:
                    case Recurso(): #tem de sobrepor recurso para collect
                        if(type(a) == Forager): #so sobrepoem o recurso se for um forager
                            print(f"Encontrou o recurso {obj.name} que vale {obj.pontos} ponto(s)")

                            a.collectRecurso(obj)
                            self.mundo.removeRecurso(obj)
                            moved = True  # dropper n sobrepoem o recurso
                    case EspacoVazio():
                        moved= True
                    case _:  # se for outro agente, um obstaculo, ou um cesto
                        print("Obstaculo encontrado!")

                if(moved == True):
                    a.atualizarPosicao(newPos)

                    if(type(a) == Dropper):
                        surrounding = self.mundo.observacaoPara(newPos)
                        for s in surrounding:
                            if (type(s) == Cesto):
                                print(f"Encontrou o cesto {s.name}")

                                pointsDeposited= a.depositRecursos()
                                print(f"Depositou um total de {pointsDeposited} ponto(s)!")

            self.displayMundo()
            print("")

            currentTime = time.time()

        totalPoints= 0
        for a in self.mundo.getAgentes():
            if(type(a) == Dropper):
                totalPoints+= a.pontosDepositados

        print("Total of points: ", totalPoints)
        return totalPoints

    def genetic(self, population, gen):
        POPULATION_SIZE = int(population)
        NUM_GENERATIONS = int(gen)
        MUTATION_RATE = 0.05
        LEARNING_RATE = 0.2
        TOURNAMENT_SIZE = 3
        N_ARCHIVE_ADD = 5  # Add top 5 most novel agents to archive each gen

        # --- Initialization ---
        archive = []
        population = []
        for _ in range(POPULATION_SIZE):
            population.append(Finder((0, 0)))
        avg_fitness_per_gen = []
        best_paths_per_gen = []
        fitness_plot = []

        print("Starting evolution...")

        # --- Generational Loop ---
        for gen in range(NUM_GENERATIONS):
            total_fitness = 0

            # 1. Evaluate Population
            for agent in population:
                agent.run_simulation(self.worldSize)

                # --- Calculate and combine scores ---
                novelty_score = compute_novelty(agent.behavior, archive)
                objective_score = agent.calculate_objective_fitness()

                # Combine the scores.
                # You might need to add a weight, e.g.:
                novelty_weight = 100  # Make novelty competitive with fitness
                agent.combined_fitness = (novelty_score * novelty_weight) + objective_score
                total_fitness = total_fitness + agent.combined_fitness

            # 2. Sort population by *combined_fitness*
            population.sort(key=lambda x: x.combined_fitness, reverse=True)

            # 3. Log results for this generation
            avg_fitness = total_fitness / POPULATION_SIZE
            avg_fitness_per_gen.append(avg_fitness)
            best_paths_per_gen.append(population[0].path)

            # Get the top agent's individual scores for logging
            best_nov = compute_novelty(population[0].behavior, archive)
            best_obj = population[0].calculate_objective_fitness()

            print(
                f"Gen {gen + 1}/{NUM_GENERATIONS} | Avg Combined: {avg_fitness:.2f} | Best Combined: {population[0].combined_fitness:.2f} (Nov: {best_nov:.2f}, Obj: {best_obj:.2f})")
            fitness_plot.append(round(population[0].combined_fitness, 2))
            # 4. Update archive with the most novel behaviors (from this gen)
            #    We still update the archive based on *pure novelty*

            # Sort by novelty just for archive update
            population.sort(key=lambda x: compute_novelty(x.behavior, archive), reverse=True)
            for i in range(N_ARCHIVE_ADD):
                archive.append(population[i].behavior)

            # Re-sort by combined fitness for breeding
            population.sort(key=lambda x: x.combined_fitness, reverse=True)

            # 5. Store top genotype in genPolitic for each agent
            topGenotype = population[0].getGenotype()
            for f in population:
                f.addPolitic(topGenotype, self.worldSize)

            # 6. Create new generation (Selection, Crossover, Mutation)
            new_population = []

            n_elite = POPULATION_SIZE // 10
            new_population.extend(population[:n_elite])

            while len(new_population) < POPULATION_SIZE:
                parent1, parent2 = Agente.select_parent(population, TOURNAMENT_SIZE)
                child1, child2 = parent1.crossover(parent1, parent2)

                for child, parent in [(child1, parent1), (child2, parent2)]:
                    if parent.genPolitic:  # se houver genótipos históricos
                        historical_genotype = random.choice(parent.genPolitic)
                        for i in range(int(len(historical_genotype) * LEARNING_RATE)):
                            idx = random.randint(0, len(child.genotype) - 1)
                            child.genotype[idx] = historical_genotype[idx]

                child1.mutate(MUTATION_RATE)
                child2.mutate(MUTATION_RATE)

                new_population.append(child1)
                if len(new_population) < POPULATION_SIZE:
                    new_population.append(child2)

            population = new_population

        generation = range(1, NUM_GENERATIONS +1)
        plt.plot(generation, fitness_plot, 'ro')
        plt.ylabel("fitness")
        plt.xlabel("generation")
        plt.show()

        self.mundo.setGenPolitic(population[0].genPolitic)
        print("Evolution complete.")

    def qLearningFarol(self, learningRate, desconto, probExplorar):
        # goals = [2, 4, 6, 7]  # index de estados ao lado do farol

        print("Comecar episodio: 1")
        index = 0
        for a in self.mundo.getAgentes():  # for each agent
            print("QTable initial do Agente", (index + 1), "\n", a.qTable)
            index += 1

        numEpisodios = 15000  # aumentar
        for episodio in range(numEpisodios):
            if ((episodio + 1) % 100 == 0):
                index = 0
                for a in self.mundo.getAgentes():  # for each agent
                    print("QTable atual do Agente", (index + 1), "\n", a.qTable)
                    index += 1

                print("Comecar episodio:", episodio + 1)
                if (learningRate > 0.1):
                    learningRate -= 0.0001
                # learningRate -= 0.001

            # escolhe uma posicao aleatoria para comecar
            self.mundo.resetStart()
            currentStates = []
            visitedPos= []
            for a in self.mundo.getAgentes():  # for each agent
                currentStates.append(a.nextState())  # get state for stating pos
                visitedPos.append(set())
                a.found = False  # comecar cada episodio com found= false

            while (True):
                done = True
                index = 0
                for a in self.mundo.getAgentes():
                    if (a.found == False):  # so fazemos move os q ainda nao encontraram
                        done = False

                        # escolher INDEX da proxima acao
                        if (np.random.rand() <= probExplorar):  # escolher se vamos explorar ou aproveitar
                            action = np.random.randint(0, len(Agente.actions))  # usar uma action nova/aleatoria
                        else:
                            action = np.argmax(a.qTable[currentStates[index]])  # usar um maximo conhecido

                        moved, newPos = a.acao(Agente.actions[action])

                        nextState = a.nextState()
                        if (a.inGoal(nextState)): #indexes de estados ao lado do farol
                            reward = 5
                        elif (moved == False):
                            reward = -1
                        elif (newPos in visitedPos[index]): #penalizar repetir posicoes
                            reward = -2
                        else:
                            reward = 0

                        # atualizar matriz
                        a.qTable[currentStates[index], action] = (
                                ((1 - learningRate) * a.qTable[currentStates[index], action]) +
                                (learningRate * (reward + (desconto * np.max(a.qTable[nextState])))))

                        if (a.inGoal(nextState)):  # para quando encontra farol
                            a.found = True  # agente conclui
                            break

                        currentStates[index] = nextState
                        visitedPos[index].add(newPos)
                        index += 1
                    else:
                        a.atualizarPosicao((-1, -1))  # para remover do mapa

                if (done == True):
                    break

            if (probExplorar > 0.01):
                probExplorar -= 0.00001  # pouco/mais? #diminuir probabilidade de explorar no fim do episodio

    def qLearningForaging(self, learningRate, desconto, probExplorar):
        index = 0
        for a in self.mundo.getAgentes():  # for each agent
            print("QTable initial do Agente", (index + 1), "\n", a.qTable)
            index += 1

        print("Comecar episodio: 1")

        numEpisodios = 15000  # aumentar
        for episodio in range(numEpisodios):  # deviamos comecar sempre no mesmo estado?
            if ((episodio + 1) % 100 == 0):
                index = 0
                for a in self.mundo.getAgentes():  # for each agent
                    print("QTable atual do Agente", (index + 1), "\n", a.qTable)
                    index += 1

                print("Comecar episodio:", episodio + 1)
                if(learningRate > 0.1):
                    learningRate -= 0.0001

            #por os rescursos de volta
            self.mundo.resetMundo()

            # self.mundo.resetStart() #escolhe uma posicao aleatoria para comecar
            currentStates = []
            visited= []
            for a in self.mundo.getAgentes():  # for each agent
                currentStates.append(a.nextState())  # get state for stating pos
                visited.append(set())

            initialTime = currentTime = time.time()
            while ((currentTime - initialTime) <= self.mundo.tempo):
                index = 0
                for a in self.mundo.getAgentes():
                    # escolher INDEX da proxima acao
                    if (np.random.rand() <= probExplorar):  # escolher se vamos explorar ou aproveitar
                        action = np.random.randint(0, len(Agente.actions))  # usar uma action nova/aleatoria
                    else:
                        action = np.argmax(a.qTable[currentStates[index]])  # usar um maximo conhecido

                    moved, newPos = a.acao(Agente.actions[action])

                    nextState = a.nextState()
                    if (a.inGoal(nextState)):
                        reward = 3
                    elif (moved == False):
                        reward = -1
                    elif (type(a) == Forager and (newPos in visited)): #penalizar repetir posicoes
                        reward= -2
                    else:
                        reward = 0

                    # atualizar matriz
                    a.qTable[currentStates[index], action] = (
                            ((1 - learningRate) * a.qTable[currentStates[index], action]) +
                            (learningRate * (reward + (desconto * np.max(a.qTable[nextState])))))

                    currentStates[index] = nextState
                    visited[index].add(newPos)
                    index += 1

                currentTime = time.time()

            if(probExplorar > 0.01):
                probExplorar -= 0.00001  # pouco/mais? #diminuir probabilidade de explorar no fim do episodio

    def showGraphs(self):
        agents= self.mundo.getAgentes()

        fig, graphs = plt.subplots(1, len(agents), figsize=(10, 10))
        fig.suptitle('Learned Q-values For Each Agent')

        if(len(agents) == 1):
            graphs = [graphs]

        x = np.array(['Up', 'Right', 'Down', 'Left'])
        for i in range(0, len(agents)):
            match self.mundo:
                case Farol():
                    y = np.arange(0, 9)
                    rangeY = 9

                    # filtrar QTable para ter 1 linha por estado
                    selected = self.getSelected(agents[i].qTable)
                case Foraging():
                    y = np.arange(0, 16)
                    rangeY = 16

                    # filtrar QTable para ter 1 linha por estado
                    selected = self.getSelected(agents[i].qTable)

            #setting up graph
            graphs[i].set_title(f'Agente {i + 1}: {type(agents[i]).__name__}')
            image = graphs[i].imshow(selected, cmap='magma', interpolation='nearest')
            graphs[i].set_xlabel('Action')
            graphs[i].set_ylabel('Estado')
            graphs[i].set_xticks(np.arange(4), x)
            graphs[i].set_yticks(np.arange(rangeY), y)
            graphs[i].invert_yaxis()

            #adding colorbar
            divider = make_axes_locatable(graphs[i])
            cax = divider.append_axes("right", size="5%", pad=0.08)
            plt.colorbar(image, cax=cax)

            #ajustar cores de numeros para dar para ler
            for j in range(len(selected)):
                for k in range(4):
                    value = selected[j][k]
                    if (value <= np.max(selected) / 2):
                        graphs[i].text(k, j, f'{value:.2f}', ha='center', va='center', color='white', fontsize= 8)
                    else:
                        graphs[i].text(k, j, f'{value:.2f}', ha='center', va='center', color='black', fontsize= 8)

        fig.subplots_adjust(wspace=0.5) #para graficos nao estarem colados
        plt.show()

    def getSelected(self, QTable):
        selected= []

        match self.mundo:
            case Farol():
                ranges= [[0],[1, 14],[15, 18],[19, 32],[33, 56],[57, 92],[93, 116],[117, 140], [141]]
            case Foraging():
                ranges= [[0],[1, 14],[15, 28],[29, 42],[43, 56],[57, 92],[93, 128],[129, 164],[165, 200],[201, 236],[237, 272],[273, 296],[297, 320],[321, 344],[345, 368], [369]]

        for r in range(len(ranges)):
            rangeAtual= ranges[r]
            if(len(rangeAtual) == 1):
                rangeEstadoAtual= QTable[rangeAtual[0]]
                selected.append(rangeEstadoAtual)
            else:
                rangeEstadoAtual= QTable[rangeAtual[0]:rangeAtual[-1]]

                estado= [None]
                if (self.onlyZeros(rangeEstadoAtual)):
                    estado = [0.0, 0.0, 0.0, 0.0]

                while(estado[0] == None):
                    possibleEstado= random.choice(rangeEstadoAtual)

                    if(possibleEstado[0] != 0.0 and possibleEstado[1] != 0.0 and possibleEstado[2] != 0.0 and possibleEstado[3] != 0.0):
                        estado = possibleEstado

                selected.append(estado)

        return selected

    def onlyZeros(self, estados):
        for i in range(len(estados)):
            if (estados[i][0] != 0.0 and estados[i][1] != 0.0 and estados[i][2] != 0.0 and estados[i][3] != 0.0):
                return False

        return True

    def testGenetic(self):
        steps = [0 for _ in self.mundo.getAgentes()]
        done_agents = [False for _ in self.mundo.getAgentes()]
        coordinator = Coordenator((self.mundo.farol.x, self.mundo.farol.y))

        while not all(done_agents):
            for i, agent in enumerate(self.mundo.getAgentes()):
                if isinstance(agent, Finder) and not done_agents[i]:
                    # Seleciona ação: genótipo, hint ou aleatória
                    best_genotype = agent.genPolitic[0]  # melhor genótipo
                    if steps[i] < len(best_genotype):
                        action_choice = np.random.rand()
                        if action_choice < 0.6:  # 60% chance de seguir genótipo
                            action = best_genotype[steps[i]]
                        elif action_choice < 0.85:  # 25% chance de seguir hint
                            action = coordinator.toFarol(agent.x, agent.y)
                        else:  # 15% chance de ação aleatória
                            action = random.choice(agent.actions)
                    else:
                        done_agents[i] = True
                        continue

                    # Atualiza contadores
                    hint = coordinator.toFarol(agent.x, agent.y)
                    if action == hint:
                        agent.followed_hints += 1

                    # Executa ação
                    moved = agent.acao(action)
                    steps[i] += 1

                    # Atualiza comportamento
                    agent.behavior.add((agent.x, agent.y))
                    agent.path.append((agent.x, agent.y))

                    # Verifica se farol está à sua volta
                    surrounding = self.mundo.observacaoPara(action)
                    for s in surrounding:
                        if (type(s) == LightHouse):
                            agent.found = True

                    if agent.found:
                        done_agents[i] = True
                        print(f"Agente {i} encontrou o farol!")

            self.displayMundo()
            time.sleep(0.2)

            # Estatísticas finais
            for i, agent in enumerate(self.mundo.getAgentes()):
                if isinstance(agent, Finder):
                    print(f"Agente {i}: Steps={len(agent.path)}, Collisions={agent.collisions}, Found={agent.found}, FollowedHints={agent.followed_hints}")
                    print(f"Caminho: {agent.path}")

        return steps

    def testQLearningFarol(self):
        self.mundo.resetMundo() #para comecar no mesmo lugar q os burros

        currentStates = []
        steps = []
        for a in self.mundo.getAgentes():  # for each agent
            currentStates.append(a.nextState())  # get state for stating pos
            steps.append(0)
            #todos agentes set to false no resetMundo

        last= (-1,-1)
        while (True):
            self.displayMundo()
            print("")

            done = True
            index = 0
            for a in self.mundo.getAgentes():
                if (a.found == False):  # so fazemos move os q ainda nao encontraram
                    done = False

                    if(steps[index] % 10 == 0): #cada 10 pacos fica com uma posicao aleatoria para evitar loops
                        action= np.random.randint(0, len(Agente.actions))
                    else:
                        # escolher INDEX da proxima acao
                        action = np.argmax(a.qTable[currentStates[index]])  # usar um maximo conhecido

                        potentialAction= Agente.actions[action]
                        potentialPosition= (a.x + potentialAction[0], a.y + potentialAction[1])

                        if(potentialPosition == last): #para evitar loops
                            action= np.random.randint(0, len(Agente.actions))

                    a.acao(Agente.actions[action])
                    last= (a.x, a.y)
                    steps[index] += 1

                    nextState = a.nextState()
                    if (a.inGoal(nextState)):  # para quando encontra farol
                        a.found = True  # agente conclui
                        # break

                    currentStates[index] = nextState
                    index += 1
                else:
                    a.atualizarPosicao((-1, -1))  # para remover do mapa

            if(steps[0] == 400):
                return [-1]

            if (done == True):
                break

        return steps

    def testQLearningForaging(self):
        self.mundo.resetMundo()  # para comecar no mesmo lugar q os burros

        currentStates = []
        steps= []
        last= []
        for a in self.mundo.getAgentes():  # for each agent
            currentStates.append(a.nextState())  # get state for stating pos
            steps.append(0)
            last.append((-1, -1))
            # todos agentes ficam com o inventario vazio no reset mundo

        initialTime = currentTime = time.time()
        while ((currentTime - initialTime) <= self.mundo.tempo):
            index = 0
            for a in self.mundo.getAgentes():
                if(steps[index] % 10 == 0):
                    action= np.random.randint(0, len(Agente.actions))
                else:
                    action = np.argmax(a.qTable[currentStates[index]])  # usar um maximo conhecido

                    potentialAction= Agente.actions[action]
                    potentialPosition= a.x+ potentialAction[0], a.y+ potentialAction[1]

                    if(potentialPosition == last[index]):
                        action= np.random.randint(0, len(Agente.actions))

                a.acao(Agente.actions[action])
                last[index]= (a.x, a.y)

                nextState = a.nextState()
                currentStates[index] = nextState
                steps[index] += 1
                index += 1

            currentTime = time.time()

        totalPoints = 0
        # foragerRemainder= 0
        for a in self.mundo.getAgentes():
            if (type(a) == Dropper):
                totalPoints += a.pontosDepositados
        #     else:
        #         totalRemain= 0
        #         for r in a.recursosCollected:
        #             totalRemain+= r.pontos
        #
        #         foragerRemainder += totalRemain
        #
        # print("Left over", foragerRemainder)
        return totalPoints

    def showTableFarol(self, points):
        colors = plt.cm.BuGn(np.full(2, 0.4))
        finders = []
        for i in range(0, len(self.mundo.getAgentes())):
            finders.append("Finder " + str(i + 1))

        plt.table(cellText=points, rowLabels=finders, colLabels=['Burro', 'Genetic'], rowColours= colors, colColours=colors, loc='center', cellLoc='center')

        plt.gca().get_yaxis().set_visible(False)
        plt.gca().get_xaxis().set_visible(False)
        plt.box(False)

        plt.show()

    def showTableForaging(self, points):
        colors = plt.cm.BuGn(np.full(2, 0.4))

        plt.table(cellText=points, colLabels=['Burro', 'Q-Learning'], colColours=colors, loc='center', cellLoc='center')

        plt.gca().get_yaxis().set_visible(False)
        plt.gca().get_xaxis().set_visible(False)
        plt.box(False)

        plt.show()

if __name__ == "__main__":
    sim = MotorSimulator(10)
    sim.mainMenu()