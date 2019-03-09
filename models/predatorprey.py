from mesa import Agent, Model
from mesa.space import SingleGrid
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
import random
import numpy as np

class Predator(Agent):
    def __init__(self, unique_id, model, probdiv=0.15, probdie=0.2, probdiv_init=0.25):
        super().__init__(unique_id, model)
        self.label = "predator"
        self.probdiv_init = probdiv_init
        self.probdiv = probdiv  # probability of division
        self.probdie = probdie   # probability of death each turn
        
    def step(self):
        neighbours = self.model.grid.get_neighbors(self.pos, 1, False)
        neighbourhood = [pos for pos in self.model.grid.iter_neighborhood(self.pos, True)]
        random.shuffle(neighbourhood)  # randomly resort the neighboring positions on grid
        
        if_die = np.random.choice([1, 0], size = (1), p=[self.probdie, 1 - self.probdie])
        if (bool(if_die)):
            self.model.grid.remove_agent(self)
            self.model.schedule.remove(self)
            self.model.num_predators -= 1
        else:
            if_div = np.random.choice([1, 0], size = (1), p=[self.probdiv, 1 - self.probdiv])
            if (bool(if_div)):
                self.probdiv = self.probdiv_init
                for pos in neighbourhood:
                    if self.model.grid.is_cell_empty(pos):
                        A = Predator(self.model.num_ids, self.model)
                        self.model.num_ids += 1
                        self.model.num_predators += 1
                        self.model.grid.place_agent(A, pos)
                        self.model.schedule.add(A)
                        break

            for neighbor in neighbours:
                if neighbor.label == "prey":
                    self.model.grid.remove_agent(neighbor)
                    self.model.schedule.remove(neighbor)
                    self.model.num_prey -= 1
                    self.probdiv = min(2*self.probdiv, 1)
        
class Prey(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.label = "prey"

    def step(self):
        neighbours = self.model.grid.get_neighbors(self.pos, 1, False)
        neighbourhood = [pos for pos in self.model.grid.iter_neighborhood(self.pos, True)]
        random.shuffle(neighbourhood)  # randomly resort the neighboring positions on grid
        for pos in neighbourhood:
            if self.model.grid.is_cell_empty(pos):
                A = Prey(self.model.num_ids, self.model)
                self.model.num_ids += 1
                self.model.num_prey += 1
                self.model.grid.place_agent(A, pos)
                self.model.schedule.add(A)
                break

class PredatorPreyModel(Model):
    def __init__(self, N_predator, N_prey, width, height, random_seed=None, predator_probdiv=0.15, predator_probdie=0.2, predator_probdiv_init=0.25):
        self.num_predators = N_predator
        self.num_prey = N_prey
        self.num_ids = N_predator + N_prey
        self.grid = SingleGrid(width, height, False)
        self.schedule = RandomActivation(self)
        model_reporters = {}
        agent_reporters = {}
        used_pos_set = set()
        random.seed(a=random_seed)
        
        for i in range(self.num_predators):
            a = Predator(i, self, probdiv=predator_probdiv, probdie=predator_probdie, probdiv_init = predator_probdiv_init)
            # Generate x,y pos
            xcoor=int(random.random()*width)
            ycoor=int(random.random()*height)
            while str([xcoor,ycoor]) in used_pos_set:
                xcoor=int(random.random()*width)
                ycoor=int(random.random()*height)
            used_pos_set.add(str([xcoor,ycoor]))
            self.grid.position_agent(a, x=xcoor, y=ycoor) 

            self.schedule.add(a)
    
        for i in range(self.num_prey):
            a = Prey(i+self.num_predators, self)
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