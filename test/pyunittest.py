from main import *
from app.calculator import *
import unittest

from unittest.mock import Mock


class TestCalculator(unittest.TestCase):

    def setUp(self) -> None:
        self.calculator = Calculator()
        # setup a mock calculator to perform api tasks
        self.test_calculator = Mock()
        # setup a mock api with valid hardcoded values to check behaviours
        self.test_calculator.get_api.return_value = {'date': '2020-10-10', 'sunrise': '05:45:00', 'sunset': '18:34:00',
                                                     'moonrise': '01:23:00', 'moonset': '11:01:00',
                                                     'moonPhase': 'Last Quarter', 'moonIlluminationPct': 38,
                                                     'minTempC': 5, 'maxTempC': 19, 'avgTempC': 14, 'sunHours': 6.5,
                                                     'uvIndex': 3,
                                                     'location': {'id': '1ee3e481-666e-486f-ba9e-ada53ca20292',
                                                                  'postcode': '3444', 'name': 'BARFOLD', 'state': 'VIC',
                                                                  'latitude': '-37.091944', 'longitude': '144.506111',
                                                                  'distanceToNearestWeatherStationMetres': 8164.202586320055,
                                                                  'nearestWeatherStation': {'name': 'REDESDALE',
                                                                                            'state': 'VIC',
                                                                                            'latitude': '-37.0194',
                                                                                            'longitude': '144.5203'}},
                                                     'hourlyWeatherHistory': [
                                                         {'hour': 0, 'tempC': 6, 'weatherDesc': 'Patchy rain possible',
                                                          'cloudCoverPct': 29, 'uvIndex': 1, 'windspeedKph': 7,
                                                          'windDirectionDeg': 248, 'windDirectionCompass': 'WSW',
                                                          'precipitationMm': 0, 'humidityPct': 95, 'visibilityKm': 5,
                                                          'pressureMb': 1020},
                                                     ]}

    # you may create more test methods
    # you may add parameters to test methods
    # this is an example
    def test_cost(self):
        self.assertRaises(TypeError, self.calculator.cost_calculation, "", "", "", "", "")
        # self.assertEqual(self.calculator.cost_calculation("", "", "", "", ""), "")

    # testing for invalid string inputs to cost_calculation function
    def test_string_input_cost_calculation(self):
        with self.assertRaises(TypeError):
            self.calculator.cost_calculation("hello", 5, True, False)
        with self.assertRaises(TypeError):
            self.calculator.cost_calculation(10, "hello", True, False)

    # testing cost_calculation for all branches with constant net value of 10 and base_price of 5
    def test_correct_input_cost_peak_no_holiday(self):
        self.assertEqual(0.5, self.calculator.cost_calculation(10, 5, True, False))

    # you may create test suite if needed
    def test_correct_input_cost_no_peak_holiday(self):
        self.assertAlmostEqual(0.275, self.calculator.cost_calculation(10, 5, False, True))

    def test_correct_input_cost_no_peak_no_holiday(self):
        self.assertAlmostEqual(0.25, self.calculator.cost_calculation(10, 5, False, False))

    def test_correct_input_cost_peak_holiday(self):
        self.assertAlmostEqual(0.55, self.calculator.cost_calculation(10, 5, True, True))

    # testing the time_calculation method using initial_charge of 0, final_charge of 72
    # capacity of 100kwh and power of 7.2 kw assuming charging configuration of 3
    def test_correct_time_calculation(self):
        self.assertEqual(10, self.calculator.time_calculation(0, 72, 100, 7.2))

    # testing for invalid string inputs to the time calculation
    def test_invalid_time_calculation(self):
        with self.assertRaises(ValueError):
            self.calculator.time_calculation("hi", 72, 100, 7.2)
        with self.assertRaises(ValueError):
            self.calculator.time_calculation(0, "hi", 100, 7.2)
        with self.assertRaises(ValueError):
            self.calculator.time_calculation(0, 72, "hi", 7.2)
        with self.assertRaises(TypeError):
            self.calculator.time_calculation(0, 72, 100, "hi")

    # test is_holiday method with the date 25/12/2020 which is a valid holiday christmas
    def test_is_date_holiday(self):
        self.assertTrue(self.calculator.is_holiday(datetime(2020, 12, 25)))

    # test is_holiday method with the date 20/12/2020 which is not a holiday
    def test_is_date_not_holiday(self):
        self.assertTrue(self.calculator.is_holiday(datetime(2020, 12, 20)))

    def test_is_invalid_date_holiday(self):
        with self.assertRaises(TypeError):
            self.calculator.is_holiday(datetime("year", 12, 20))
        with self.assertRaises(TypeError):
            self.calculator.is_holiday(datetime(2020, "month", 20))
        with self.assertRaises(TypeError):
            self.calculator.is_holiday(datetime(2020, 12, "day"))

    # test is_peak with times that are all peak times
    def test_is_time_peak(self):
        # testing for edge values of peak times
        self.assertTrue(self.calculator.is_peak(time(6, 0, 0)))
        self.assertTrue(self.calculator.is_peak(time(17, 59, 59)))
        # testing for a normal value for peak value
        self.assertTrue(self.calculator.is_peak(time(12, 0, 0)))

    def test_is_time_not_peak(self):
        # testing for edge values of off-peak times
        self.assertFalse(self.calculator.is_peak(time(5, 59, 59)))
        self.assertFalse(self.calculator.is_peak(time(18, 0, 0)))
        # testing for a normal value in off-peak time
        self.assertFalse(self.calculator.is_peak(time(3, 0, 0)))

    # test get_endtime to check for valid ending times
    def test_get_endtime(self):
        # test for a few hours in the same day from start of the day
        self.assertEqual(datetime(2020, 1, 1, 5, 0), self.calculator.get_endtime("1/1/2020", "0:0", 5))
        # test for almost the whole day from start of the day, to the last second of the day
        self.assertEqual(datetime(2020, 1, 1, 23, 59, 59),
                         self.calculator.get_endtime("1/1/2020", "0:0", 23.9997222222))
        # test from one day to the next day normally
        self.assertEqual(datetime(2020, 1, 2, 14, 48), self.calculator.get_endtime("1/1/2020", "0:0", 38.8))
        # test from one day to exactly the next day
        self.assertEqual(datetime(2020, 1, 2, 0, 0), self.calculator.get_endtime("1/1/2020", "0:0", 24))

    # Tests Below All Run Using The Mock Calculator and Mock Api

    # test if the api returns the required json file
    def test_get_api(self):
        api = self.test_calculator.get_api("3444", "2020-10-10")

        self.assertTrue(api['location']['postcode'] == "3444")
        self.assertTrue(api['date'] == "2020-10-10")

    # tests the length of daylight for a specific postcode in a specific day is correct
    def test_get_day_light_length(self):
        self.assertEqual(12.816666666666666,
                         self.calculator.get_day_light_length(self.test_calculator.get_api("3444", "2020-10-10")))

    # tests the solar insolation for a specific postcode in a specific day is correct
    def test_get_solar_insolation(self):
        self.assertEqual(6.5,
                         self.calculator.get_solar_insolation(self.test_calculator.get_api("3444", "2020-10-10")))

    # tests if the cloud cover for a specific postcode in a specific day is correct
    def test_get_cloud_cover(self):
        api = self.test_calculator.get_api("3444", "2020-10-10")

        self.assertEqual(29,
                         self.calculator.get_cloud_cover(api, 0))

    # tests if the solar energy generated is valid
    def test_calculate_solar_energy(self):
        # test with the mock calculator and mock apis results
        api = self.test_calculator.get_api("3444", "2020-10-10")
        si = self.calculator.get_solar_insolation(api)
        dl = self.calculator.get_day_light_length(api)
        cc = self.calculator.get_cloud_cover(api, 0)
        hour = 0.5

        self.assertAlmostEqual(1.80039012,
                               self.calculator.calculate_solar_energy(si, dl, cc, hour))

        # tests the amount of solar energy generated for a valid set of normal values
        self.assertAlmostEqual(3.9609375,
                               self.calculator.calculate_solar_energy(6.5, 12.8, 22, 1))

        # tests if no energy is generated if the length of sunlight for the day is zero
        self.assertAlmostEqual(0,
                               self.calculator.calculate_solar_energy(6.5, 0, 22, 1))

        # tests if no energy is generated if the solar insolation is zero
        self.assertAlmostEqual(0,
                               self.calculator.calculate_solar_energy(0, 12.8, 22, 1))

        # tests if no energy is generated when the cloud cover is at a 100%
        self.assertAlmostEqual(0,
                               self.calculator.calculate_solar_energy(6.5, 12.8, 100, 1))

        # tests if no energy is generated when hours charged is zero
        self.assertAlmostEqual(0,
                               self.calculator.calculate_solar_energy(6.5, 12.8, 22, 0))

        #  these variables represent the conditions:
        #  rm, cfv, pep, pdc, n = 'request.method == "POST"', 'calculator_form.validate()', 'point < end_point', 'point.date() != current', ' net < 0'

    def operator_result_mock(self, rm, cfv, pep, pdc, n):

        if rm and cfv:
            # extract information from the form
            battery_capacity = 82
            initial_charge = 2
            final_charge = 50
            start_date = '10/10/2020'
            start_time = '09:10'
            charger_configuration = 8
            postcode = 3444

            # list of values based of charger_configuration
            power = [2, 3.6, 7.2, 11, 22, 36, 90, 350]
            base_price = [5, 7.5, 10, 12.5, 15, 20, 30, 50]

            time = self.calculator.time_calculation(initial_charge, final_charge, battery_capacity, power[int(charger_configuration)-1])
            start_point = datetime.strptime(start_date + ' ' + start_time, '%d/%m/%Y %H:%M')
            end_point = self.calculator.get_endtime(start_date, start_time, time)                    
                    
            # you may change the logic as your like
            costs = 0

            # loops for the 3 different years
            # for point in [start_point, start_point.replace(year=start_point.year-1), start_point.replace(year=start_point.year-2)]:
            point = start_point
            current = point.date()
            api = self.test_calculator.get_api(postcode, str(point.date()))
            is_holiday = self.calculator.is_holiday(point.date())
            if pep:
                # if date changes, update api and is_holiday
                if pdc:
                    is_holiday = self.calculator.is_holiday(point.date())
                    api = self.test_calculator.get_api(postcode, str(point.date()))
                is_peak = self.calculator.is_peak(point.time())
                si , dl, cc, = self.calculator.get_solar_insolation(api), self.calculator.get_day_light_length(api), self.calculator.get_cloud_cover(api, 0)

                solar = self.calculator.calculate_solar_energy(si, dl, cc, 1/60)
                charger = power[int(charger_configuration)-1]/60
                net = charger - solar
                if n:
                    net = 0

                costs += self.calculator.cost_calculation(net, base_price[int(charger_configuration)-1], is_peak, is_holiday)
                # increments by 1 minute
                point += timedelta(minutes=1)
            # sets new end_point based on the year
            # end_point = end_point.replace(year = end_point.year - 1)

        # get average costs of the 3 years
        # cost = costs/3
            return costs
 
    # tests when all condition branches are True
    def test_all_True(self):
        self.assertAlmostEqual(0, self.operator_result_mock(True, True, True, True, True))

    # tests when all condition branches are True, except for 'request.method == "POST" and calculator_form.validate()'
    def test_rm_and_cfv_False(self):
        self.assertAlmostEqual(None, self.operator_result_mock(True, False, True, True, True))

    # tests when all condition branches are True, except for 'point < end_point'
    def test_pep_False(self):
        self.assertAlmostEqual(0, self.operator_result_mock(True, True, False, True, True))

    # tests when all condition branches are True, except for 'point.date() != current'
    def test_pdc_False(self):
        self.assertAlmostEqual(0, self.operator_result_mock(True, True, True, False, True))
    
    # tests when all condition branches are True, except for 'net < 0'
    def test_n_False(self):
        self.assertAlmostEqual(3.17532618118, self.operator_result_mock(True, True, True, True, False))


def main():
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCalculator)
    unittest.TextTestRunner(verbosity=2).run(suite)


main()
# if __name__ == "__main__":
