# Variables principales du brachiographe
POS_X = -50  # Position X du pivot
POS_Y = 140  # Position Y du pivot
LEN_E = 155  # Longueur du bras avant (elbow)
LEN_B = 155  # Longueur du bras arrière (shoulder)
SPEED = 0.5  # Délai entre les mouvements (secondes)

# Dimensions de la page pour l'ADC
PAGE_LEN = [0, 300]  # Longueur de la page (mm)
PAGE_WID = [0, 225]  # Largeur de la page (mm)

# Configuration PWM pour les servomoteurs
FREQ = 50          # Fréquence PWM en Hz (20 ms période)
MIN_US = 500       # Largeur impulsion min (0°)
MAX_US = 2500      # Largeur impulsion max (180°)
PERIOD_US = 20000  # Période en microsecondes (1/50 Hz)