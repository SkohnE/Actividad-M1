from mesa import Model
from mesa.datacollection import DataCollector
from mesa.time import RandomActivation
from mesa.space import MultiGrid

from agent import Cleaner, Floor

class FloorModel(Model):
    """ 
    Creates a new model with random agents.
    Args:
        N: Number of agents in the simulation
        height, width: The size of the grid to model
        density: % of dirty floors
    """
    def __init__(self, N, width, height, density, maxTime):
        self.grid = MultiGrid(height, width, torus = False) 
        self.schedule = RandomActivation(self)
        self.density = density
        self.maxTime = maxTime
        self.timeCount = 0
        self.datacollector = DataCollector(
            {
                "Clean": lambda m: self.count_type(m, "Clean"),
                "Dirty": lambda m: self.count_type(m, "Dirty"),
            }
        )


        # Add the dirty agent to a random empty grid cell

        for (contests, x, y) in self.grid.coord_iter():
            new_floor = Floor((x, y), self)

            if self.random.random() < density:
                new_floor.setState("Dirty")

            self.grid._place_agent((x,y), new_floor)
            self.schedule.add(new_floor)

        # Add N Cleaners to the point (1, 1).

        for i in range(N):
            agent = Cleaner(i, (1,1), self)
            self.grid.place_agent(agent, (1,1))
            self.schedule.add(agent)
        
        self.running = True 
        self.datacollector.collect(self)

    def step(self):
        '''Advance the model by one step.'''
        self.schedule.step()
        self.datacollector.collect(self)

        if (self.count_type(self, "Dirty") == 0 or self.maxTime == 0):
            self.running = False
            # Data
            for agent in self.schedule.agents:
                if (isinstance(agent, Cleaner)):
                    print("Vaccum:", agent.unique_id, "Clean:", agent.cleaned, "Steps:", agent.steps)
            
            print("% of dirty floor:", self.count_type(self, "Dirty")/self.count_type(self, "Clean")*100, "after", self.timeCount, "steps.")
        self.maxTime -= 1
        self.timeCount += 1

    @staticmethod
    def count_type(model, state):

        count = 0
        for floor in model.schedule.agents:
            if (isinstance(floor, Floor) and floor.state == state):
                count += 1

        return count
