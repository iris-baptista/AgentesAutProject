class Farol:
    mapa= []
    farol= (0, 0) #posicao vai ser alterada, isto e so para instanciar
    obstaculos= []

    def __init__(self, sizeMapa, posFarol= None, posObstaculos= None): #queremos indicar as posicoes do farol ou do mapa?
        #criar mapa
        #adicionar farol
        #adicionar obstaculos
        pass

    #observacao para mandar ao agente dado?
    def observacaoPara(self, agente): #agente do tipo Agente
        #devolve objeto do tipo Observation
        pass

    #atualiza ambiente(mapa)
    def atualizar(self):
        pass

    #movimenta o agente/faz a sua accao?
    def agir(self, accao, agente): #accao do tipo accao, agente do tipo Agente
        pass