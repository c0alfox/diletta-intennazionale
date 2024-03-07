from inventorhatmini import InventorHATMini
from ioexpander.common import PID

from typing import Tuple
import math

class Motor:

    def __init__(self, updates_per_second: int, updates_per_move: int,
                 board: InventorHATMini, motor_code: int, direction: int, 
                 speed_scale: float, extent: float, gains: Tuple[float, float, float]):
        
        """
        Instantiates a PID-enabled motor

        :param updates_per_second: int. The number of updates the PID is recalculated per second.
        :param updates_per_move: int. The number of update calls required to change the velocity.
        :param board: InventorHATMini. The board object connected to the raspberry pi.
        :param motor_code: MOTOR_A or MOTOR_B from inventorhatmini, the code for the motor and the encoder.
        :param direction: NORMAL_DIR or REVERSED_DIR from ioexpander.common, the direction of the motor.
        :param speed_scale: the scaling to apply to the motor's speed to match its real output
        :param extent: how far from zero to drive the motor at, in revolutions per second
        :param gains: Tuple[float, float, float]. In order, the proportional, integral and derivative gains
        """


        self.motor = board.motors[motor_code]
        self.encoder = board.encoders[motor_code]

        self.motor.direction(direction)
        self.encoder.direction(direction)

        self.motor.speed_scale(speed_scale)

        self.update_rate = 1 / updates_per_second
        self.updates_per_move = updates_per_move
        self.pid = PID(*gains, self.update_rate)

        self.vel_extent = extent

        self.update_count = 0
        self.start_value = 0
        self.end_value = 0

    def enable(self):
        self.motor.enable()

    def disable(self):
        self.motor.disable()

    def stop(self):
        self.end_value = 0

    def hard_stop(self):
        self.start_value = 0
        self.end_value = 0
        self.motor.speed(0)

    def set_speed(self, value):
        self.end_value = max(-self.vel_extent, min(self.vel_extent, value))

    def update(self):
        capture = self.encoder.capture()

        percent_along = min(self.update_count / self.updates_per_move, 1.0)

        self.pid.setpoint = (((-math.cos(percent_along * math.pi) + 1.0) / 2.0) * (self.end_value - self.start_value)) + self.start_value
        accel = self.pid.calculate(capture.revolutions_per_second)

        self.motor.speed(self.motor.speed() + accel * self.update_rate)

        self.update_count += 1

        if self.update_count >= self.updates_per_move:
            self.update_count = 0
            self.start_value = self.end_value