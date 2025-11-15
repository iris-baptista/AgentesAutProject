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

    #comecar a simulacao (?)
    def execute(self):
        pass