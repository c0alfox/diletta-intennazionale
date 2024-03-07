import time
import threading

from modules import MotorController

UPDATES = 100                           # How many times to update the motor per second
UPDATE_RATE = 1 / UPDATES
TIME_FOR_EACH_MOVE = 1                  # The time to travel between each random value, in seconds
UPDATES_PER_MOVE = TIME_FOR_EACH_MOVE * UPDATES

mc = MotorController(298, UPDATES, UPDATES_PER_MOVE)


def sleep_until(end_time):
    time_to_sleep = end_time - time.monotonic()
    if time_to_sleep > 0.0:
        time.sleep(time_to_sleep)


def test_values():
    values = [
        (-1,  1), # Turn left
        ( 1, -1), # Turn right
        ( 1,  1), # Go forwards
        (-1, -1)  # Go backwards
    ]

    i = 0

    mc.set_speed(*values[1])

    while True:
        mc.set_speed(*values[i])

        i += 1
        i %= 4

        time.sleep(1.5)

        mc.hard_stop()
        time.sleep(1)


t = threading.Thread(target=test_values, daemon=True)
t.start()

try: 
    while not mc.board.switch_pressed():
        start_time = time.monotonic()

        mc.update()

        sleep_until(start_time + UPDATE_RATE)
finally:
    del mc