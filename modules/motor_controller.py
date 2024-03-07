from .motor import Motor

from inventorhatmini import InventorHATMini, MOTOR_A, MOTOR_B
from ioexpander.common import NORMAL_DIR, REVERSED_DIR

class MotorController:
    def __init__(self, gear_ratio, updates_per_second, updates_per_move):
        self.board = InventorHATMini(motor_gear_ratio=gear_ratio, init_leds=False)
        self.motor_left = Motor(updates_per_second, updates_per_move, self.board, MOTOR_B, REVERSED_DIR, 5.3, 1, (30.0, 0.0, 0.4))
        self.motor_right = Motor(updates_per_second, updates_per_move, self.board, MOTOR_A, NORMAL_DIR, 5.3, 1, (30.0, 0.0, 0.4))
        
        self.motor_left.enable()
        self.motor_right.enable()

    def __del__(self):
        self.hard_stop()
        self.motor_left.disable()
        self.motor_right.disable()

    def set_speed(self, left: float, right: float):
        self.motor_left.set_speed(left)
        self.motor_right.set_speed(right)
    
    def update(self):
        self.motor_left.update()
        self.motor_right.update()
    
    def hard_stop(self):
        self.motor_left.hard_stop()
        self.motor_right.hard_stop()

    def stop(self):
        self.motor_left.stop()
        self.motor_right.stop()