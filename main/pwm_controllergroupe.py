# pwm_controller.py
from machine import Pin, PWM
from Global_Variables import FREQ, MIN_US, MAX_US, PERIOD_US

class PWMController:
    """
    Contrôleur PWM pour gérer les servomoteurs du brachiographe.
    """
    def __init__(self, pins):
        """
        Initialise les servomoteurs sur les pins spécifiés.
        
        Args:
            pins: Dictionnaire { "shoulder": 15, "elbow": 16, "pen": 17 }
        """
        self.servos = {}
        for name, pin_num in pins.items():
            pwm = PWM(Pin(pin_num))
            pwm.freq(FREQ)
            self.servos[name] = pwm

    def angle_to_duty(self, angle):
        """
        Convertit un angle en degrés vers une valeur duty cycle 16 bits.
        
        Args:
            angle: Angle en degrés (0-180)
            
        Returns:
            int: Valeur duty cycle 16 bits
        """
        # Limiter l'angle entre 0 et 180
        angle = max(0, min(180, angle))
        # Calcul largeur impulsion
        pulse = MIN_US + (angle / 180) * (MAX_US - MIN_US)
        # Conversion en duty 16 bits
        duty = int((pulse / PERIOD_US) * 65535)
        return duty

    def set_angle(self, servo_name, angle):
        """
        Définit l'angle d'un servomoteur.
        
        Args:
            servo_name: Nom du servomoteur ("shoulder", "elbow", etc.)
            angle: Angle en degrés (0-180)
        """
        duty = self.angle_to_duty(angle)
        self.servos[servo_name].duty_u16(duty)

