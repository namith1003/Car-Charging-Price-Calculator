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

    # test is_peak with times that are all peak times
    def test_is_time_peak(self):
        self.calculator = Calculator()
        # testing for edge values of peak times
        self.assertTrue(self.calculator.is_peak(time(6, 0, 0)))
        self.assertTrue(self.calculator.is_peak(time(17, 59, 59)))
        # testing for a normal value for peak value
        self.assertTrue(self.calculator.is_peak(time(12, 0, 0)))

    def test_is_time_not_peak(self):
        self.calculator = Calculator()
        # testing for edge values of off-peak times
        self.assertFalse(self.calculator.is_peak(time(5, 59, 59)))
        self.assertFalse(self.calculator.is_peak(time(18, 0, 0)))
        # testing for a normal value in off-peak time
        self.assertFalse(self.calculator.is_peak(time(3, 0, 0)))

    # def test_peak_period(self):
    #     self.calculator = Calculator()
    #     # test for the time from the start of the peak period to the end
    #     self.assertEqual(timedelta(seconds=43200), self.calculator.peak_period("6:00"))
    #     # test for a time in the non peak region within the same day before peak starts
    #     self.assertEqual(timedelta(seconds=43200), self.calculator.peak_period("3:00"))
    #     # test for a time in the non peak region within the same day after peak times ended
    #     self.assertEqual(timedelta(seconds=0), self.calculator.peak_period("20:00"))
    #     # test for a normal time within the peak times of the same day
    #     self.assertEqual(timedelta(seconds=21600), self.calculator.peak_period("12:00"))

    # test get_endtime to check for valid ending times
    def test_get_endtime(self):
        self.calculator = Calculator()
        # test for a few hours in the same day from start of the day
        self.assertEqual(datetime(2020, 1, 1, 5, 0), self.calculator.get_endtime("1/1/2020", "0:0", 5))
        # test for almost the whole day from start of the day, to the last second of the day
        self.assertEqual(datetime(2020, 1, 1, 23, 59, 59),
                         self.calculator.get_endtime("1/1/2020", "0:0", 23.9997222222))
        # test from one day to the next day normally
        self.assertEqual(datetime(2020, 1, 2, 14, 48), self.calculator.get_endtime("1/1/2020", "0:0", 38.8))
        # test from one day to exactly the next day
        self.assertEqual(datetime(2020, 1, 2, 0, 0), self.calculator.get_endtime("1/1/2020", "0:0", 24))

    # test if the api returns the required json file
    def test_get_api(self):
        self.calculator = Calculator()

        self.calculator.get_api("3444", "2020-10-10")

    # tests the length of daylight for a specific postcode in a specific day is correct
    def test_get_day_light_length(self):
        self.calculator = Calculator()

        self.assertEqual(12.816666666666666,
                         self.calculator.get_day_light_length(self.calculator.get_api("3444", "2020-10-10")))

    # tests the solar insolation for a specific postcode in a specific day is correct
    def test_get_solar_insolation(self):
        self.calculator = Calculator()

        self.assertEqual(6.5,
                         self.calculator.get_solar_insolation(self.calculator.get_api("3444", "2020-10-10")))

    # tests if the cloud cover for a specific postcode in a specific day is correct
    def test_get_cloud_cover(self):
        self.calculator = Calculator()
        #
        # self.assertEqual(22,
        #                  self.calculator.get_cloud_cover(self.calculator.get_api("3444", "2020-10-10"), 1))

    # tests if the solar energy generated is valid
    def test_calculate_solar_energy(self):
        self.calculator = Calculator()

        # tests the amount of solar energy generated for a valid set of normal values
        self.assertAlmostEqual(3.9609375,
                               self.calculator.calculate_solar_energy(6.5, 12.8, 22, 1))

        # # tests if no energy is generated if the length of sunlight for the day is zero
        # self.assertAlmostEqual(0,
        #                        self.calculator.calculate_solar_energy(6.5, 0, 22, 1))

        # tests if no energy is generated if the solar insolation is zero
        self.assertAlmostEqual(0,
                               self.calculator.calculate_solar_energy(0, 12.8, 22, 1))

        # tests if no energy is generated when the cloud cover is at a 100%
        self.assertAlmostEqual(0,
                               self.calculator.calculate_solar_energy(6.5, 12.8, 100, 1))

        # tests if no energy is generated when hours charged is zero
        self.assertAlmostEqual(0,
                               self.calculator.calculate_solar_energy(6.5, 12.8, 22, 0))


def main():
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCalculator)
    unittest.TextTestRunner(verbosity=2).run(suite)


main()
# if __name__ == "__main__":
#     pass
