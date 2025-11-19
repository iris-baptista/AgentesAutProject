from Farol import LightHouse

import os

class MotorSimulator:
    mundo= None #instancia inicial
    modoExecucao= '' #a= aprendizagem, t= teste
    agentes= []

    def __init__(self, mapa, modo, a):
        self.mundo= mapa
        self.modoExecucao= modo
        self.agentes= a

    #cria um simulador novo
    def criar(self, nomeFicheiro):  # nomeFicheiro do tipo string
        #falta leitura de ficheiro para ter estes valores
        mundo= None
        modoExecucao= ''
        agentes= []

        return MotorSimulator(mundo, modoExecucao, agentes)

    #devolve lista de agentes
    def listaAgentes(self):
        return self.agentes

    def displayMundo(self):
        s= self.mundo.sizeMap

        for i in range(0, s):
            row = ""
            for j in range(0, s):
                obj= self.mundo.getObject(i, j)
                match obj:
                    case isinstance(LightHouse):
                        row+= "F"
                    case isinstance(Obstaculo):
                        row+= "0"
                    case isinstance(Recurso):
                        row+= "*"
                    case isinstance(Cesto):
                        row+= "U"
                    case isinstance(EspacoVazio):
                        found= False
                        for a in self.agentes: #verificar se agente esta na posicao atual
                            if (a.x == i and a.y == j and found == False):
                                row += "A"
                                found= True

                        if(found == False):
                            row += "•"

            print(row)

    #comecar a simulacao (?)
    def execute(self):
        pass

    def mainMenu(self):
        while True:
            print("\n======= Projeto de Agentes Autónomos =======")
            print("Feito por Constança Ferreira e Íris Baptista")
            print("  1. Problema do Farol")
            print("  2. Problema da Recoleção (Foraging)")
            print("  0. Sair")

            choice = input("Selecione a opção: ")

            if choice == "1":
                print("\n==== Modo de Execução ====")
                print("  1. Modo de Aprendizagem (Learning Mode)")
                print("  2. Modo de Teste (Testing Mode)")
                print("  0. Sair")

                choice1 = input("Selecione a opção: ")

                if choice1 == "1":
                    print("\n==== Política do Agente ====")
                    print("  1. Algoritmo Q-Learning")
                    print("  2. Algoritmo Genético")
                    print("  0. Sair")

                    choice2 = input("Selecione a opção: ")

                    if choice2 == "1":
                        print("a aprender com algoritmo q-learning!")
                        # learning com algoritmo q-learning
                    elif choice2 == "2":
                        print("a aprender com algoritmo genetico!")
                        # learning com algoritmo genetico
                    elif choice2 == "0":
                        break
                    else:
                        print("Opção inválida, por favor tente novamente")

                elif choice1 == "2":
                    print("a executar em modo de teste!")
                    #correr em modo teste

                elif choice1 == "0":
                    break

                else:
                    print("Opção inválida, por favor tente novamente")

            elif choice == "2":
                print("\n==== Modo de Execução ====")
                print("  1. Modo de Aprendizagem (Learning Mode)")
                print("  2. Modo de Teste (Testing Mode)")
                print("  0. Sair")

                choice3 = input("Selecione a opção: ")

                if choice3 == "1":
                    print("\n==== Política do Agente ====")
                    print("  1. Algoritmo Q-Learning")
                    print("  2. Algoritmo Genético")
                    print("  0. Sair")

                    choice4 = input("Selecione a opção: ")

                    if choice4 == "1":
                        print("a aprender com algoritmo q-learning!")
                        # learning com algoritmo q-learning
                    elif choice4 == "2":
                        print("a aprender com algoritmo genetico!")
                        # learning com algoritmo genetico
                    elif choice4 == "0":
                        break
                    else:
                        print("Opção inválida, por favor tente novamente")

                elif choice3 == "2":
                    # correr em modo teste
                    pass

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
    MotorSimulator.mainMenu()
