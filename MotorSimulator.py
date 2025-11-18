from Farol import LightHouse


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
                #verificar se agente esta na posicao atual primeiro!
                #else:
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
                        row += "•"

            print(row)

    #comecar a simulacao (?)
    def execute(self):
        pass

if __name__ == '__main__':
    for i in range(0, 10):
        print(i)