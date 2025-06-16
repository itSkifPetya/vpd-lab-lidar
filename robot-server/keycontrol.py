import termios
import tty
import sys
import ev3dev2.motor

class KeyController:
    def __init__(self, left_motor, right_motor, forward_cycle = 100, turn_cycle = 80):
        self.LEFT_MOTOR = left_motor
        self.RIGHT_MOTOR = right_motor
        try:
            self.forward_cycle = forward_cycle
        except Exception:
            print("Incorrect forward_cycle")
        try:
            self.turn_cycle = turn_cycle
        except Exception:
            print("Incorrect turn_cycle")

    def __get_char(self):
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch
    
    def __forward(self):
        self.LEFT_MOTOR.run_direct(duty_cycle_sp = self.forward_cycle)
        self.RIGHT_MOTOR.run_direct(duty_cycle_sp = self.forward_cycle)   

    def __backward(self):
        self.LEFT_MOTOR.run_direct(duty_cycle_sp = -self.forward_cycle)
        self.RIGHT_MOTOR.run_direct(duty_cycle_sp = -self.forward_cycle)

    def __left(self):
        self.LEFT_MOTOR.run_direct(duty_cycle_sp = -self.turn_cycle)
        self.RIGHT_MOTOR.run_direct(duty_cycle_sp = self.turn_cycle)   

    def __right(self):
        self.LEFT_MOTOR.run_direct(duty_cycle_sp = self.turn_cycle)
        self.RIGHT_MOTOR.run_direct(duty_cycle_sp = -self.turn_cycle)      
    
    def __stop(self):
        self.LEFT_MOTOR.run_direct(duty_cycle_sp = 0)
        self.RIGHT_MOTOR.run_direct(duty_cycle_sp = 0)   

    def control(self):
        k = self.__get_char()
        print(k)
        if k == 'w':
            self.__forward()
        if k == 's':
            self.__backward()
        if k == 'a':
            self.__left()
        if k == 'd':
            self.__right()
        if k == ' ':
            self.__stop()
        if k == 'q':
            return True
        return False