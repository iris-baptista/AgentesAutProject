import random

class Obstaculo:
    def __init__(self, x, y):
        self.x= x
        self.y= y

class EspacoVazio:
    def __init__(self, x, y):
        self.x= x
        self.y= y

class LightHouse:
    def __init__(self, name, x, y):
        self.name= name
        self.x= x
        self.y= y

class Cesto: #ponto de entrega
    def __init__(self, name, x, y):
        self.name= name
        self.x= x
        self.y= y

class Recurso:
    def __init__(self, name, x, y):
        self.name= name
        self.x= x
        self.y= y

        self.pontos= random.randint(1, 5)