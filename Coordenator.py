class Coordenator():

    # construtor
    def __init__(self, farolPos):
        self.fx= farolPos[0]
        self.fy= farolPos[1]

    #devolve proxima coord na direcao do farol para o agente
    def toFarol(self, agent_x, agent_y):
        dx = self.fx - agent_x
        dy = self.fy - agent_y
        
        # escolher eixo dominante
        if abs(dx) > abs(dy):
            return (1, 0) if dx > 0 else (-1, 0)
        else:
            return (0, 1) if dy > 0 else (0, -1)