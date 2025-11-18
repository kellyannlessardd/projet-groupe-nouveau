from machine import ADC, Pin
import time
from adc_reader import read_potentiometers, read_switch
from pencontrol import set_pen_state
from inverse_kinematics import cinematique_inverse
from pwm_controllergroupe import PWMController
from Global_Variables import POS_X, POS_Y, LEN_E, LEN_B

pins = { "shoulder": 1, "elbow": 2 }

if __name__ == "__main__":
    while True:
        x, y = read_potentiometers()
        set_pen_state(read_switch())
        alpha, beta = cinematique_inverse(POS_X, POS_Y, x, y, LEN_E, LEN_B)

        pwm_controller = PWMController(pins)
        pwm_controller.set_angle("shoulder", alpha)
        pwm_controller.set_angle("elbow", beta)
        time.sleep(0.1)