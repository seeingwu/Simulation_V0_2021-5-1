# Simulation_V0_2021-5-1
The simulation model for commuting and virus transmission.

This is the first version of the simulation process. Its contribution consists of the realizaion of the flexible model structure, 
the basic interactive behaviours, the grid visuallization methods, and the data collection methods. These contents provide a good 
foudation for more complex functions.

The current V0 model includes two agent types: Household & Pupil. Each of them have almost ten attributes, which give the guidence
of their actions. The agents are built by importing the synthetic .csv files.

The agent behaviours are defined in two directions. First, the agent may cause infection or transmit the virus according to their
health states in different places, like coummuting process, school or workplace. Second, they have travel behaviours: go to school 
or go to work. The travel behaviours include mode choice and road assignment. 

The infection risk is calculated in a quite easy way. It is determined by a pre-loaded probablility distribution and the Perception 
of the agent. Agent's perception will influence their behaviours. In that way, agent with virous perception has different infection
risk.

# Future improments
## Agent
  1. Add the number of the agents.
  2. Add the dimension (degree of freedom) of the Agent. The agent can evolve their behaviours or change the strategy.
  3. Add the Agent's types: For example, the environment agent such as school, workplace, external vrius environment etc.
## Visualization
  1. Give different agent types different shapes. The environment can also be visualized (rectangle)
  2. Add other charts.
## Model Logic
  1. The current model step represents the disctete events. Four steps consitutes one day.
  2. The infection mechanism can be improved along with the perception thing.
