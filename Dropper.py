from Agente import Agente
from Ambiente import EspacoVazio, Cesto, Recurso, Obstaculo

class Dropper(Agente):
    pontosDepositados= 0

    #construtor
    def __init__(self, posInitial, foragers):
        self.x= posInitial[0]
        self.y= posInitial[1]
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
            match obj:  # pode sobrepor espacos vazios e recursos
                case EspacoVazio():
                    self.atualizarPosicao(newPos)
                    # print("Movido para", newPos)

                    surrounding = self.mundoPertence.observacaoPara(newPos)
                    for s in surrounding:
                        if (type(s) == Cesto):
                            self.depositRecursos()
                case Recurso():
                    self.atualizarPosicao(newPos); #sobrepoem sem colecionar
                case _:  #nao pode sobrepor agentes ou obstaculos ou cestos ou recursos
                    # print("Obstaculo encontrado!")
                    return False

            return True
        else:
            # print("Out of Bounds!")
            return False

    #fns genetic
    def run_simulation(self):
        pass

    # fns q learning
    def nextState(self):  # estado vai ser o mundo? ou o index
        obs = self.mundoPertence.observacaoPara((self.x, self.y))  # observacao para novo index
        if (self.containsType(obs, Obstaculo)):
            if (self.containsType(obs, Recurso)):
                if (self.containsType(obs, Cesto)):
                    return 11
                elif (self.containsType(obs, Agente)):
                    return 12
                else:
                    return 5
            elif (self.containsType(obs, Agente)):
                return 6
            elif (self.containsType(obs, Cesto)):
                if (self.containsType(obs, Agente)):
                    return 14
                else:
                    return 7
            else:
                return 1
        elif (self.containsType(obs, Recurso)):
            if (self.containsType(obs, Cesto)):
                if (self.containsType(obs, Agente)):
                    return 13
                else:
                    return 8
            elif (self.containsType(obs, Agente)):
                return 9
            else:
                return 2
        elif (self.containsType(obs, Agente)):
            if (self.containsType(obs, Cesto)):
                return 10
            else:
                return 3
        elif (self.containsType(obs, Cesto)):
            return 4
        else:  # so espacos vazios
            return 0