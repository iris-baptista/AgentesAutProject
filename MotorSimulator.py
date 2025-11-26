from Ambiente import LightHouse, Obstaculo, EspacoVazio, Cesto, Recurso
from Farol import Farol
from Foraging import Foraging
import random
import Agente
import Finder


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
    agentes= []

    def __init__(self, worldSize):
        self.worldSize= worldSize

    # #cria um simulador novo
    # def criar(self, nomeFicheiro):  # nomeFicheiro do tipo string
    #     #falta leitura de ficheiro para ter estes valores
    #     mundo= None
    #     modoExecucao= ''
    #     agentes= []
    #
    #     return MotorSimulator(mundo, modoExecucao, agentes)

    #devolve lista de agentes
    def listaAgentes(self):
        return self.agentes

    def displayMundo(self):
        s= self.mundo.sizeMap
                                 
        for i in range(0, s):
            row = ""
            for j in range(0, s):
                obj= self.mundo.getObject(i, j)
                # print(obj.__class__)
                # print(i, j)
                match obj:
                    case LightHouse():
                        row+= "F  "
                    case Obstaculo():
                        row+= "0  "
                    case Recurso():
                        row+= "*  "
                    case Cesto():
                        row+= "U  "
                    case _:
                        found = False
                        for a in self.agentes:  # verificar se agente esta na posicao atual
                           if (a.x == i and a.y == j and found == False):
                              row += "A  "
                              found = True
                        if (found == False):
                            row += "•  "
            print(row)

    def genetic(self, population, gen):
        # --- EA Hyperparameters ---
        POPULATION_SIZE = population
        NUM_GENERATIONS = gen
        MUTATION_RATE = 0.01
        TOURNAMENT_SIZE = 3
        N_ARCHIVE_ADD = 5  # Add top 5 most novel agents to archive each gen

        # --- Initialization ---
        archive = []
        population = [Agente() for _ in range(POPULATION_SIZE)]
        avg_fitness_per_gen = []
        best_paths_per_gen = []

        print("Starting evolution...")

        # --- Generational Loop ---
        for gen in range(NUM_GENERATIONS):
            total_fitness = 0

            # 1. Evaluate Population
            for agent in population:
                agent.run_simulation()

                # --- Calculate and combine scores ---
                novelty_score = compute_novelty(agent.behavior, archive)
                objective_score = agent.calculate_objective_fitness()

                # Combine the scores.
                # You might need to add a weight, e.g.:
                novelty_weight = 1000  # Make novelty competitive with fitness
                agent.combined_fitness = (novelty_score * novelty_weight) + objective_score
                total_fitness += agent.combined_fitness

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

            # 5. Create new generation (Selection, Crossover, Mutation)
            new_population = []

            n_elite = POPULATION_SIZE // 10
            new_population.extend(population[:n_elite])

            while len(new_population) < POPULATION_SIZE:
                parent1 = Finder.select_parent(population, TOURNAMENT_SIZE)  # This now uses combined_fitness
                parent2 = Finder.select_parent(population, TOURNAMENT_SIZE)

                child1, child2 = Finder.crossover(parent1, parent2)

                child1.mutate(MUTATION_RATE)
                child2.mutate(MUTATION_RATE)

                new_population.append(child1)
                if len(new_population) < POPULATION_SIZE:
                    new_population.append(child2)

            population = new_population

        print("Evolution complete.")

    def testing(self):
        pass  # modo de teste

    def mainMenu(self):
        while True:
            print("\n======= Projeto de Agentes Autónomos =======")
            print("Feito por Constança Ferreira e Íris Baptista")
            print("  1. Problema do Farol")
            print("  2. Problema da Recoleção (Foraging)")
            print("  0. Sair")

            choice = input("Selecione a opção: ")

            if choice == "1":
                self.mundo = Farol(self.worldSize)
                print("Mundo Farol: ")
                self.displayMundo()
                print("\n==== Modo de Execução ====")
                print("  1. Modo de Aprendizagem (Learning Mode)")
                print("  2. Modo de Teste (Testing Mode)")
                print("  0. Sair")

                choice1 = input("Selecione a opção: ")

                if choice1 == "1":
                    self.modoExecucao = 'a'
                    print("\n==== Política do Agente ====")
                    print("  1. Algoritmo Genético")
                    print("  2. Algoritmo Q-Learning")
                    print("  0. Sair")

                    choice2 = input("Selecione a opção: ")

                    if choice2 == "1":
                        print("a aprender com algoritmo genetico!")
                        # learning com algoritmo genetico
                        # self.genetico()
                    elif choice2 == "2":
                        print("a aprender com algoritmo q-learning!")
                        # learning com algoritmo q-learning
                        # self.qlearning()
                    elif choice2 == "0":
                        break
                    else:
                        print("Opção inválida, por favor tente novamente")
                elif choice1 == "2":
                    self.modoExecucao = 't'
                    print("a executar em modo de teste!")
                    # correr em modo teste
                    # self.testing()
                    # imprimir mundo para ser visualizado
                    # self.displayMundo()
                elif choice1 == "0":
                    break
                else:
                    print("Opção inválida, por favor tente novamente")
            elif choice == "2":
                self.mundo = Foraging(self.worldSize)
                self.displayMundo()
                print("\n==== Modo de Execução ====")
                print("  1. Modo de Aprendizagem (Learning Mode)")
                print("  2. Modo de Teste (Testing Mode)")
                print("  0. Sair")

                choice3 = input("Selecione a opção: ")

                if choice3 == "1":
                    self.modoExecucao = 'a'
                    print("\n==== Política do Agente ====")
                    print("  1. Algoritmo Genético")
                    print("  2. Algoritmo Q-Learning")
                    print("  0. Sair")

                    choice4 = input("Selecione a opção: ")

                    if choice4 == "1":
                        print("a aprender com algoritmo genetico!")
                        # learning com algoritmo genetico
                        # self.genetico()
                    elif choice4 == "2":
                        print("a aprender com algoritmo q-learning!")
                        # learning com algoritmo q-learning
                        # self.qlearning()
                    elif choice4 == "0":
                        break
                    else:
                        print("Opção inválida, por favor tente novamente")
                elif choice3 == "2":
                    self.modoExecucao = 't'
                    # correr em modo teste
                    # self.testing()
                    # imprimir mundo para ser visualizado
                    # self.displayMundo()
                elif choice3 == "0":
                    break
                else:
                    print("Opção inválida, por favor tente novamente")
            elif choice == "0":
                print("A terminar...")
                break
            else:
                print("Opção inválida, por favor tente novamente")



if __name__ == "__main__":
    sim = MotorSimulator(10)
    sim.mainMenu()