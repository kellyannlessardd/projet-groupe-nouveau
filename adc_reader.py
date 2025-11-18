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

# Add these at module level
prev_x = None
prev_y = None
alpha = 1  # smoothing factor (0.0 = no smoothing, 1.0 = instant change)

def read_potentiometers():
    global prev_x, prev_y
    raw_x = pot_x.read_u16()
    raw_y = pot_y.read_u16()

    scaled_x = raw_x * (PAGE_WID[1] - PAGE_WID[0]) / 65535 + PAGE_WID[0]
    scaled_y = raw_y * (PAGE_LEN[1] - PAGE_LEN[0]) / 65535 + PAGE_LEN[0]

    if prev_x is None:
        prev_x = scaled_x
        prev_y = scaled_y

    # Apply exponential smoothing
    smoothed_x = alpha * scaled_x + (1 - alpha) * prev_x
    smoothed_y = alpha * scaled_y + (1 - alpha) * prev_y

    prev_x = smoothed_x
    prev_y = smoothed_y

    return smoothed_x, smoothed_y


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

