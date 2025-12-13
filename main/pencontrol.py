from machine import Pin, PWM

Servo_stylo = PWM(Pin(2))
Servo_stylo.freq(50)

def traduit(angle: float) -> int:
    """
    Convertit un angle en degrés vers l'entrée correspondante
    pour la méthode duty_u16 de la classe servo

    Voir https://docs.micropython.org/en/latest/library/machine.PWM.html pour plus
    de détails sur la méthode duty_u16
    """
    
    if angle < 0:
        angle = 0
    elif angle > 180:
        angle = 180 
    y = ((2000/180)*angle) + 500
    z = (65535/20000)*y
    return int(z)

def set_pen_state(state):
    """
    Contrôle l'état du stylo (haut/bas).
    
    Args:
        state: True pour stylo baissé, False pour stylo levé
    """
    if state == True:
        Servo_stylo.duty_u16(traduit(0))  # Position stylo baissé
    elif state == False:
        Servo_stylo.duty_u16(traduit(10))  # Position stylo levé
    else:
        raise ValueError("Invalid state. Use True or False.")

def auto_state_update(inst):
    """
    Met à jour l'état du stylo selon une instruction G-code.
    
    Args:
        inst: Instruction G-code ("M5" pour baisser, "M3" pour lever)
    """
    if inst == "M5":
        Servo_stylo.duty_u16(traduit(0))  # Stylo baissé
    elif inst == "M3":
        Servo_stylo.duty_u16(traduit(10))  # Stylo levé