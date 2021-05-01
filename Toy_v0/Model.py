from mesa import Model
from mesa.time import SimultaneousActivation
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
import pandas as pd
from Agent import Pupil, Household

from mesa import Model
from mesa.datacollection import DataCollector
from mesa.time import SimultaneousActivation
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector


def total_inf(model):
    total_infection = 0
    for agent in model.schedule.agents:
        if agent.health == 'i':
            total_infection += 1
    return total_infection


def pupil_inf(model):
    pupil_infection = 0
    for agent in model.schedule.agents:
        if agent.health == 'i' and agent.breed == 'pupil':
            pupil_infection += 1
        return pupil_infection


def household_inf(model):
    household_inf = 0
    for agent in model.schedule.agents:
        if agent.health == 'i' and agent.breed == 'household':
            household_inf += 1
    return household_inf


def home_inf(model):
    home_inf = 0
    for agent in model.schedule.agents:
        if agent.health == 'i' and agent.pos == (agent.hx, agent.hy):
            home_inf += 1
    return home_inf


def school_inf(model):
    school_inf = 0
    schools = {1: (15, 15), 2: (30, 30)}
    for agent in model.schedule.agents:
        if agent.breed == 'pupil':
            if agent.health == 'i' and agent.pos == schools[agent.school]:
                school_inf += 1
    return school_inf


def workplace_inf(model):
    workplace_inf = 0
    workplaces = {1: (15, 15), 2: (30, 30), 3: (45, 45)}
    for agent in model.schedule.agents:
        if agent.breed == 'household':
            if agent.health == 'i' and agent.pos == workplaces[agent.workplace]:
                workplace_inf += 1
    return workplace_inf


def road_inf(model):
    road_inf = 0
    road_inf = total_inf(model) - home_inf(model) - workplace_inf(model) - school_inf(model)
    return road_inf


class SimModel(Model):
    """
    The model will give a basic enviornment paramter configuration.
    And generate the grid, agents.
    """

    def __init__(self,
                 height=51,
                 width=51,

                 ):
        super().__init__()
        self.height = height
        self.width = width
        self.grid = MultiGrid(height, width, torus=False)

        self.iteration = 0

        self.schedule = SimultaneousActivation(self)

        # collect the data
        model_reporters = {
            "Total_infection": total_inf,
            "Pupil infection": pupil_inf,
            "Household Infection": household_inf,
            "Home infection": home_inf,
            "School infection": school_inf,
            "Workplace infection": workplace_inf,
            "Road infection": road_inf
        }

        self.datacollector = DataCollector(model_reporters=model_reporters, agent_reporters=None)

        # generate the agents from the file
        AgentParaDataFrame = pd.read_csv('pupil.csv')
        for row in range(0, AgentParaDataFrame.shape[0]):
            agent = Pupil(
                AgentParaDataFrame.iloc[row][0],
                self,
                AgentParaDataFrame.iloc[row][2],
                AgentParaDataFrame.iloc[row][3],
                AgentParaDataFrame.iloc[row][4],
                (AgentParaDataFrame.iloc[row][5], AgentParaDataFrame.iloc[row][6], AgentParaDataFrame.iloc[row][7],
                 AgentParaDataFrame.iloc[row][8]),
                AgentParaDataFrame.iloc[row][9],
                AgentParaDataFrame.iloc[row][10]
            )
            self.schedule.add(agent)
            self.grid.place_agent(agent, (agent.hx, agent.hy))
            # self.running = True

        HouseholdPara = pd.read_csv('household.csv')
        for row in range(0, HouseholdPara.shape[0]):
            agent = Household(
                HouseholdPara.iloc[row][0] + 20,
                self,
                HouseholdPara.iloc[row][2],
                HouseholdPara.iloc[row][3],
                HouseholdPara.iloc[row][4],
                HouseholdPara.iloc[row][5],
                (HouseholdPara.iloc[row][6], HouseholdPara.iloc[row][7], HouseholdPara.iloc[row][8]),
                HouseholdPara.iloc[row][9],
                HouseholdPara.iloc[row][10]
            )
            self.schedule.add(agent)
            self.grid.place_agent(agent, (agent.hx, agent.hy))

        self.running = True

    def step(self):

        # if self.schedule.time % 4 == 0:
        self.datacollector.collect(self)
        self.schedule.step()


