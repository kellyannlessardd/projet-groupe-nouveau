from machine import Pin, PWM

Servo_stylo = PWM(pin(13))
servo_style.freq(50)

def set_pen_state(state):
    if state == "down":
        Servo_stylo.duty_u16(6500)  # Position for pen down
    elif state == "up":
        Servo_stylo.duty_u16(3000)  # Position for pen up
    else:
        raise ValueError("Invalid state. Use 'up' or 'down'.")

