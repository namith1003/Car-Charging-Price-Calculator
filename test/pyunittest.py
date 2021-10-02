from app.calculator import *
import unittest


# from unittest.mock import Mock


class TestCalculator(unittest.TestCase):

    # you may create more test methods
    # you may add parameters to test methods
    # this is an example
    def test_cost(self):
        self.calculator = Calculator()
        self.assertRaises(TypeError, self.calculator.cost_calculation, "", "", "", "", "")
        # self.assertEqual(self.calculator.cost_calculation("", "", "", "", ""), "")

    # testing cost_calculation for all branches with constant net value of 10 and base_price of 5
    def test_correct_input_cost_peak_no_holiday(self):
        self.calculator = Calculator()
        self.assertEqual(0.5, self.calculator.cost_calculation(10, 5, True, False))

    # you may create test suite if needed
    def test_correct_input_cost_no_peak_holiday(self):
        self.calculator = Calculator()
        self.assertAlmostEqual(0.275, self.calculator.cost_calculation(10, 5, False, True))

    def test_correct_input_cost_no_peak_no_holiday(self):
        self.calculator = Calculator()
        self.assertAlmostEqual(0.25, self.calculator.cost_calculation(10, 5, False, False))

    def test_correct_input_cost_peak_holiday(self):
        self.calculator = Calculator()
        self.assertAlmostEqual(0.55, self.calculator.cost_calculation(10, 5, True, True))

    # testing the time_calculation method using initial_charge of 0, final_charge of 72
    # capacity of 100kwh and power of 7.2 kw assuming charging configuration of 3
    def test_correct_time_calculation(self):
        self.calculator = Calculator()
        self.assertEqual(10, self.calculator.time_calculation(0, 72, 100, 7.2))

    # test is_holiday method with the date 25/12/2020 which is a valid holiday christmas
    def test_is_date_holiday(self):
        self.calculator = Calculator()
        self.assertTrue(self.calculator.is_holiday(datetime(2020, 12, 25)))

    # test is_holiday method with the date 20/12/2020 which is not a holiday
    def test_is_date_not_holiday(self):
        self.calculator = Calculator()
        self.assertTrue(self.calculator.is_holiday(datetime(2020, 12, 20)))

    def test_is_time_peak(self):
        self.calculator = Calculator("3333", "10/10/2020")


def main():
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCalculator)
    unittest.TextTestRunner(verbosity=2).run(suite)


main()
# if __name__ == "__main__":
#     pass
