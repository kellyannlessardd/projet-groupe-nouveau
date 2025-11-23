import unittest
from unittest.mock import patch
import adc_reader


class TestADCReader(unittest.TestCase):
    """
    Tests unitaires pour les fonctions du module adc_reader.
    Les objets matériels (ADC, Pin) sont simulés grâce à unittest.mock.
    """

    @patch("adc_reader.pot_x")
    @patch("adc_reader.pot_y")
    def test_read_potentiometers(self, mock_pot_y, mock_pot_x):
        """
        Vérifie que les valeurs lues par l'ADC sont correctement mises à l'échelle.
        """
        # Valeurs simulées
        mock_pot_x.read_u16.return_value = 32767   # ~50%
        mock_pot_y.read_u16.return_value = 65535   # max

        # Appel de la fonction
        x, y = adc_reader.read_potentiometers()

        # X doit être proche de 10
        self.assertAlmostEqual(x, 10, delta=0.5)

        # Y doit être proche de 40
        self.assertAlmostEqual(y, 40, delta=0.5)

    @patch("adc_reader.switch")
    @patch("adc_reader.time.sleep_ms")
    def test_read_switch_toggle(self, mock_sleep, mock_switch):
        """
        Vérifie qu’un front montant (0→1) bascule l'état du stylo.
        """
        mock_switch.value.side_effect = [0, 1]
        adc_reader.pen_state = False
        adc_reader.last_switch_value = 0

        result = adc_reader.read_switch()

        self.assertTrue(result)

    @patch("adc_reader.switch")
    @patch("adc_reader.time.sleep_ms")
    def test_read_switch_no_toggle(self, mock_sleep, mock_switch):
        """
        Si la valeur reste à 1, il ne doit pas y avoir de basculement.
        """
        mock_switch.value.return_value = 1
        adc_reader.pen_state = True
        adc_reader.last_switch_value = 1

        result = adc_reader.read_switch()

        self.assertTrue(result)

    @patch("adc_reader.switch")
    @patch("adc_reader.time.sleep_ms")
    def test_read_switch_multiple_sequence(self, mock_sleep, mock_switch):
        """
        Teste une séquence : 0→1 (toggle), 1→0 (rien), 0→1 (toggle)
        """
        mock_switch.value.side_effect = [0, 1, 0, 1]

        adc_reader.pen_state = False
        adc_reader.last_switch_value = 0

        r1 = adc_reader.read_switch()   # 0→1 toggle → True
        r2 = adc_reader.read_switch()   # 1→0 rien → True
        r3 = adc_reader.read_switch()   # 0→1 toggle → False

        self.assertTrue(r1)
        self.assertTrue(r2)
        self.assertFalse(r3)


if __name__ == "__main__":
    unittest.main()
