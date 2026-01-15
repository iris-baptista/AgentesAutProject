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
            # print("Depositou o recurso ", r.name, "que valia ", r.pontos, " ponto(s)!")

        self.pontosDepositados += totalDeposited
        return totalDeposited

    def acao(self, action):
        newPos = (action[0] + self.x, action[1] + self.y)

        # so muda de posicao se for uma posicao valida/der para sobrepor!
        tamanho = self.mundoPertence.sizeMap
        if (newPos[0] < tamanho and newPos[0] >= 0 and newPos[1] < tamanho and newPos[1] >= 0):  # dentro do mapa
            obj = self.mundoPertence.getObject(newPos[0], newPos[1])
            match obj:  # pode sobrepor espacos vazios
                case EspacoVazio():
                    self.atualizarPosicao(newPos)
                    # print("Movido para", newPos)

                    surrounding = self.mundoPertence.observacaoPara(newPos)
                    for s in surrounding:
                        if (type(s) == Cesto):
                            self.depositRecursos()
                case _:  #nao pode sobrepor agentes ou obstaculos ou cestos ou recursos
                    # print("Obstaculo encontrado!")
                    return False, (self.x, self.y)

            return True, newPos
        else:
            # print("Out of Bounds!")
            return False, (self.x, self.y)

    #fns genetic
    def run_simulation(self):
        pass

    def calculate_objective_fitness(self):
        pass

    # fns q learning
    def acaoQLearning(self):
        pass

    def nextState(self):  # estado vai ser o mundo? ou o index
        obs = self.mundoPertence.observacaoPara((self.x, self.y))  # observacao para novo index

        emptyCount= self.containsType(obs, EspacoVazio)
        if(emptyCount == 0): #agent boxed in
            return 369

        obstaculoCount = self.containsType(obs, Obstaculo)
        agentCount = self.containsType(obs, Agente)
        recursoCount = self.containsType(obs, Recurso)
        cestoCount = self.containsType(obs, Cesto)
        if (obstaculoCount >= 1):
            if (recursoCount >= 1):
                if (cestoCount >= 1): #se for cesto, recurso, e obstaculo
                    match obs:
                        case [Obstaculo(), Cesto(), Recurso(), EspacoVazio()]:
                            return 273
                        case [Obstaculo(), EspacoVazio(), Recurso(), Cesto()]:
                            return 274
                        case [Obstaculo(), Recurso(), Cesto(), EspacoVazio()]:
                            return 275
                        case [Obstaculo(), Recurso(), EspacoVazio(), Cesto()]:
                            return 276
                        case [Obstaculo(), Cesto(), EspacoVazio(), Recurso()]:
                            return 277
                        case [Obstaculo(), EspacoVazio(), Cesto(), Recurso()]:
                            return 278
                        case [Recurso(), EspacoVazio(), Cesto(), Obstaculo()]:
                            return 279
                        case [Recurso(), Cesto(), EspacoVazio(), Obstaculo()]:
                            return 280
                        case [Cesto(), EspacoVazio(), Recurso(), Obstaculo()]:
                            return 281
                        case [EspacoVazio(), Cesto(), Recurso(), Obstaculo()]:
                            return 282
                        case [EspacoVazio(), Recurso(), Cesto(), Obstaculo()]:
                            return 283
                        case [Cesto(), Recurso(), EspacoVazio(), Obstaculo()]:
                            return 284
                        case [Cesto(), Obstaculo(), Recurso(), EspacoVazio()]:
                            return 285
                        case [EspacoVazio(), Obstaculo(), Recurso(), Cesto()]:
                            return 286
                        case [Recurso(), Obstaculo(), Cesto(), EspacoVazio()]:
                            return 287
                        case [Recurso(), Obstaculo(), EspacoVazio(), Cesto()]:
                            return 288
                        case [Cesto(), Obstaculo(), EspacoVazio(), Recurso()]:
                            return 289
                        case [EspacoVazio(), Obstaculo(), Cesto(), Recurso()]:
                            return 290
                        case [Recurso(), Cesto(), Obstaculo(), EspacoVazio()]:
                            return 291
                        case [Recurso(), EspacoVazio(), Obstaculo(), Cesto()]:
                            return 292
                        case [Cesto(), EspacoVazio(), Obstaculo(), Recurso()]:
                            return 293
                        case [EspacoVazio(), Cesto(), Obstaculo(), Recurso()]:
                            return 294
                        case [Cesto(), Recurso(), Obstaculo(), EspacoVazio()]:
                            return 295
                        case [EspacoVazio(), Recurso(), Obstaculo(), Cesto()]:
                            return 296
                        case _:
                            return 369
                elif (agentCount >= 1): #se agente e recurso e obstaculo
                    match obs:
                        case [Obstaculo(), Agente(), Recurso(), EspacoVazio()]:
                            return 297
                        case [Obstaculo(), EspacoVazio(), Recurso(), Agente()]:
                            return 298
                        case [Obstaculo(), Recurso(), Agente(), EspacoVazio()]:
                            return 299
                        case [Obstaculo(), Recurso(), EspacoVazio(), Agente()]:
                            return 300
                        case [Obstaculo(), EspacoVazio(), Agente(), Recurso()]:
                            return 301
                        case [Obstaculo(), Agente(), EspacoVazio(), Recurso()]:
                            return 302
                        case [Recurso(), EspacoVazio(), Agente(), Obstaculo()]:
                            return 303
                        case [Recurso(), Agente(), EspacoVazio(), Obstaculo()]:
                            return 304
                        case [Agente(), EspacoVazio(), Recurso(), Obstaculo()]:
                            return 305
                        case [EspacoVazio(), Agente(), Recurso(), Obstaculo()]:
                            return 306
                        case [EspacoVazio(), Recurso(), Agente(), Obstaculo()]:
                            return 307
                        case [Agente(), Recurso(), EspacoVazio(), Obstaculo()]:
                            return 308
                        case [Agente(), Obstaculo(), Recurso(), EspacoVazio()]:
                            return 309
                        case [EspacoVazio(), Obstaculo(), Recurso(), Agente()]:
                            return 310
                        case [Recurso(), Obstaculo(), Agente(), EspacoVazio()]:
                            return 311
                        case [Recurso(), Obstaculo(), EspacoVazio(), Agente()]:
                            return 312
                        case [EspacoVazio(), Obstaculo(), Agente(), Recurso()]:
                            return 313
                        case [Agente(), Obstaculo(), EspacoVazio(), Recurso()]:
                            return 314
                        case [Recurso(), Agente(), Obstaculo(), EspacoVazio()]:
                            return 315
                        case [Recurso(), EspacoVazio(), Obstaculo(), Agente()]:
                            return 316
                        case [Agente(), EspacoVazio(), Obstaculo(), Recurso()]:
                            return 317
                        case [EspacoVazio(), Agente(), Obstaculo(), Recurso()]:
                            return 318
                        case [Agente(), Recurso(), Obstaculo(), EspacoVazio()]:
                            return 319
                        case [EspacoVazio(), Recurso(), Obstaculo(), Agente()]:
                            return 320
                        case _:
                            return 369
                else: #recursos e obstaculos
                    if(obstaculoCount == 1):
                        if(recursoCount == 1): #1 obstaculo 1 recurso
                            match obs:
                                case [Obstaculo(), EspacoVazio(), EspacoVazio(), Recurso()]:
                                    return 57
                                case [Obstaculo(), Recurso(), EspacoVazio(), EspacoVazio()]:
                                    return 58
                                case [Obstaculo(), EspacoVazio(), Recurso(), EspacoVazio()]:
                                    return 59
                                case [Recurso(), EspacoVazio(), EspacoVazio(), Obstaculo()]:
                                    return 60
                                case [EspacoVazio(), EspacoVazio(), Recurso(), Obstaculo()]:
                                    return 61
                                case [EspacoVazio(), Recurso(), EspacoVazio(), Obstaculo()]:
                                    return 62
                                case [EspacoVazio(), Obstaculo(), Recurso(), EspacoVazio()]:
                                    return 63
                                case [Recurso(), Obstaculo(), EspacoVazio(), EspacoVazio()]:
                                    return 64
                                case [EspacoVazio(), Obstaculo(), EspacoVazio(), Recurso()]:
                                    return 65
                                case [Recurso(), EspacoVazio(), Obstaculo(), EspacoVazio()]:
                                    return 66
                                case [EspacoVazio(), EspacoVazio(), Obstaculo(), Recurso()]:
                                    return 67
                                case [EspacoVazio(), Recurso(), Obstaculo(), EspacoVazio()]:
                                    return 68
                                case _:
                                    return 369
                        else: #2 recursos 1 obstaculo
                            match obs:
                                case [Recurso(), EspacoVazio(), Obstaculo(), Recurso()]:
                                    return 81
                                case [Recurso(), Obstaculo(), EspacoVazio(), Recurso()]:
                                    return 82
                                case [EspacoVazio(), Recurso(), Obstaculo(), Recurso()]:
                                    return 83
                                case [Obstaculo(), Recurso(), EspacoVazio(), Recurso()]:
                                    return 84
                                case [Obstaculo(), Recurso(), Recurso(), EspacoVazio()]:
                                    return 85
                                case [EspacoVazio(), Recurso(), Recurso(), Obstaculo()]:
                                    return 86
                                case [Recurso(), Obstaculo(), Recurso(), EspacoVazio()]:
                                    return 87
                                case [Recurso(), EspacoVazio(), Recurso(), Obstaculo()]:
                                    return 88
                                case [Obstaculo(), EspacoVazio(), Recurso(), Recurso()]:
                                    return 89
                                case [EspacoVazio(), Obstaculo(), Recurso(), Recurso()]:
                                    return 90
                                case [Recurso(), Recurso(), Obstaculo(), EspacoVazio()]:
                                    return 91
                                case [Recurso(), Recurso(), EspacoVazio(), Obstaculo()]:
                                    return 92
                                case _:
                                    return 369
                    else: #2 obstaculos 1 recurso
                        match obs:
                            case [Obstaculo(), EspacoVazio(), Recurso(), Obstaculo()]:
                                return 69
                            case [Obstaculo(), Recurso(), EspacoVazio(), Obstaculo()]:
                                return 70
                            case [EspacoVazio(), Obstaculo(), Recurso(), Obstaculo()]:
                                return 71
                            case [Recurso(), Obstaculo(), EspacoVazio(), Obstaculo()]:
                                return 72
                            case [Recurso(), Obstaculo(), Obstaculo(), EspacoVazio()]:
                                return 73
                            case [EspacoVazio(), Obstaculo(), Obstaculo(), Recurso()]:
                                return 74
                            case [Obstaculo(), Recurso(), Obstaculo(), EspacoVazio()]:
                                return 75
                            case [Obstaculo(), EspacoVazio(), Obstaculo(), Recurso()]:
                                return 76
                            case [Recurso(), EspacoVazio(), Obstaculo(), Obstaculo()]:
                                return 77
                            case [EspacoVazio(), Recurso(), Obstaculo(), Obstaculo()]:
                                return 78
                            case [Obstaculo(), Obstaculo(), Recurso(), EspacoVazio()]:
                                return 79
                            case [Obstaculo(), Obstaculo(), EspacoVazio(), Recurso()]:
                                return 80
                            case _:
                                return 369
            elif (agentCount >= 1): #agentes, e obstaculos
                if(obstaculoCount == 1):
                    if(agentCount == 1): #1 obstaculo e 1 agente
                        match obs:
                            case [Obstaculo(), EspacoVazio(), EspacoVazio(), Agente()]:
                                return 93
                            case [Obstaculo(), Agente(), EspacoVazio(), EspacoVazio()]:
                                return 94
                            case [Obstaculo(), EspacoVazio(), Agente(), EspacoVazio()]:
                                return 95
                            case [Agente(), EspacoVazio(), EspacoVazio(), Obstaculo()]:
                                return 96
                            case [EspacoVazio(), EspacoVazio(), Agente(), Obstaculo()]:
                                return 97
                            case [EspacoVazio(), Agente(), EspacoVazio(), Obstaculo()]:
                                return 98
                            case [EspacoVazio(), Obstaculo(), Agente(), EspacoVazio()]:
                                return 99
                            case [Agente(), Obstaculo(), EspacoVazio(), EspacoVazio()]:
                                return 100
                            case [EspacoVazio(), Obstaculo(), EspacoVazio(), Agente()]:
                                return 101
                            case [Agente(), EspacoVazio(), Obstaculo(), EspacoVazio()]:
                                return 102
                            case [EspacoVazio(), EspacoVazio(), Obstaculo(), Agente()]:
                                return 103
                            case [EspacoVazio(), Agente(), Obstaculo(), EspacoVazio()]:
                                return 104
                            case _:
                                return 369
                    else: #2 agentes 1 obstaculo
                        match obs:
                            case [Agente(), EspacoVazio(), Obstaculo(), Agente()]:
                                return 117
                            case [Agente(), Obstaculo(), EspacoVazio(), Agente()]:
                                return 118
                            case [EspacoVazio(), Agente(), Obstaculo(), Agente()]:
                                return 119
                            case [Obstaculo(), Agente(), EspacoVazio(), Agente()]:
                                return 120
                            case [Obstaculo(), Agente(), Agente(), EspacoVazio()]:
                                return 121
                            case [EspacoVazio(), Agente(), Agente(), Obstaculo()]:
                                return 122
                            case [Agente(), Obstaculo(), Agente(), EspacoVazio()]:
                                return 123
                            case [Agente(), EspacoVazio(), Agente(), Obstaculo()]:
                                return 124
                            case [Agente(), Agente(), Obstaculo(), EspacoVazio()]:
                                return 125
                            case [Agente(), Agente(), EspacoVazio(), Obstaculo()]:
                                return 126
                            case [Obstaculo(), EspacoVazio(), Agente(), Agente()]:
                                return 127
                            case [EspacoVazio(), Obstaculo(), Agente(), Agente()]:
                                return 128
                            case _:
                                return 369
                else: #2 obstaculos 1 agente
                    match obs:
                        case [Obstaculo(), EspacoVazio(), Obstaculo(), Agente()]:
                            return 105
                        case [Obstaculo(), Agente(), EspacoVazio(), Obstaculo()]:
                            return 106
                        case [EspacoVazio(), Obstaculo(), Agente(), Obstaculo()]:
                            return 107
                        case [Agente(), Obstaculo(), EspacoVazio(), Obstaculo()]:
                            return 108
                        case [Agente(), Obstaculo(), Obstaculo(), EspacoVazio()]:
                            return 109
                        case [EspacoVazio(), Obstaculo(), Obstaculo(), Agente()]:
                            return 110
                        case [Obstaculo(), EspacoVazio(), Obstaculo(), Agente()]:
                            return 111
                        case [Obstaculo(), Agente(), Obstaculo(), EspacoVazio()]:
                            return 112
                        case [Obstaculo(), Obstaculo(), Agente(), EspacoVazio()]:
                            return 113
                        case [Obstaculo(), Obstaculo(), EspacoVazio(), Agente()]:
                            return 114
                        case [Agente(), EspacoVazio(), Obstaculo(), Obstaculo()]:
                            return 115
                        case [EspacoVazio(), Agente(), Obstaculo(), Obstaculo()]:
                            return 116
                        case _:
                            return 369
            elif (cestoCount >= 1):
                if (agentCount >= 1): #obstaculos, cestos, e agentes
                    match obs:
                        case [Obstaculo(), Agente(), Cesto(), EspacoVazio()]:
                            return 345
                        case [Obstaculo(), EspacoVazio(), Cesto(), Agente()]:
                            return 346
                        case [Obstaculo(), Cesto(), Agente(), EspacoVazio()]:
                            return 347
                        case [Obstaculo(), Cesto(), EspacoVazio(), Agente()]:
                            return 348
                        case [Obstaculo(), EspacoVazio(), Agente(), Cesto()]:
                            return 349
                        case [Obstaculo(), Agente(), EspacoVazio(), Cesto()]:
                            return 350
                        case [Cesto(), EspacoVazio(), Agente(), Obstaculo()]:
                            return 351
                        case [Cesto(), Agente(), EspacoVazio(), Obstaculo()]:
                            return 352
                        case [Agente(), EspacoVazio(), Cesto(), Obstaculo()]:
                            return 353
                        case [EspacoVazio(), Agente(), Cesto(), Obstaculo()]:
                            return 354
                        case [Agente(), Cesto(), EspacoVazio(), Obstaculo()]:
                            return 355
                        case [EspacoVazio(), Cesto(), Agente(), Obstaculo()]:
                            return 356
                        case [Agente(), Obstaculo(), Cesto(), EspacoVazio()]:
                            return 357
                        case [EspacoVazio(), Obstaculo(), Cesto(), Agente()]:
                            return 358
                        case [Cesto(), Obstaculo(), Agente(), EspacoVazio()]:
                            return 359
                        case [Cesto(), Obstaculo(), EspacoVazio(), Agente()]:
                            return 360
                        case [EspacoVazio(), Obstaculo(), Agente(), Cesto()]:
                            return 361
                        case [Agente(), Obstaculo(), EspacoVazio(), Cesto()]:
                            return 362
                        case [Cesto(), Agente(), Obstaculo(), EspacoVazio()]:
                            return 363
                        case [Cesto(), EspacoVazio(), Obstaculo(), Agente()]:
                            return 364
                        case [Agente(), EspacoVazio(), Obstaculo(), Cesto()]:
                            return 365
                        case [EspacoVazio(), Agente(), Obstaculo(), Cesto()]:
                            return 366
                        case [Agente(), Cesto(), Obstaculo(), EspacoVazio()]:
                            return 367
                        case [EspacoVazio(), Cesto(), Obstaculo(), Agente()]:
                            return 368
                        case _:
                            return 369
                else: #cestos e obstaculos
                    if(obstaculoCount == 1):
                        if(cestoCount == 1): #1 cesto e 1 obstaculo
                            match obs:
                                case [Obstaculo(), EspacoVazio(), Cesto(), EspacoVazio()]:
                                    return 129
                                case [Obstaculo(), Cesto(), EspacoVazio(), EspacoVazio()]:
                                    return 130
                                case [Obstaculo(), EspacoVazio(), EspacoVazio(), Cesto()]:
                                    return 131
                                case [Cesto(), EspacoVazio(), EspacoVazio(), Obstaculo()]:
                                    return 132
                                case [EspacoVazio(), EspacoVazio(), Cesto(), Obstaculo()]:
                                    return 133
                                case [EspacoVazio(), Cesto(), EspacoVazio(), Obstaculo()]:
                                    return 134
                                case [EspacoVazio(), Obstaculo(), Cesto(), EspacoVazio()]:
                                    return 135
                                case [Cesto(), Obstaculo(), EspacoVazio(), EspacoVazio()]:
                                    return 136
                                case [EspacoVazio(), Obstaculo(), EspacoVazio(), Cesto()]:
                                    return 137
                                case [Cesto(), EspacoVazio(), Obstaculo(), EspacoVazio()]:
                                    return 138
                                case [EspacoVazio(), EspacoVazio(), Obstaculo(), Cesto()]:
                                    return 139
                                case [EspacoVazio(), Cesto(), Obstaculo(), EspacoVazio()]:
                                    return 140
                                case _:
                                    return 369
                        else: #2 cestos 1 obstaculo
                            match obs:
                                case [Cesto(), Obstaculo(), EspacoVazio(), Cesto()]:
                                    return 153
                                case [Cesto(), EspacoVazio(), Obstaculo(), Cesto()]:
                                    return 154
                                case [EspacoVazio(), Cesto(), Obstaculo(), Cesto()]:
                                    return 155
                                case [Obstaculo(), Cesto(), EspacoVazio(), Cesto()]:
                                    return 156
                                case [Obstaculo(), Cesto(), Cesto(), EspacoVazio()]:
                                    return 157
                                case [EspacoVazio(), Cesto(), Cesto(), Obstaculo()]:
                                    return 158
                                case [Cesto(), Obstaculo(), Cesto(), EspacoVazio()]:
                                    return 159
                                case [Cesto(), EspacoVazio(), Cesto(), Obstaculo()]:
                                    return 160
                                case [Obstaculo(), EspacoVazio(), Cesto(), Cesto()]:
                                    return 161
                                case [EspacoVazio(), Obstaculo(), Cesto(), Cesto()]:
                                    return 162
                                case [Cesto(), Cesto(), Obstaculo(), EspacoVazio()]:
                                    return 163
                                case [Cesto(), Cesto(), EspacoVazio(), Obstaculo()]:
                                    return 164
                                case _:
                                    return 369
                    else: #2 obstaculos 1 cesto
                        match obs:
                            case [Obstaculo(), EspacoVazio(), Cesto(), Obstaculo()]:
                                return 141
                            case [Obstaculo(), Cesto(), EspacoVazio(), Obstaculo()]:
                                return 142
                            case [Cesto(), Obstaculo(), EspacoVazio(), Obstaculo()]:
                                return 143
                            case [EspacoVazio(), Obstaculo(), Cesto(), Obstaculo()]:
                                return 144
                            case [Cesto(), Obstaculo(), Obstaculo(), EspacoVazio()]:
                                return 145
                            case [EspacoVazio(), Obstaculo(), Obstaculo(), Cesto()]:
                                return 146
                            case [Obstaculo(), Cesto(), Obstaculo(), EspacoVazio()]:
                                return 147
                            case [Obstaculo(), EspacoVazio(), Obstaculo(), Cesto()]:
                                return 148
                            case [Obstaculo(), Obstaculo(), Cesto(), EspacoVazio()]:
                                return 149
                            case [Obstaculo(), Obstaculo(), EspacoVazio(), Cesto()]:
                                return 150
                            case [Cesto(), EspacoVazio(), Obstaculo(), Obstaculo()]:
                                return 151
                            case [EspacoVazio(), Cesto(), Obstaculo(), Obstaculo()]:
                                return 152
                            case _:
                                return 369
            else: #so tem obstaculos
                if(obstaculoCount == 1):
                    match obs:
                        case [Obstaculo(), EspacoVazio(), EspacoVazio(), EspacoVazio()]:
                            return 1
                        case [EspacoVazio(), EspacoVazio(), EspacoVazio(), Obstaculo()]:
                            return 2
                        case [EspacoVazio(), Obstaculo(), EspacoVazio(), EspacoVazio()]:
                            return 3
                        case [EspacoVazio(), EspacoVazio(), Obstaculo(), EspacoVazio()]:
                            return 4
                        case _:
                            return 369
                elif(obstaculoCount == 2):
                    match obs:
                        case [Obstaculo(), EspacoVazio(), EspacoVazio(), Obstaculo()]:
                            return 5
                        case [EspacoVazio(), Obstaculo(), EspacoVazio(), Obstaculo()]:
                            return 6
                        case [EspacoVazio(), Obstaculo(), Obstaculo(), EspacoVazio()]:
                            return 7
                        case [Obstaculo(), EspacoVazio(), Obstaculo(), EspacoVazio()]:
                            return 8
                        case [Obstaculo(), Obstaculo(), EspacoVazio(), EspacoVazio()]:
                            return 9
                        case [EspacoVazio(), EspacoVazio(), Obstaculo(), Obstaculo()]:
                            return 10
                        case _:
                            return 369
                else: #se forem 3 obstaculos
                    match obs:
                        case [Obstaculo(), Obstaculo(), EspacoVazio(), Obstaculo()]:
                            return 11
                        case [EspacoVazio(), Obstaculo(), Obstaculo(), Obstaculo()]:
                            return 12
                        case [Obstaculo(), Obstaculo(), Obstaculo(), EspacoVazio()]:
                            return 13
                        case [Obstaculo(), EspacoVazio(), Obstaculo(), Obstaculo()]:
                            return 14
                        case _:
                            return 369
        elif (recursoCount >= 1):
            if (cestoCount >= 1):
                if(agentCount >= 1): #recursos e cestos e agentes
                    match obs:
                        case [Recurso(), Agente(), Cesto(), EspacoVazio()]:
                            return 321
                        case [Recurso(), EspacoVazio(), Cesto(), Agente()]:
                            return 322
                        case [Recurso(), Cesto(), Agente(), EspacoVazio()]:
                            return 323
                        case [Recurso(), Cesto(), EspacoVazio(), Agente()]:
                            return 324
                        case [Recurso(), EspacoVazio(), Agente(), Cesto()]:
                            return 325
                        case [Recurso(), Agente(), EspacoVazio(), Cesto()]:
                            return 326
                        case [Cesto(), EspacoVazio(), Agente(), Recurso()]:
                            return 327
                        case [Cesto(), Agente(), EspacoVazio(), Recurso()]:
                            return 328
                        case [Agente(), EspacoVazio(), Cesto(), Recurso()]:
                            return 329
                        case [EspacoVazio(), Agente(), Cesto(), Recurso()]:
                            return 330
                        case [EspacoVazio(), Cesto(), Agente(), Recurso()]:
                            return 331
                        case [Agente(), Cesto(), EspacoVazio(), Recurso()]:
                            return 332
                        case [Agente(), Recurso(), Cesto(), EspacoVazio()]:
                            return 333
                        case [EspacoVazio(), Recurso(), Cesto(), Agente()]:
                            return 334
                        case [Cesto(), Recurso(), Agente(), EspacoVazio()]:
                            return 335
                        case [Cesto(), Recurso(), EspacoVazio(), Agente()]:
                            return 336
                        case [Agente(), Recurso(), EspacoVazio(), Cesto()]:
                            return 337
                        case [EspacoVazio(), Recurso(), Agente(), Cesto()]:
                            return 338
                        case [Cesto(), EspacoVazio(), Recurso(), Agente()]:
                            return 339
                        case [Cesto(), Agente(), Recurso(), EspacoVazio()]:
                            return 340
                        case [Agente(), EspacoVazio(), Recurso(), Cesto()]:
                            return 341
                        case [EspacoVazio(), Agente(), Recurso(), Cesto()]:
                            return 342
                        case [Agente(), Cesto(), Recurso(), EspacoVazio()]:
                            return 343
                        case [EspacoVazio(), Cesto(), Recurso(), Agente()]:
                            return 344
                        case _:
                            return 369
                else: #so recursos e cestos
                    if(cestoCount == 1):
                        if(recursoCount == 1): #1 cesto e 1 recurso
                            match obs:
                                case [Cesto(), EspacoVazio(), Recurso(), EspacoVazio()]:
                                    return 165
                                case [Cesto(), Recurso(), EspacoVazio(), EspacoVazio()]:
                                    return 166
                                case [Cesto(), EspacoVazio(), EspacoVazio(), Recurso()]:
                                    return 167
                                case [Recurso(), EspacoVazio(), EspacoVazio(), Cesto()]:
                                    return 168
                                case [EspacoVazio(), EspacoVazio(), Recurso(), Cesto()]:
                                    return 169
                                case [EspacoVazio(), Recurso(), EspacoVazio(), Cesto()]:
                                    return 170
                                case [EspacoVazio(), Cesto(), Recurso(), EspacoVazio()]:
                                    return 171
                                case [Recurso(), Cesto(), EspacoVazio(), EspacoVazio()]:
                                    return 172
                                case [EspacoVazio(), Cesto(), EspacoVazio(), Recurso()]:
                                    return 173
                                case [Recurso(), EspacoVazio(), Cesto(), EspacoVazio()]:
                                    return 174
                                case [EspacoVazio(), EspacoVazio(), Cesto(), Recurso()]:
                                    return 175
                                case [EspacoVazio(), Recurso(), Cesto(), EspacoVazio()]:
                                    return 176
                                case _:
                                    return 369
                        else: #2 recursos e 1 cesto
                            match obs:
                                case [Recurso(), EspacoVazio(), Cesto(), Recurso()]:
                                    return 189
                                case [Recurso(), Cesto(), EspacoVazio(), Recurso()]:
                                    return 190
                                case [EspacoVazio(), Recurso(), Cesto(), Recurso()]:
                                    return 191
                                case [Cesto(), Recurso(), EspacoVazio(), Recurso()]:
                                    return 192
                                case [Cesto(), Recurso(), Recurso(), EspacoVazio()]:
                                    return 193
                                case [EspacoVazio(), Recurso(), Recurso(), Cesto()]:
                                    return 194
                                case [Recurso(), EspacoVazio(), Recurso(), Cesto()]:
                                    return 195
                                case [Recurso(), Cesto(), Recurso(), EspacoVazio()]:
                                    return 196
                                case [Recurso(), Recurso(), Cesto(), EspacoVazio()]:
                                    return 197
                                case [Recurso(), Recurso(), EspacoVazio(), Cesto()]:
                                    return 198
                                case [Cesto(), EspacoVazio(), Recurso(), Recurso()]:
                                    return 199
                                case [EspacoVazio(), Cesto(), Recurso(), Recurso()]:
                                    return 200
                                case _:
                                    return 369
                    else: #2 cesto e 1 recursos
                        match obs:
                            case [Cesto(), EspacoVazio(), Recurso(), Cesto()]:
                                return 177
                            case [Cesto(), Recurso(), EspacoVazio(), Cesto()]:
                                return 178
                            case [EspacoVazio(), Cesto(), Recurso(), Cesto()]:
                                return 179
                            case [Recurso(), Cesto(), EspacoVazio(), Cesto()]:
                                return 180
                            case [Recurso(), Cesto(), Cesto(), EspacoVazio()]:
                                return 181
                            case [EspacoVazio(), Cesto(), Cesto(), Recurso()]:
                                return 182
                            case [Cesto(), Recurso(), Cesto(), EspacoVazio()]:
                                return 183
                            case [Cesto(), EspacoVazio(), Cesto(), Recurso()]:
                                return 184
                            case [Cesto(), Cesto(), Recurso(), EspacoVazio()]:
                                return 185
                            case [Cesto(), Cesto(), EspacoVazio(), Recurso()]:
                                return 186
                            case [Recurso(), EspacoVazio(), Cesto(), Cesto()]:
                                return 187
                            case [EspacoVazio(), Recurso(), Cesto(), Cesto()]:
                                return 188
                            case _:
                                return 369
            elif (agentCount >= 1): #agentes e recursos
                if(recursoCount == 1):
                    if(agentCount == 1): #1 agente e 1 recurso
                        match obs:
                            case [Agente(), EspacoVazio(), Recurso(), EspacoVazio()]:
                                return 201
                            case [Agente(), Recurso(), EspacoVazio(), EspacoVazio()]:
                                return 202
                            case [Agente(), EspacoVazio(), EspacoVazio(), Recurso()]:
                                return 202
                            case [Recurso(), EspacoVazio(), EspacoVazio(), Agente()]:
                                return 204
                            case [EspacoVazio(), EspacoVazio(), Recurso(), Agente()]:
                                return 205
                            case [EspacoVazio(), Recurso(), EspacoVazio(), Agente()]:
                                return 206
                            case [EspacoVazio(), Agente(), Recurso(), EspacoVazio()]:
                                return 207
                            case [Recurso(), Agente(), EspacoVazio(), EspacoVazio()]:
                                return 208
                            case [EspacoVazio(), Agente(), EspacoVazio(), Recurso()]:
                                return 209
                            case [Recurso(), EspacoVazio(), Agente(), EspacoVazio()]:
                                return 210
                            case [EspacoVazio(), EspacoVazio(), Agente(), Recurso()]:
                                return 211
                            case [EspacoVazio(), Recurso(), Agente(), EspacoVazio()]:
                                return 212
                            case _:
                                return 369
                    else: #se 2 agentes e 1 recurso
                        match obs:
                            case [Agente(), EspacoVazio(), Recurso(), Agente()]:
                                return 213
                            case [Agente(), Recurso(), EspacoVazio(), Agente()]:
                                return 214
                            case [EspacoVazio(), Agente(), Recurso(), Agente()]:
                                return 215
                            case [Recurso(), Agente(), EspacoVazio(), Agente()]:
                                return 216
                            case [Recurso(), Agente(), Agente(), EspacoVazio()]:
                                return 217
                            case [EspacoVazio(), Agente(), Agente(), Recurso()]:
                                return 218
                            case [Agente(), Recurso(), Agente(), EspacoVazio()]:
                                return 219
                            case [Agente(), EspacoVazio(), Agente(), Recurso()]:
                                return 220
                            case [Recurso(), EspacoVazio(), Agente(), Agente()]:
                                return 221
                            case [EspacoVazio(), Recurso(), Agente(), Agente()]:
                                return 222
                            case [Agente(), Agente(), Recurso(), EspacoVazio()]:
                                return 223
                            case [Agente(), Agente(), EspacoVazio(), Recurso()]:
                                return 224
                            case _:
                                return 369
                else: #se 2 recursos e 1 agente
                    match obs:
                        case [Recurso(), EspacoVazio(), Agente(), Recurso()]:
                            return 225
                        case [Recurso(), Agente(), EspacoVazio(), Recurso()]:
                            return 226
                        case [EspacoVazio(), Recurso(), Agente(), Recurso()]:
                            return 227
                        case [Agente(), Recurso(), EspacoVazio(), Recurso()]:
                            return 228
                        case [Agente(), Recurso(), Recurso(), EspacoVazio()]:
                            return 229
                        case [EspacoVazio(), Recurso(), Recurso(), Agente()]:
                            return 230
                        case [Recurso(), Agente(), Recurso(), EspacoVazio()]:
                            return 231
                        case [Recurso(), EspacoVazio(), Recurso(), Agente()]:
                            return 232
                        case [Recurso(), Recurso(), Agente(), EspacoVazio()]:
                            return 233
                        case [Recurso(), Recurso(), EspacoVazio(), Agente()]:
                            return 234
                        case [Agente(), EspacoVazio(), Recurso(), Recurso()]:
                            return 235
                        case [EspacoVazio(), Agente(), Recurso(), Recurso()]:
                            return 236
                        case _:
                            return 369
            else: #se for so recursos
                if(recursoCount == 1):
                    match obs:
                        case [Recurso(), EspacoVazio(), EspacoVazio(), EspacoVazio()]:
                            return 15
                        case [EspacoVazio(), Recurso(), EspacoVazio(), EspacoVazio()]:
                            return 17
                        case [EspacoVazio(), EspacoVazio(), Recurso(), EspacoVazio()]:
                            return 18
                        case [EspacoVazio(), EspacoVazio(), EspacoVazio(), Recurso()]:
                            return 16
                        case _:
                            return 369
                elif(recursoCount == 2):
                    match obs:
                        case [Recurso(), EspacoVazio(), EspacoVazio(), Recurso()]:
                            return 19
                        case [EspacoVazio(), Recurso(), EspacoVazio(), Recurso()]:
                            return 20
                        case [EspacoVazio(), Recurso(), Recurso(), EspacoVazio()]:
                            return 21
                        case [Recurso(), EspacoVazio(), Recurso(), EspacoVazio()]:
                            return 22
                        case [Recurso(), Recurso(), EspacoVazio(), EspacoVazio()]:
                            return 23
                        case [EspacoVazio(), EspacoVazio(), Recurso(), Recurso()]:
                            return 24
                        case _:
                            return 369
                else: #se 3 recursos
                    match obs:
                        case [Recurso(), EspacoVazio(), Recurso(), Recurso()]:
                            return 25
                        case [Recurso(), Recurso(), EspacoVazio(), Recurso()]:
                            return 26
                        case [EspacoVazio(), Recurso(), Recurso(), Recurso()]:
                            return 27
                        case [Recurso(), Recurso(), Recurso(), EspacoVazio()]:
                            return 28
                        case _:
                            return 369
        elif (agentCount >= 1):
            if (cestoCount >= 1): #agentes e cestos
                if(agentCount == 1):
                    if(cestoCount == 1): #1 agente e 1 cesto
                        match obs:
                            case [Agente(), EspacoVazio(), Cesto(), EspacoVazio()]:
                                return 237
                            case [Agente(), Cesto(), EspacoVazio(), EspacoVazio()]:
                                return 238
                            case [Agente(), EspacoVazio(), EspacoVazio(), Cesto()]:
                                return 239
                            case [Cesto(), EspacoVazio(), EspacoVazio(), Agente()]:
                                return 240
                            case [EspacoVazio(), EspacoVazio(), Cesto(), Agente()]:
                                return 241
                            case [EspacoVazio(), Cesto(), EspacoVazio(), Agente()]:
                                return 242
                            case [EspacoVazio(), Agente(), Cesto(), EspacoVazio()]:
                                return 243
                            case [Cesto(), Agente(), EspacoVazio(), EspacoVazio()]:
                                return 244
                            case [EspacoVazio(), Agente(), EspacoVazio(), Cesto()]:
                                return 245
                            case [Cesto(), EspacoVazio(), Agente(), EspacoVazio()]:
                                return 246
                            case [EspacoVazio(), EspacoVazio(), Agente(), Cesto()]:
                                return 247
                            case [EspacoVazio(), Cesto(), Agente(), EspacoVazio()]:
                                return 248
                            case _:
                                return 369
                    else: #2 cestos e 1 agente
                        match obs:
                            case [Agente(), Cesto(), Cesto(), EspacoVazio()]:
                                return 261
                            case [EspacoVazio(), Cesto(), Cesto(), Agente()]:
                                return 262
                            case [Cesto(), Agente(), Cesto(), EspacoVazio()]:
                                return 263
                            case [Cesto(), EspacoVazio(), Cesto(), Agente()]:
                                return 264
                            case [Cesto(), EspacoVazio(), Agente(), Cesto()]:
                                return 265
                            case [Cesto(), Agente(), EspacoVazio(), Cesto()]:
                                return 266
                            case [EspacoVazio(), Cesto(), Agente(), Cesto()]:
                                return 267
                            case [Agente(), Cesto(), EspacoVazio(), Cesto()]:
                                return 268
                            case [Cesto(), Cesto(), Agente(), EspacoVazio()]:
                                return 269
                            case [Cesto(), Cesto(), EspacoVazio(), Agente()]:
                                return 270
                            case [Agente(), EspacoVazio(), Cesto(), Cesto()]:
                                return 271
                            case [EspacoVazio(), Agente(), Cesto(), Cesto()]:
                                return 272
                            case _:
                                return 369
                else: #2 agentes e 1 cesto
                    match obs:
                        case [Agente(), EspacoVazio(), Cesto(), Agente()]:
                            return 249
                        case [Agente(), Cesto(), EspacoVazio(), Agente()]:
                            return 250
                        case [EspacoVazio(), Agente(), Cesto(), Agente()]:
                            return 251
                        case [Cesto(), Agente(), EspacoVazio(), Agente()]:
                            return 252
                        case [Cesto(), Agente(), Agente(), EspacoVazio()]:
                            return 253
                        case [EspacoVazio(), Agente(), Agente(), Cesto()]:
                            return 254
                        case [Agente(), EspacoVazio(), Agente(), Cesto()]:
                            return 255
                        case [Agente(), Cesto(), Agente(), EspacoVazio()]:
                            return 256
                        case [Agente(), Agente(), EspacoVazio(), Cesto()]:
                            return 258
                        case [Agente(), Agente(), Cesto(), EspacoVazio()]:
                            return 257
                        case [EspacoVazio(), Cesto(), Agente(), Agente()]:
                            return 259
                        case [Cesto(), EspacoVazio(), Agente(), Agente()]:
                            return 260
                        case _:
                            return 369
            else: #so agentes
                if(agentCount == 1):
                    match obs:
                        case [Agente(), EspacoVazio(), EspacoVazio(), EspacoVazio()]:
                            return 29
                        case [EspacoVazio(), Agente(), EspacoVazio(), EspacoVazio()]:
                            return 31
                        case [EspacoVazio(), EspacoVazio(), Agente(), EspacoVazio()]:
                            return 32
                        case [EspacoVazio(), EspacoVazio(), EspacoVazio(), Agente()]:
                            return 30
                        case _:
                            return 369
                elif(agentCount == 2):
                    match obs:
                        case [Agente(), EspacoVazio(), EspacoVazio(), Agente()]:
                            return 33
                        case [EspacoVazio(), Agente(), EspacoVazio(), Agente()]:
                            return 34
                        case [EspacoVazio(), Agente(), Agente(), EspacoVazio()]:
                            return 35
                        case [Agente(), EspacoVazio(), Agente(), EspacoVazio()]:
                            return 36
                        case [Agente(), Agente(), EspacoVazio(), EspacoVazio()]:
                            return 37
                        case [EspacoVazio(), EspacoVazio(), Agente(), Agente()]:
                            return 38
                        case _:
                            return 369
                else: #se forem 3 agentes
                    match obs:
                        case [Agente(), EspacoVazio(), Agente(), Agente()]:
                            return 39
                        case [EspacoVazio(), Agente(), Agente(), Agente()]:
                            return 41
                        case [Agente(), Agente(), EspacoVazio(), Agente()]:
                            return 40
                        case [Agente(), Agente(), Agente(), EspacoVazio()]:
                            return 42
                        case _:
                            return 369
        elif (cestoCount >= 1):
            if(cestoCount == 1):
                match obs:
                    case [Cesto(), EspacoVazio(), EspacoVazio(), EspacoVazio()]:
                        return 43
                    case [EspacoVazio(), Cesto(), EspacoVazio(), EspacoVazio()]:
                        return 45
                    case [EspacoVazio(), EspacoVazio(), Cesto(), EspacoVazio()]:
                        return 46
                    case [EspacoVazio(), EspacoVazio(), EspacoVazio(), Cesto()]:
                        return 44
                    case _:
                        return 369
            elif (cestoCount == 2):
                match obs:
                    case [Cesto(), EspacoVazio(), EspacoVazio(), Cesto()]:
                        return 47
                    case [EspacoVazio(), Cesto(), EspacoVazio(), Cesto()]:
                        return 48
                    case [EspacoVazio(), Cesto(), Cesto(), EspacoVazio()]:
                        return 49
                    case [Cesto(), EspacoVazio(), Cesto(), EspacoVazio()]:
                        return 50
                    case [Cesto(), Cesto(), EspacoVazio(), EspacoVazio()]:
                        return 52
                    case [EspacoVazio(), EspacoVazio(), Cesto(), Cesto()]:
                        return 51
                    case _:
                        return 369
            else: #se forem 3 cestos
                match obs:
                    case [EspacoVazio(), Cesto(), Cesto(), Cesto()]:
                        return 53
                    case [Cesto(), Cesto(), Cesto(), EspacoVazio()]:
                        return 54
                    case [Cesto(), Cesto(), EspacoVazio(), Cesto()]:
                        return 55
                    case [Cesto(), EspacoVazio(), Cesto(), Cesto()]:
                        return 56
                    case _:
                        return 369
        else:  # so espacos vazios
            return 0

    def inGoal(self, nextState):
        if (nextState >= 43 and nextState <= 56):
            return True
        elif (nextState >= 129 and nextState <= 200):
            return True
        elif (nextState >= 237 and nextState <= 296):
            return True
        elif (nextState >= 345 and nextState <= 368):
            return True
        else:
            return False