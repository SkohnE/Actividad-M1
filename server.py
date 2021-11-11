from mesa.datacollection import DataCollector
from mesa.visualization.modules import CanvasGrid, PieChartModule, ChartModule
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter

from agent import Cleaner, Floor
from model import FloorModel

colors = {"Clean" : "#dddddd", "Dirty": "#555555"}

def agent_portrayal(agent):
    if agent is None: return

    portrayal = {"Filled": "true"}
    
    if (isinstance(agent, Cleaner)):
        portrayal["Shape"] = "circle"
        portrayal["Color"] = "grey"
        portrayal["Layer"] = 1
        portrayal["r"] = 1
    else:
        portrayal["Shape"] = "rect"
        portrayal["w"] = 1
        portrayal["h"] = 1
        portrayal["Layer"] = 0
        portrayal["Color"] = colors[agent.state]


    return portrayal


model_params = {"N": UserSettableParameter("slider", "Number of Cleaners", 2, 1, 10, 1),
                "width": 10, #UserSettableParameter("slider", "Width", 10, 10, 30, 1), 
                "height": 10, #UserSettableParameter("slider", "Height", 10, 10, 30, 1), 
                "density": UserSettableParameter("slider", "Density dirty", 0.6, 0.1, 1, 0.1),
                "maxTime": UserSettableParameter("slider", "Max Steps", 100, 10, 400, 1)}

grid = CanvasGrid(agent_portrayal, model_params["width"], model_params["height"], 500, 500)

tree_chart = ChartModule([{"Label": label, "Color": color} for (label, color) in colors.items()])
pie_chart = PieChartModule([{"Label": label, "Color": color} for (label, color) in colors.items()])
server = ModularServer(FloorModel, [grid, tree_chart ,pie_chart], "Random Cleaner", model_params)
                       
server.port = 8521 # The default
server.launch()