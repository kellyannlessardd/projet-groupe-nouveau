from machine import ADC, Pin
import time

PAGE_LEN = [-40, 40]
PAGE_WID = [0, 20]
pot_x = ADC(Pin(27))
pot_y = ADC(Pin(26))

switch = Pin(16, Pin.IN, Pin.PULL_UP)

# --- Etat mémoire du stylo (False = haut, True = bas) ---
pen_state = False
last_switch_value = 1  # Avec PULL_UP, repos = 1


def read_potentiometers():
    """
    Lit les deux potentiomètres X et Y.
    Retourne (x, y) sous forme de valeurs ADC (0 à 65535).
    """
    x = pot_x.read_u16()
    y = pot_y.read_u16()
    scaled_x = (x/65535)*(PAGE_WID[1]-PAGE_WID[0]) - PAGE_WID[0]
    scaled_y = (y/65535)*abs((PAGE_LEN[1]-PAGE_LEN[0])) + PAGE_LEN[0]
    return scaled_x, scaled_y


def read_switch():
    """
    Modifie l'état du stylo à chaque pression sur l'interrupteur.
    Retourne l'état actuel du stylo : True = bas, False = haut.
    """
    global pen_state, last_switch_value

    current_value = switch.value()

    # Détection du front descendant (1 → 0 = bouton pressé)
    if last_switch_value == 1 and current_value == 0:
        pen_state = not pen_state  # Toggle de l'état

    # Mise à jour du précédent état
    last_switch_value = current_value

    return pen_state

if __name__ == "__main__":
    while True:
        print(read_potentiometers())
        time.sleep(2)