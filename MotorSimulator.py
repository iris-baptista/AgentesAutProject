from matplotlib import pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable

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
import copy
import numpy as np

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
    modoExecucao= '' #a= aprendizagem, t= teste

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
                while (True): #manter escolha para testing
                    self.mundo= Foraging(self.worldSize)
                    print("Mundo Foraging: ")
                    self.displayMundo()

                    again = input("Quer gerar outro mundo?(y/n) ")
                    if (again == "n"):
                        break

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
                self.modoExecucao = 'a'
                print("\n==== Política do Agente ====")
                print("  1. Algoritmo Genético")
                print("  2. Algoritmo Q-Learning")

                choice2 = input("Selecione a opção: ")

                if choice2 == "1": #genetico
                    population = input("Selecione o tamanho da população: ")
                    gen = input("Selecione o número de gerações: ")
                    # self.genetic(population, gen)
                    print("a aprender com algoritmo genetico!")
                elif choice2 == "2": #q learning
                    print("A aprender com algoritmo Q-learning!")
                    learningRate = 0.7  # demais? a menos? #% de info nova
                    desconto = 0.9  # quanto mais alto maior a quantidade de info q passa para tras
                    probExplorar = 0.6  # demais?

                    if(type(self.mundo) == Farol):
                        for a in self.mundo.getAgentes():
                            if (type(a) != Coordenator):  # coordenador nao treina
                                a.setMundo(self.mundo)

                                if (a.qTable is None): #se e a primeira vez a correr o algoritmo
                                    a.qTable = np.zeros((8, len(Agente.actions))) #8 estados

                        self.qLearningFarol(learningRate, desconto, probExplorar)
                    else:
                        for a in self.mundo.getAgentes():
                            if (type(a) != Coordenator):  # coordenador nao treina
                                a.setMundo(self.mundo)

                                if (a.qTable is None): #se e a primeira vez a correr o algoritmo
                                    a.qTable = np.zeros((15, len(Agente.actions))) #15 variacoes possiveis para os sensores
                                    #NAO ESTA DAR!!!

                        self.qLearningForaging(learningRate, desconto, probExplorar)

                    index = 0
                    for a in self.mundo.getAgentes():
                        print("QTable final do Agente", (index + 1), ":", type(a).__name__, "\n", a.qTable)
                        index += 1

                    self.showGraphs()
                else:
                    print("Opção inválida, por favor tente novamente")
            elif choice1 == "2": #modo teste
                self.modoExecucao = 't'
                print("a executar em modo de teste!")

                if(type(self.mundo) == Farol):
                    self.testFarol()
                else:
                    self.testForaging()
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
            print(f"Agente {index} precisou de {steps[index]} passos para encontrar o farol!")
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
                f"Gen {gen + 1}/{NUM_GENERATIONS} | Avg Combined: {avg_fitness:.2f} | Best Combined: {population[0].combined_fitness:.2f} (Nov: {best_nov:.2f}, Obj: {best_obj})")

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

        print("Evolution complete.")

    def qLearningFarol(self, learningRate, desconto, probExplorar):
        goals = [2, 4, 6, 7]  # index de estado ao lado do farol

        print("Comecar episodio: 1")
        index = 0
        for a in self.mundo.getAgentes():  # for each agent
            print("QTable initial do Agente", (index + 1), "\n", a.qTable)
            index += 1

        numEpisodios = 2000  # aumentar
        for episodio in range(numEpisodios):
            if((episodio+1) % 100 == 0):
                index= 0
                for a in self.mundo.getAgentes():  # for each agent
                    print("QTable atual do Agente", (index+1) ,"\n", a.qTable)
                    index+= 1

                print("Comecar episodio:", episodio+1)
                learningRate-= 0.001

            # escolhe uma posicao aleatoria para comecar
            self.mundo.resetStart()
            currentStates= []
            for a in self.mundo.getAgentes(): #for each agent
                currentStates.append(a.nextState())  # get state for stating pos
                a.found= False #comecar cada episodio com found= false

            while (True):
                done = True
                index= 0
                for a in self.mundo.getAgentes():
                    if(a.found == False): #so fazemos move os q ainda nao encontraram
                        done= False

                        # escolher INDEX da proxima acao
                        if (np.random.rand() <= probExplorar):  # escolher se vamos explorar ou aproveitar
                            action = np.random.randint(0, len(Agente.actions))  # usar uma action nova/aleatoria
                        else:
                            action = np.argmax(a.qTable[currentStates[index]])  # usar um maximo conhecido

                        moved = a.acao(Agente.actions[action])

                        nextState = a.nextState()
                        if (nextState in goals):
                            reward = 1
                        elif (moved == False):
                            reward = -1
                        else:
                            reward = 0

                        # atualizar matriz
                        a.qTable[currentStates[index], action] = (
                                ((1 - learningRate) * a.qTable[currentStates[index], action]) +
                                (learningRate * (reward + (desconto * np.max(a.qTable[nextState])))))

                        if (nextState in goals):  # para quando encontra farol
                            a.found= True #agente conclui
                            break

                        currentStates[index] = nextState
                        index+= 1
                    else:
                        a.atualizarPosicao((-1, -1)) #para remover do mapa

                if (done == True):
                    break

            probExplorar -= 0.0001  # pouco/mais? #diminuir probabilidade de explorar no fim do episodio

    def qLearningForaging(self, learningRate, desconto, probExplorar):
        print("Comecar episodio: 1")
        index = 0
        for a in self.mundo.getAgentes():  # for each agent
            print("QTable initial do Agente", (index + 1), "\n", a.qTable)
            index += 1

        numEpisodios = 2000  # aumentar
        for episodio in range(numEpisodios):  # deviamos comecar sempre no mesmo estado?
            if ((episodio + 1) % 100 == 0):
                index = 0
                for a in self.mundo.getAgentes():  # for each agent
                    print("QTable atual do Agente", (index + 1), "\n", a.qTable)
                    index += 1

                print("Comecar episodio:", episodio + 1)
                learningRate -= 0.001

            #por os rescursos de volta
            self.mundo.resetMundo()

            # escolhe uma posicao aleatoria para comecar
            self.mundo.resetStart()
            currentStates = []
            for a in self.mundo.getAgentes():  # for each agent
                currentStates.append(a.nextState())  # get state for stating pos

                if(type(a) == Forager):
                    a.recursosCollected= [] #comecar cada episodio sem recursos
                else: #se for um dropper
                    a.pontosDepositados= 0 #comecar cada episodio sem pontos

            initialTime = currentTime = time.time()
            while ((currentTime - initialTime) <= self.mundo.tempo):
                index = 0
                for a in self.mundo.getAgentes():
                    match a:
                        case Forager():
                            goals= [2, 5, 8, 9, 11, 12, 13]  # index de estado next to recurso
                        case Dropper():
                            goals= [4, 7, 8, 10, 11, 13, 14]  # index de estado next to cesto

                    # escolher INDEX da proxima acao
                    if (np.random.rand() <= probExplorar):  # escolher se vamos explorar ou aproveitar
                        action = np.random.randint(0, len(Agente.actions))  # usar uma action nova/aleatoria
                    else:
                        action = np.argmax(a.qTable[currentStates[index]])  # usar um maximo conhecido

                    moved = a.acao(Agente.actions[action])

                    nextState = a.nextState()
                    if (nextState in goals):
                        reward = 1
                    elif (moved == False):
                        reward = -1
                    else:
                        reward = 0

                    # atualizar matriz
                    a.qTable[currentStates[index], action] = (
                            ((1 - learningRate) * a.qTable[currentStates[index], action]) +
                            (learningRate * (reward + (desconto * np.max(a.qTable[nextState])))))

                    currentStates[index] = nextState
                    index += 1

                currentTime = time.time()

            probExplorar -= 0.0001  # pouco/mais? #diminuir probabilidade de explorar no fim do episodio

    def showGraphs(self):
        agents= self.mundo.getAgentes()

        fig, graphs = plt.subplots(1, len(agents), figsize=(8, 8))
        fig.suptitle('Learned Q-values For Each Agent')

        if(len(agents) == 1):
            graphs = [graphs]

        match self.mundo:
            case Farol():
                y = np.array(['0', '1', '2', '3', '4', '5', '6', '7'])
                rangeY= 8
            case Foraging():
                y = np.array(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14'])
                rangeY= 15

        x = np.array(['Up', 'Right', 'Down', 'Left'])
        for i in range(0, len(agents)):
            currentQTable= agents[i].qTable

            #setting up graph
            graphs[i].set_title(f'Agente {i + 1}: {type(agents[i]).__name__}')
            image = graphs[i].imshow(currentQTable, cmap='magma', interpolation='nearest')  # RdBu, PiYG
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
            for j in range(len(currentQTable)):
                for k in range(4):
                    value = currentQTable[j][k]
                    if (value <= np.max(currentQTable) / 2):
                        graphs[i].text(k, j, f'{value:.2f}', ha='center', va='center', color='white')
                    else:
                        graphs[i].text(k, j, f'{value:.2f}', ha='center', va='center', color='black')

        fig.subplots_adjust(wspace=0.5) #para graficos nao estarem colados
        plt.show()

    def testFarol(self):
        #com genetic
        #com q learning
        pass

    def testForaging(self):
        pass

if __name__ == "__main__":
    sim = MotorSimulator(10)
    sim.mainMenu()