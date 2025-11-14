# pwm_controller.py
from machine import Pin, PWM

# Constantes pour les servos
FREQ = 50          # fréquence PWM en Hz (20 ms période)
MIN_US = 500       # largeur impulsion min (0°)
MAX_US = 2500      # largeur impulsion max (180°)
PERIOD_US = 20000  # période en microsecondes (1/50 Hz)

class PWMController:
    def __init__(self, pins):
        """
        pins : dictionnaire { "shoulder": 15, "elbow": 16, "pen": 17 }
        """
        self.servos = {}
        for name, pin_num in pins.items():
            pwm = PWM(Pin(pin_num))
            pwm.freq(FREQ)
            self.servos[name] = pwm

    def angle_to_duty(self, angle):
        # Limiter l'angle entre 0 et 180
        angle = max(0, min(180, angle))
        # Calcul largeur impulsion
        pulse = MIN_US + (angle / 180) * (MAX_US - MIN_US)
        # Conversion en duty 16 bits
        duty = int((pulse / PERIOD_US) * 65535)
        return duty

    def set_angle(self, servo_name, angle):
        duty = self.angle_to_duty(angle)
        self.servos[servo_name].duty_u16(duty)