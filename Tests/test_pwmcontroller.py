from pwm_controllergroupe import PWMController
import unittest


class TestPWMController(unittest.TestCase):

    def setUp(self):
        self.ctrl = PWMController({"servo": 1})

    def test_angle_to_duty_limits(self):
        duty_min = self.ctrl.angle_to_duty(-10)
        expected_min = int((MIN_US / PERIOD_US) * 65535)
        self.assertEqual(duty_min, expected_min)

        duty_max = self.ctrl.angle_to_duty(200)
        expected_max = int((MAX_US / PERIOD_US) * 65535)
        self.assertEqual(duty_max, expected_max)

    def test_angle_to_duty_midpoint(self):
        duty_90 = self.ctrl.angle_to_duty(90)
        expected_pulse = MIN_US + (90 / 180) * (MAX_US - MIN_US)
        expected_duty = int((expected_pulse / PERIOD_US) * 65535)
        self.assertEqual(duty_90, expected_duty)

    def test_set_angle_calls_pwm(self):
        self.ctrl.set_angle("servo", 45)
        expected_duty = self.ctrl.angle_to_duty(45)
        self.assertEqual(self.ctrl.servos["servo"].last_duty, expected_duty)
        self.assertEqual(self.ctrl.servos["servo"]._freq, FREQ)


if __name__ == "__main__":
    unittest.main()
