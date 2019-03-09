from models import *
import utils
from mesa.visualization.UserParam import UserSettableParameter
from mesa.visualization.modules import ChartModule

def agent_portrayal(agent):
    portrayal = {"Shape": "circle", "Filled": "true", "r": 0.5, "Layer": 0}
    colours = ["red", "blue", "green", "yellow", "purple", "orange", "brown", "grey", "black", "cyan"]
    portrayal["Color"] = colours[agent.label=="mutualist_B"]
    return portrayal

grid_width = 60
grid_height = 60

chart = ChartModule([
    {"Label": "Total_Population", "Color": "#000000"},
    {"Label": "Population_A", "Color": "#f46542"},
    {"Label": "Population_B", "Color": "#99ccff"}],
    data_collector_name='datacollector'
)

model_params = {"N_mutA": UserSettableParameter('slider', "Number of mutualist A", 50, 10, 100, 1),
                "N_mutB": UserSettableParameter('slider', "Number of mutualist B", 50, 10, 100, 1), "width": grid_width, "height": grid_height}
utils.run_interactive_visualization(MutualismModel, model_params, agent_portrayal, grid_width, grid_height, 500, 500, additional_modules=[chart])