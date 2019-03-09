from models import *
import utils
from mesa.visualization.UserParam import UserSettableParameter

def agent_portrayal(agent):
    portrayal = {"Shape": "circle", "Filled": "true", "r": 0.5, "Layer": 0}
    colours = {"prey": "blue", "predator": "red"}
    portrayal["Color"] = colours[agent.label]
    return portrayal

grid_width = 60
grid_height = 60
model_params = {"N_predator": UserSettableParameter('slider', "Number of predators", 20, 0, 100, 1,
                               description="Choose how many predators to include in the model"),
                "N_prey": UserSettableParameter('slider', "Number of prey", 100, 1, 1000, 1,
                               description="Choose how many prey to include in the model"),
                "width": grid_width, "height": grid_height}
utils.run_interactive_visualization(PredatorPreyModel, model_params, agent_portrayal, grid_width, grid_height, 500, 500)