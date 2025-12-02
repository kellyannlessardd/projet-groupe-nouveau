import unittest
from unittest.mock import MagicMock
import sys
import pathlib
from importlib import import_module

# Ajoute le répertoire main au chemin pour importer pencontrol
main_dir = str(pathlib.Path(__file__).parent.parent / 'main')
if main_dir not in sys.path:
    sys.path.insert(0, main_dir)

# Mock du module machine avant d'importer pencontrol
sys.modules['machine'] = MagicMock()

# Importe pencontrol en utilisant importlib pour éviter les erreurs Pylance
pencontrol = import_module('pencontrol')


class TestPenControl(unittest.TestCase):
    """Tests pour les fonctions du module pencontrol.py"""
    
    def setUp(self):
        """Configuration avant chaque test - Mock l'objet Servo_stylo"""
        # Mock de l'objet Servo_stylo
        self.mock_servo = MagicMock()
        pencontrol.Servo_stylo = self.mock_servo
    
    def tearDown(self):
        """Nettoyage après chaque test"""
        pass
    
    # Tests pour la fonction traduit()
    def test_traduit_angle_normal(self):
        """Test de la fonction traduit avec un angle de 90 degrés"""
        result = pencontrol.traduit(90)
        y = ((2000/180) * 90) + 500
        expected = int((65535/20000) * y)
        self.assertEqual(result, expected)
    
    # Tests pour la fonction set_pen_state()
    def test_set_pen_state_true(self):
        """Test de set_pen_state avec state=True (stylo baissé)"""
        pencontrol.set_pen_state(True)
        self.mock_servo.duty_u16.assert_called_once()
    
    def test_set_pen_state_false(self):
        """Test de set_pen_state avec state=False (stylo levé)"""
        pencontrol.set_pen_state(False)
        self.mock_servo.duty_u16.assert_called_once()
    
    # Tests pour la fonction auto_state_update()
    def test_auto_state_update_m5(self):
        """Test de auto_state_update avec instruction M5"""
        pencontrol.auto_state_update("M5")
        self.mock_servo.duty_u16.assert_called_once()
    
    def test_auto_state_update_m3(self):
        """Test de auto_state_update avec instruction M3"""
        pencontrol.auto_state_update("M3")
        self.mock_servo.duty_u16.assert_called_once()


if __name__ == '__main__':
    # Exécuter les tests avec verbosité
    unittest.main(verbosity=2)
