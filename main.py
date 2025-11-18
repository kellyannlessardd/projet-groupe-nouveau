from machine import ADC, Pin
import time
from adc_reader import read_potentiometers, read_switch
from pencontrol import set_pen_state
from inverse_kinematics import cinematique_inverse

POS_X = -5
POS_Y = 20
LEN_E = 100
LEN_B = 100

if __name__ == "__main__":
    while True:
        x, y = read_potentiometers()
        set_pen_state(read_switch())
        alpha, beta = cinematique_inverse(POS_X, POS_Y, x, y, LEN_E, LEN_B)
        
        time.sleep(0.1)