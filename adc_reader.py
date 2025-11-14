from machine import ADC, Pin

# Potentiomètres
pot_x = ADC(26)
pot_y = ADC(27)

# Interrupteur (stylo)
switch = Pin(16, Pin.IN, Pin.PULL_UP)

def read_potentiometers():
    """
    Lit les deux potentiomètres et retourne X et Y.
    Retourne : (x, y) entre 0 et 65535.
    """
    x = pot_x.read_u16()
    y = pot_y.read_u16()
    return x, y

def read_switch():
    """
    Retourne l'état du stylo.
    True  -> stylo en bas
    False -> stylo en haut
    """
    return switch.value() == 0
