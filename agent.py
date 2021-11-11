from mesa import Agent

class Cleaner(Agent):
    def __init__(self, unique_id, pos, model):
        super().__init__(pos, model)
        self.unique_id = unique_id
        self.pos = pos
        self.cleaned = 0
        self.steps = 0
    
    def clean(self):
        (x, y) = self.pos
        cell = self.model.grid.get_cell_list_contents([self.pos])
        if (cell[0].state == "Dirty"):
            print("Clean cell:", x, ",", y, cell[0].state)
            cell[0].state = "Clean"
            self.cleaned += 1
            return False
        return True
        
    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=False)
        
        direction = self.random.randint(0,len(possible_steps)-1)
        print("Move", self.unique_id, "to:", possible_steps[direction])
        self.model.grid.move_agent(self, possible_steps[direction])
        self.steps += 1

    def step(self):
        if (self.clean()):
            self.move()


class Floor(Agent):
    def __init__(self, pos, model):
        super().__init__(pos, model)
        self.pos = pos
        self.state = "Clean"
    
    def step(self):
        pass

    def setState(self, state):
        self.state = state
