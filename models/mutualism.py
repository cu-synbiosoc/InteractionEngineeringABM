from mesa import Agent, Model
from mesa.space import SingleGrid
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
import random
import numpy as np

class Mutualist_A(Agent):
    def __init__(self, unique_id, model, probdiv=0.2, probdie=0.15):
        super().__init__(unique_id, model)
        self.label = "mutualist_A"
        self.probdiv_init = probdiv
        self.probdiv = probdiv  # probability of division
        self.probdie = probdie   # probability of death each turn
        
    def step(self):
        neighbors = self.model.grid.get_neighbors(self.pos, 2, False)
        neighborhood = [pos for pos in self.model.grid.iter_neighborhood(self.pos, True)]
        random.shuffle(neighborhood)  # randomly resort the neighboring positions on grid
        
        if_die = np.random.choice([1, 0], size = (1), p=[self.probdie, 1 - self.probdie])
        if (bool(if_die)):
            self.model.grid.remove_agent(self)
            self.model.schedule.remove(self)
            self.model.num_mutA -= 1
        else:
            if_div = np.random.choice([1, 0], size = (1), p=[self.probdiv, 1 - self.probdiv])
            if (bool(if_div)):
                self.probdiv = self.probdiv_init
                for pos in neighborhood:
                    if self.model.grid.is_cell_empty(pos):
                        self.model.num_ids += 1
                        A = Mutualist_A(self.model.num_ids, self.model)
                        self.model.num_mutA += 1
                        self.model.grid.place_agent(A, pos)
                        self.model.schedule.add(A)
                        break

            for neighbor in neighbors:
                if neighbor.label == "mutualist_B":
                    self.probdiv = min(2*self.probdiv, 1)

class Mutualist_B(Agent):
    def __init__(self, unique_id, model, probdiv=0.2, probdie=0.15):
        super().__init__(unique_id, model)
        self.label = "mutualist_B"
        self.probdiv_init = probdiv
        self.probdiv = probdiv  # probability of division
        self.probdie = probdie   # probability of death each turn
        
    def step(self):
        neighbors = self.model.grid.get_neighbors(self.pos, 2, False)
        neighborhood = [pos for pos in self.model.grid.iter_neighborhood(self.pos, True)]
        random.shuffle(neighborhood)  # randomly resort the neighboring positions on grid
        
        if_die = np.random.choice([1, 0], size = (1), p=[self.probdie, 1 - self.probdie])
        if (bool(if_die)):
            self.model.grid.remove_agent(self)
            self.model.schedule.remove(self)
            self.model.num_mutB -= 1
        else:
            if_div = np.random.choice([1, 0], size = (1), p=[self.probdiv, 1 - self.probdiv])
            if (bool(if_div)):
                self.probdiv = self.probdiv_init
                for pos in neighborhood:
                    if self.model.grid.is_cell_empty(pos):
                        self.model.num_ids += 1
                        A = Mutualist_B(self.model.num_ids, self.model)
                        self.model.num_mutB += 1
                        self.model.grid.place_agent(A, pos)
                        self.model.schedule.add(A)
                        break

            for neighbor in neighbors:
                if neighbor.label == "mutualist_A":
                    self.probdiv = min(2*self.probdiv, 1)

class MutualismModel(Model):
    def __init__(self, N_mutA, N_mutB, width, height, random_seed=None, mutA_probdiv=0.2, mutA_probdie=0.15, mutB_probdiv=0.2, mutB_probdie=0.15):
        self.num_ids = N_mutA + N_mutB  # keeps track of agent number
        self.num_mutA = N_mutA
        self.num_mutB = N_mutB
        self.grid = SingleGrid(height, width, False)
        self.schedule = RandomActivation(self)
        model_reporters = {"Total_Population": lambda model : model.num_mutA + model.num_mutB,
                           "Population_A": lambda model : model.num_mutA, 
                           "Population_B": lambda model : model.num_mutB
                          }
        agent_reporters = {}
        used_pos_set = set()
        random.seed(a=random_seed)
        
        for i in range(self.num_mutA):
            a = Mutualist_A(i, self, probdiv=mutA_probdiv, probdie=mutA_probdie)
            # Generate x,y pos
            xcoor=int(random.random()*width)
            ycoor=int(random.random()*height)
            while str([xcoor,ycoor]) in used_pos_set:
                xcoor=int(random.random()*width)
                ycoor=int(random.random()*height)
            used_pos_set.add(str([xcoor,ycoor]))
            self.grid.position_agent(a, x=xcoor, y=ycoor) 

            self.schedule.add(a)
    
        for i in range(self.num_mutB):
            a = Mutualist_B(i+self.num_mutB, self, probdiv=mutB_probdiv, probdie=mutB_probdie)
            # Generate x,y pos
            xcoor=int(random.random()*width)
            ycoor=int(random.random()*height)
            while str([xcoor,ycoor]) in used_pos_set:
                xcoor=int(random.random()*width)
                ycoor=int(random.random()*height)
            used_pos_set.add(str([xcoor,ycoor]))
            self.grid.position_agent(a, x=xcoor, y=ycoor)

            self.schedule.add(a)

        self.datacollector = DataCollector(model_reporters=model_reporters, agent_reporters=agent_reporters)
        self.running = True
        self.datacollector.collect(self)

    def step(self):
        self.schedule.step()
        self.datacollector.collect(self)
