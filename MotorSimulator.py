from Ambiente import LightHouse, Obstaculo, EspacoVazio, Cesto, Recurso
from Farol import Farol
from Foraging import Foraging
import Finder

class MotorSimulator:
    mundo= None #instancia inicial
    modoExecucao= '' #a= aprendizagem, t= teste
    # agentes= []

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
        print("")
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
                        for a in self.mundo.getAgentes():  # verificar se agente esta na posicao atual
                           if (a.x == i and a.y == j and found == False):
                              row += "A  "
                              found = True
                        if (found == False):
                            row += "•  "
            print(row)

    def genetic(self):
        pass  # aprendizagem com algoritmo genetico

    def qlearning(self):
        pass  # aprendizagem com algoritmo qlearning
        # tirar do simulador e por no agente

    def testing(self):
        pass  # modo de teste

    def farolBurro(self):
        a= self.mundo.getAgentes()[0]
        while(a.found == False):
            while(True): #verificar q posicao gerada seja dentro do mapa
                newAccao= a.acaoBurro()
                newPos= (newAccao[0]+a.x, newAccao[1]+a.y)

                if(newPos[0] < self.mundo.sizeMap and newPos[0] >= 0 and newPos[1] < self.mundo.sizeMap and newPos[1] >= 0):
                    break

            obj= self.mundo.getObject(newPos[0], newPos[1])

            match obj:
                case LightHouse():
                    a.found= True
                    print("Encontrou o farol!")
                case EspacoVazio():
                    a.atualizarPosicao(newPos)
                case _: #se for outro agente ou um obstaculo
                    print("Obstaculo encontrado!")

            self.displayMundo()

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
                self.displayMundo()
                print("\n==== Modo de Execução ====")
                print("  1. Modo de Aprendizagem (Learning Mode)")
                print("  2. Modo de Teste (Testing Mode)")
                print("  3. Solução Burro")
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
                elif choice1 == "3":
                    self.farolBurro()
                elif choice1 == "0":
                    break
                else:
                    print("Opção inválida, por favor tente novamente")
            elif choice == "2":
                self.mundo = Foraging(self.worldSize)
                #self.displayMundo()
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