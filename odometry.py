from integrator import Integrator
from math import cos, sin

class Odometry:
    def __init__(self, wheel_raidus: float, base: float, T: float, x_start = 0.0, y_start = 0.0, theta_start = 0.0):
        self.wheel_raidus = wheel_raidus
        self.base = base
        self.T = T
        self.x_integrator = Integrator(0, T)
        self.y_integrator = Integrator(0, T)
        self.theta_integrator = Integrator(0, T)
        self.x = x_start
        self.y = y_start
        self.theta = theta_start
    
    def __get_speed(self, omega_l, omega_r):
        v = (omega_l + omega_r) * self.wheel_raidus / 2
        omega_robot = (omega_r - omega_l) * self.wheel_raidus / self.base
        dx = v * cos(self.theta)
        dy = v * sin(self.theta)
        dtheta = omega_robot
        return (dx, dy, dtheta)
    
    def update(self, omega_l, omega_r):
        dx, dy, dtheta = self.__get_speed(omega_l, omega_r)

        self.x = self.x_integrator.update(dx)
        self.y = self.y_integrator.update(dy)
        self.theta = self.theta_integrator.update(dtheta)

        return (self.x, self.y, self.theta)
    

    def update_and_get_coarse_matching(self, omega_l, omega_r) -> tuple:
        dx, dy, dtheta = self.__get_speed(omega_l, omega_r)
        
        prev_x, prev_y, prev_theta = self.x, self.y, self.theta
        self.x = self.x_integrator.update(dx)
        self.y = self.y_integrator.update(dy)
        self.theta = self.theta_integrator.update(dtheta)

        
        x_match = self.x - prev_x
        y_match = self.y - prev_y
        theta_match = self.theta - prev_theta

        return ((self.x, self.y, self.theta), (x_match, y_match, theta_match))

        

        
