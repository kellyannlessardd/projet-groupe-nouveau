from machine import ADC, Pin
import time
from adc_reader import read_potentiometers, read_switch
from pencontrol import set_pen_state, auto_state_update
from inverse_kinematics import cinematique_inverse
from pwm_controllergroupe import PWMController
from Global_Variables import POS_X, POS_Y, LEN_E, LEN_B
from gcode_reader import read_file

pins = { "shoulder": 0, "elbow": 1 }
pwm_controller = PWMController(pins)

def main(pwm_controller):
    while True:
        x, y = read_potentiometers()
        set_pen_state(read_switch())
        alpha, beta = cinematique_inverse(POS_X, POS_Y, x, y, LEN_E, LEN_B)
        pwm_controller.set_angle("shoulder", alpha)
        pwm_controller.set_angle("elbow", beta)
        time.sleep(0.05)

def self_plotter(file_name, pwm_controller):
    plot_info = read_file(file_name)
    for inst in plot_info:
        if inst[0] in ["M3", "M5"]:
            auto_state_update(inst[0])
            time.sleep(0.05)
        elif inst[0] == "G1":
            pwm_controller.set_angle("shoulder", float(inst[1][1:]))
            time.sleep(0.1)
            pwm_controller.set_angle("elbow", float(inst[2][1:]))
        elif inst[0] == "M18":
            print("Fin du programe... ")


def menu():
    choice = int(input("Que voulez vous faire? \n1. Controller les bras a l'aide de potentiometres \n2. Faire dessiner une figure par le brachiographe\n Veillez entrer le numbero de votre choix"))
    if choice == 1:
        main(pwm_controller)
    elif choice == 2:
        file = input("Entrez le nom du fichier que vous voulez dessiner")
        self_plotter(file, pwm_controller)
    else: 
        print("Choix non reconnu")


if __name__ == "__main__":
    main(pwm_controller)
    #self_plotter("circle.gcode", pwm_controller)
    
