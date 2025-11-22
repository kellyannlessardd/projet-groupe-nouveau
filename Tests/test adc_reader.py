import adc_reader
# Test 1 : Scaling des potentiomètres

def test_read_potentiometers():
    #Simule des valeurs de l'ADC
    adc_reader.pot_x.read_u16 = lambda: 32767   #+-50%
    adc_reader.pot_y.read_u16 = lambda: 65535   # max

    x, y = adc_reader.read_potentiometers()

    print("Test potentiomètres :")
    print("X =", x, "(attendu ~10)")
    print("Y =", y, "(attendu ~40)")
    print()


# Test 2 : Basculer le switch
def test_read_switch():
    print("Test switch :")

    # Cas 0 -> 1 : doit basculer
    adc_reader.switch.value = lambda: 0
    adc_reader.last_switch_value = 0
    adc_reader.pen_state = False

    adc_reader.switch.value = lambda: 1
    r = adc_reader.read_switch()
    print("0 -> 1, attendu True, obtenu :", r)

    # Cas 1 -> 1 : rien ne change
    adc_reader.switch.value = lambda: 1
    r = adc_reader.read_switch()
    print("1 -> 1, attendu True, obtenu :", r)

    # Cas 1 -> 0 : rien ne change
    adc_reader.switch.value = lambda: 0
    r = adc_reader.read_switch()
    print("1 -> 0, attendu True, obtenu :", r)

    print()



# Lancer les tests
test_read_potentiometers()
test_read_switch()
