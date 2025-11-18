from machine import ADC, Pin
import time
from Global_Variables import PAGE_LEN, PAGE_WID

pot_x = ADC(Pin(27))
pot_y = ADC(Pin(26))

switch = Pin(22, Pin.IN, Pin.PULL_DOWN)

# --- État mémoire du stylo (False = haut, True = bas) ---
pen_state = False
# Conserver la dernière valeur lue pour détecter les fronts (0 -> 1)
last_switch_value = switch.value()  # lire l'état réel au démarrage


def read_potentiometers():
    """
    Lit les deux potentiomètres X et Y.
    Retourne (x, y) mis à l'échelle.
    """
    x = pot_x.read_u16()
    y = pot_y.read_u16()

    # Mise à l'échelle linéaire depuis [0, 65535] vers [min, max]
    scaled_x = x * (PAGE_WID[1] - PAGE_WID[0]) / 65535 + PAGE_WID[0]
    scaled_y = y * (PAGE_LEN[1] - PAGE_LEN[0]) / 65535 + PAGE_LEN[0]

    return scaled_x, scaled_y


def read_switch():
    """
    Bascule pen_state à chaque appui (front 0->1) avec un petit anti-rebond.
    """
    global pen_state, last_switch_value

    current = switch.value()

    # front montant : 0 -> 1
    if last_switch_value == 0 and current == 1:
        # petit anti-rebond
        time.sleep_ms(20)
        # Relire pour confirmer que l'état est toujours à 1
        if switch.value() == 1:
            pen_state = not pen_state

    # Mémoriser la lecture courante pour la prochaine détection de front
    last_switch_value = current
    return pen_state

