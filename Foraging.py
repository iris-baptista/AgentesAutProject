class Foraging:
    mapa= []
    cestos= [] #pontos de entrega
    recursos = []
    obstaculos= []

    def __init__(self, sizeMapa, posRecursos=None, posCestos=None, posObstaculos= None):  # queremos indicar as posicoes?
        # criar mapa
        # adicionar recursos
        # adicionar cestos
        # adicionar obstaculos
        pass

    #observacao para mandar ao agente dado?
    def observacaoPara(self, agente): #agente do tipo Agente
        #devolve objeto do tipo Observation
        pass

    #atualiza ambiente
    def atualizar(self):
        pass

    #movimenta o agente/faz a sua accao?
    def agir(self, accao, agente): #accao do tipo accao, agente do tipo Agente
        pass