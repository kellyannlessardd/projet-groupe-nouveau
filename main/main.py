from machine import ADC, Pin
import time
from adc_reader import read_potentiometers, read_switch
from pencontrol import set_pen_state, auto_state_update
from inverse_kinematics import cinematique_inverse
from pwm_controllergroupe import PWMController
from Global_Variables import POS_X, POS_Y, LEN_E, LEN_B, SPEED
from gcode_reader import read_file, circles, squares

pins = { "shoulder": 0, "elbow": 1 }
pwm_controller = PWMController(pins)

def main(pwm_controller):
    print("Amusez vous bien!")
    while True:
        x, y = read_potentiometers()
        set_pen_state(read_switch())
        alpha, beta = cinematique_inverse(POS_X, POS_Y, x, y, LEN_E, LEN_B)
        pwm_controller.set_angle("shoulder", alpha)
        pwm_controller.set_angle("elbow", beta)
        time.sleep(SPEED)

def self_plotter(file_name, fn, pwm_controller):
    if fn == "cercle":
        circles(file_name, 50, 0.1, 50, 5, 100, 140)
    elif fn == "square":
        squares(file_name, 50, 100, 10)

    plot_info = read_file(file_name)
    print("Plotting...")
    for inst in plot_info:
        if inst[0] in ["M3", "M5"]:
            auto_state_update(inst[0])
            time.sleep(SPEED)
        elif inst[0] == "G1":
            pwm_controller.set_angle("shoulder", float(inst[1][1:]))
            time.sleep(SPEED)
            pwm_controller.set_angle("elbow", float(inst[2][1:]))
        elif inst[0] == "M18":
            print("Fin du programe... ")


def menu():
    choice = int(input("Que voulez vous faire? \n1. Controller les bras a l'aide de potentiometres \n2. Faire dessiner une figure par le brachiographe\n Veillez entrer le numbero de votre choix\n"))
    if choice == 1:
        main(pwm_controller)
    elif choice == 2:
        figure = int(input("Quelle figure voulez vous dessiner? \n1. Des cercles? ou\n2. Des carres?\n"))
        if figure == 1: 
            self_plotter("self_plot.gcode","cercle", pwm_controller)
        elif figure == 2:
            self_plotter("self_plot.gcode","square", pwm_controller)
    else: 
        print("Choix non reconnu")


if __name__ == "__main__":
    menu()
    