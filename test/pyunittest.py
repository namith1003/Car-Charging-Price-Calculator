from app.calculator import *
import unittest

class TestCalculator(unittest.TestCase):

    # you may create more test methods
    # you may add parameters to test methods
    # this is an example
    def test_cost(self):
        self.calculator = Calculator()
        self.assertEqual(self.calculator.cost_calculation("", "", "", "", ""), "")

    # you may create test suite if needed
    if __name__ == "__main__":
        pass
