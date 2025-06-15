class Integrator:
    def __init__(self, x0, T):
        self.x0 = 0
        self.T = T
        self.integral = x0
        self.firstUpdate = True

    def update(self, val: float):
        if self.firstUpdate:
            self.integral = 0 + val*self.T
            self.firstUpdate = False
        else: 
            self.integral += (self.prev_val + val)/2 * self.T
        
        self.prev_val = val
        return self.integral