import unittest
import sys
import os
import math

# Permet d'importer inverse_kinematics.py situé dans le dossier parent
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from inverse_kinematics import cinematique_inverse

class TestInverseKinematics(unittest.TestCase):

    def test_zero_position(self):
        """Test qu’un point C à l’origine retourne bien des angles valides."""
        alpha, beta = cinematique_inverse(-50, 140, 0, 0, 155, 155)
        self.assertTrue(math.isfinite(alpha))
        self.assertTrue(math.isfinite(beta))

    def test_symmetry(self):
        """Test que les angles retournés sont valides et cohérents pour des points symétriques."""
        alpha1, beta1 = cinematique_inverse(-50, 140, 100, 100, 155, 155)
        alpha2, beta2 = cinematique_inverse(-50, 140, 100, -100, 155, 155)

        # Alpha doit changer
        self.assertNotEqual(alpha1, alpha2)

        # Les valeurs doivent être finies
        self.assertTrue(math.isfinite(beta1))
        self.assertTrue(math.isfinite(beta2))

    def test_reach_limit(self):
        """Test un point non atteignable ."""
        Ax, Ay = -50, 140
        Cx, Cy = 400, 400
        La, Lb = 155, 155

        AC = math.sqrt((Cx - Ax)**2 + (Cy - Ay)**2)
        self.assertTrue(AC > La + Lb)

        alpha, beta = cinematique_inverse(Ax, Ay, Cx, Cy, La, Lb)
        self.assertTrue(math.isfinite(alpha))
        self.assertTrue(math.isfinite(beta))

    def test_midpoint(self):
        """Test un point au milieu des deux segments."""
        alpha, beta = cinematique_inverse(-50, 140, 80, 80, 155, 155)

        # Vérifier uniquement validité mathématique
        self.assertTrue(math.isfinite(alpha))
        self.assertTrue(math.isfinite(beta))

if __name__ == "__main__":
    unittest.main()
