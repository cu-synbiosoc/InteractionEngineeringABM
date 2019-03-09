from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer

def run_interactive_visualization(model, model_params, agent_portrayal, grid_width, grid_height, pixel_width=500, pixel_height=500, additional_modules=[], port=8531, title="SynBioSoc ABM"):
    grid = CanvasGrid(agent_portrayal, grid_width, grid_height, canvas_width=pixel_width, canvas_height=pixel_height)
    modules = [grid]
    modules.extend(additional_modules)
    server = ModularServer(model, modules, title, model_params)
    server.port = port
    server.launch()