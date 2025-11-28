from Agente import Agente
import random

class Finder(Agente):
    actions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    #construtor
    def __init__(self, posInitial): #genotype e o caminho q o agente utiliza, genotype= None
        self.x= posInitial[0]
        self.y= posInitial[1]
        self.found= False
        # self.fitness= 0
        # self.novelty
        # self.path= []
        # self.steps= 50
        # # nao percebi behaviour
        #
        # if(genotype != None):
        #     self.genotype= genotype
        # else:
        #     self.genotype= []
        #     for i in range(0, self.steps):
        #         self.genotype.append(random.choice(self.actions))

    def acaoBurro(self): #para ele fazer move para o farol especificamente
        choice= random.choice(self.actions)

        return choice

    def run_simulation(self):
        """Runs the agent's genotype in a fresh environment to get its behavior."""
        env = Farol()

        # --- Reset all state variables ---
        self.behavior = set()
        self.path = []
        self.farolFound = False

        # Add starting position
        self.behavior.add((env.agentx, env.agenty))
        self.path.append((env.agentx, env.agenty))

        # We need to track the keys *this agent* has for this run
        local_found_keys = []

        for action in self.genotype:
            # 1. Get new proposed position
            newx = env.agentx + action[0]
            newy = env.agenty + action[1]

            # 2. Check boundaries
            if not (0 <= newx < env.size and 0 <= newy < env.size):
                newx, newy = env.agentx, env.agenty

            # 3. Check object at new location
            obj = env.get_object_here(newx, newy)

            # 4. Update agent/env state
            if isinstance(obj, Ground):
                env.agentx, env.agenty = newx, newy
            elif isinstance(obj, Key):
                env.keys.remove(obj)
                local_found_keys.append(obj)
                self.keys_found.append(obj)
                env.agentx, env.agenty = newx, newy
            elif isinstance(obj, Treasure):
                for key in local_found_keys:
                    if key.treasure == obj.name:
                        obj.opened = True
                        env.treasures.remove(obj)
                        self.treasures_opened.append(obj)
                        env.agentx, env.agenty = newx, newy

            # 5. Record behavior
            self.behavior.add((env.agentx, env.agenty))
            self.path.append((env.agentx, env.agenty))