import math
import pandas as pd
import numpy as np
from mesa import Agent
import random


class Pupil(Agent):
    """
    Define the agent type: pupils
        they have location information and travel behaviours;
        They will carry out some functions: choose destination, choose mode, etc

        Attributes:
            unique_id : the id of the agent
            hx,hy: the home location of the agent's home
            school: the agent's destination school
            # road_p: road choice probability distribution, e.g. road_p = [0.3,0.3,0.3,0.1]
            mode_p: mode choice probability distribution, e.g. mode_p = [0.1,0.9,0,0]
            perception: the agent's perception towards the COVID-19, from 1-5 , the perception increases
            health: agent's health condition, "s","i","r" representing the susecptibel, exposed, infected, reovered

    """

    def __init__(self,
                 unique_id,
                 model,
                 hx,
                 hy,
                 school,  # road_p is deleted here
                 mode_p,
                 perception,
                 health):
        ## define a new agent

        super().__init__(unique_id, model)
        self.breed = 'pupil'  # define the agent type: pupil
        self.hx = hx
        self.hy = hy
        self.school = school
        # self.road_p = road_p
        self.mode_p = mode_p
        self.perception = perception
        self.health = health
        self.infection_time = 0  ## record the infection time
        self.time = 0

        ## define the mode choice and corresponding risk, simple version by considering the whole commute process as a discrete event
        self.modes = ['bus', 'school bus', 'private car', 'walk']
        # mode_risk = {'bus':0.03,'school bus':0.01,'private car':0.001,'walk':0.02}
        self.roads = {'bus': [7], 'school bus': [6], 'private car': [4, 5], 'walk': [1, 2, 3]}
        self.road_risk = {1: 0.005, 2: 0.004, 3: 0.002, 4: 0.004, 5: 0.005, 6: 0.01, 7: 0.003}
        self.road_cell = {1: (50, 1), 2: (50, 2), 3: (50, 3), 4: (50, 4), 5: (50, 5), 6: (50, 6), 7: (50, 7)}

    def infect(self):
        """Find close contacts and infect"""

        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        if len(cellmates) > 1:
            for other in cellmates:
                if (self.random.random() < 0.5 * ((6 - self.perception) / 5) * (
                        (6 - other.perception) / 5)) and other.health == 's':
                    other.health = 'i'
                    other.infection_time = self.model.schedule.time

    def test(self):

        schools = {1: (15, 15), 2: (30, 30)}
        self.model.grid.move_agent(self, schools[self.school])
        if self.health == 'i':
            self.infect()

        self.model.grid.move_agent(self, (self.hx, self.hy))

    def step1(self):
        ## move to the assigned road from home
        mode = np.random.choice(self.modes, size=None, p=self.mode_p)

        # assign the road
        road = np.random.choice(self.roads[mode])
        # self.model.grid.move_agent(self,road_cell[road])
        # calculate the travel risk = risk * perception

        risk = self.road_risk[road] * (6 - self.perception)
        self.model.grid.move_agent(self, self.road_cell[road])

        ## if agent is susceptibel, it is possible to be infected
        if self.health == 's':
            if random.random() < risk:
                self.health = 'i'
                self.infection_time = self.model.schedule.time

        # if it is infected, calculate whether it is recovered
        ## if agent is infected, it is possible to infect other agents.
        if self.health == 'i':
            t = self.model.schedule.time - self.infection_time
            if t >= 21:
                self.health = 'r'
            else:
                self.infect()

    def step2(self):

        ## move to school from the road

        schools = {1: (15, 15), 2: (30, 30)}
        self.model.grid.move_agent(self, schools[self.school])
        if self.health == 'i':
            self.infect()

    def step3(self):

        # move to the home from the road

        self.model.grid.move_agent(self, (self.hx, self.hy))
        if self.health == 'i':
            t = self.model.schedule.time - self.infection_time
            if t >= 21:
                self.health = 'r'
            else:
                self.infect()

    def step(self):

        """
        This step function will tell agents their agenda for one day

        First, detect if the agent is infected, this is for destination choosing;

        Then, choose the mode for this destination;

        The movement will happen by move function, and the process will include the transmission or infection

        Once arrive the destination, the agent will stay there and have another possible transmission or infection

        """
        self.time = self.time + 1

        if self.time % 4 == 1:
            self.step1()
        if self.time % 4 == 2:
            self.step2()
        if self.time % 4 == 3:
            self.step1()
        if self.time % 4 == 4:
            self.step3()

        # self.assign_road()
        # self.school_activity()
        # self.go_home()
        # self.test()


class Household(Agent):
    """

    Now define the agnet type: Household members

    work: whether they need to go to the workplace, 0:stay home; 1:go outside

    hx,hy: house location

    workplace: if they need to go to the work place,there are 1,2,3 different workplaces

    mode_p: the mode choice probablility distribution, as Pupil

    perception: the covid-19 perception, from 1-5

    """

    def __init__(self, unique_id, model, hx, hy, work, workplace, mode_p, perception, health):

        super().__init__(unique_id, model)
        self.breed = 'household'
        self.work = work
        self.hx = hx
        self.hy = hy
        self.workplace = workplace
        self.mode_p = mode_p
        self.perception = perception
        self.health = health

        self.infection_time = 0  ## record the infection time
        self.time = 0

        ## define the mode choice and corresponding risk, simple version by considering the whole commute process as a discrete event
        self.modes = ['bus', 'private car', 'walk']
        # mode_risk = {'bus':0.03,'school bus':0.01,'private car':0.001,'walk':0.02}
        self.roads = {'bus': [6, 7, 8, 9], 'private car': [4, 5], 'walk': [1, 2, 3]}
        self.road_risk = {1: 0.005, 2: 0.004, 3: 0.002, 4: 0.004, 5: 0.005, 6: 0.01, 7: 0.003, 8: 0.002, 9: 0.001}
        self.road_cell = {1: (49, 1), 2: (49, 2), 3: (49, 3), 4: (49, 4), 5: (49, 5), 6: (49, 6), 7: (49, 7),
                          8: (49, 8), 9: (49, 9)}

    def infect(self):
        """Find close contacts and infect"""

        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        if len(cellmates) > 1:
            for other in cellmates:
                if (self.random.random() < 0.5 * ((6 - self.perception) / 5) * (
                        (6 - other.perception) / 5)) and other.health == 's':
                    other.health = 'i'
                    other.infection_time = self.model.schedule.time

    def step1(self):
        if self.work == 1:
            ## move to the assigned road from home
            mode = np.random.choice(self.modes, size=None, p=self.mode_p)

            # assign the road
            road = np.random.choice(self.roads[mode])
            # self.model.grid.move_agent(self,road_cell[road])
            # calculate the travel risk = risk * perception

            risk = self.road_risk[road] * (6 - self.perception)
            self.model.grid.move_agent(self, self.road_cell[road])

            ## if agent is susceptibel, it is possible to be infected
            if self.health == 's':
                if random.random() < risk:
                    self.health = 'i'
                    self.infection_time = self.model.schedule.time

            # if it is infected, calculate whether it is recovered
            ## if agent is infected, it is possible to infect other agents.
            if self.health == 'i':
                self.infect()

    def step2(self):

        ## move to workplaces from the road, if they are healthy, they may be infected by the environment.

        workplaces = {1: (15, 15), 2: (30, 30), 3: (45, 45)}
        if self.work == 1:
            self.model.grid.move_agent(self, workplaces[self.workplace])
            if self.health == 'i':
                self.infect()

            if self.health == 's':
                risk = 0.002 * (6 - self.perception)
                if random.random() < risk:
                    self.health = 'i'
                    self.infection_time = self.model.schedule.time

    def step3(self):

        # move to the home from the road

        self.model.grid.move_agent(self, (self.hx, self.hy))
        if self.health == 'i':
            t = self.model.schedule.time - self.infection_time
            if t >= 21:
                self.health = 'r'
            else:
                self.infect()

    def step(self):

        """
        This step function will tell agents their agenda for one day

        First, detect if the agent is infected, this is for destination choosing;

        Then, choose the mode for this destination;

        The movement will happen by move function, and the process will include the transmission or infection

        Once arrive the destination, the agent will stay there and have another possible transmission or infection

        """
        self.time = self.time + 1

        if self.time % 4 == 1:
            self.step1()
        if self.time % 4 == 2:
            self.step2()
        if self.time % 4 == 3:
            self.step1()
        if self.time % 4 == 4:
            self.step3()







