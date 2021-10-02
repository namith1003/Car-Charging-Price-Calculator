from app.calculator import *
import unittest
# from unittest.mock import Mock


class TestCalculator(unittest.TestCase):

    # you may create more test methods
    # you may add parameters to test methods
    # this is an example
    def test_cost(self):
        self.calculator = Calculator("3333", "10/10/2020")
        self.assertRaises(TypeError, self.calculator.cost_calculation, "", "", "", "", "")
        # self.assertEqual(self.calculator.cost_calculation("", "", "", "", ""), "")

    def test_correct_input_cost_peak_no_holiday(self):
        self.calculator = Calculator("3333", "10/10/2020")
        self.assertEqual(5, self.calculator.cost_calculation(10, 50, True, False))


    # you may create test suite if needed
    def test_correct_input_cost_no_peak_holiday(self):
        self.calculator = Calculator("3333", "10/10/2020")
        self.assertAlmostEqual(2.75, self.calculator.cost_calculation(10, 50, False, True))


def main():
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCalculator)
    unittest.TextTestRunner(verbosity=2).run(suite)


main()
# if __name__ == "__main__":
#     pass
