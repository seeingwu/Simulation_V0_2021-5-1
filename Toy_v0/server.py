from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import ChartModule
import nest_asyncio

from Model import SimModel

nest_asyncio.apply()


def agent_portrayal(agent):
    portrayal = {"Shape": "circle",
                 "Filled": "true",
                 "Layer": 0,
                 "r": 0.7}

    if agent.health == 's':
        portrayal['Color'] = 'green'
    if agent.health == 'i':
        portrayal['Color'] = 'red'
    if agent.health == 'r':
        portrayal['Color'] = 'gray'

    return portrayal


grid = CanvasGrid(agent_portrayal, 52, 52, 500, 500)

chart = ChartModule(
    [
        {"Label": "Total_infection", "Color": "red"},
        {"Label": "Pupil infection", "Color": "green"},
        {"Label": "Household Infection", "Color": "yellow"},
        {"Label": "Home infection", "Color": "blue"},
        {"Label": "School infection", "Color": "grey"},
        {"Label": "Workplace infection", "Color": "black"},
        {"Label": "Road infection", "Color": "orange"}
    ]
)

server = ModularServer(SimModel,
                       [grid, chart],
                       "Commute & Epidemic",
                       {"width": 52, "height": 52})
server.port = 8849  # The default
server.launch()