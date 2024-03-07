import cv2
import time

from modules import *

params = Params("overrides.json")

camera = picamera_init(params.frame_size)
line_vision = LineVision(params)
motor_controller = MotorController(params)
Gyroscope()


@timeable
def loop():
    image = camera.capture_array()
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    image, error, angle, intr, detected = line_vision.evaluate(image)

    if params.display_frame:
        cv2.imshow("image", image)

    dx_perc, sx_perc, steer = motor_controller.move(error, angle, intr, detected)
    # print(f"dx: {dx_perc} - sx: {sx_perc} // steering: {steer}")
    motor_controller.set_speed(sx_perc, dx_perc)

    if cv2.waitKey(1) & 0xff == ord('q'):
        return False

    return True


def main():
    cond = True
    execute = False

    while cond:
            
        if motor_controller.board.switch_pressed():
            print(f"Switch pressed old exec: {execute}")
            line_vision.redline = False
            execute = not execute
            motor_controller.stop()
            time.sleep(1)
        
        if not execute:
            continue

        delta, cond = loop()
        if params.print_fps:
            print(f"[FPS] {int(1/delta)}")

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
