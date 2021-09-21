from datetime import date
from workalendar.oceania import Australia
import holidays

class Calculator():
    # you can choose to initialise variables here, if needed.
    def __init__(self):
        pass

    # you may add more parameters if needed, you may modify the formula also.
    def cost_calculation(self, initial_state, final_state, capacity, is_peak, is_holiday):
        if is_peak:
            base_price = 100
        else:
            base_price = 50

        if is_holiday:
            surcharge_factor = 1.1
        else:
            surcharge_factor = 1

        cost = (final_state - initial_state) / 100 * capacity * base_price / 100 * surcharge_factor
        return cost

    # you may add more parameters if needed, you may also modify the formula.
    def time_calculation(self, initial_state, final_state, capacity, power):
        time = (final_state - initial_state) / 100 * capacity / power
        return time


    # you may create some new methods at your convenience, or modify these methods, or choose not to use them.
    def is_holiday(self, start_date):
        d = start_date.split('/')
        day = int(d[0])
        month = int(d[1])
        year = int(d[2])
        aus = Australia()

        return aus.is_working_day(date(year, month, day)) == False

    def is_peak(self, start_time):
        t = start_time.split(':')
        hour = int(t[0])

        return hour<18 & hour>5

    def peak_period(self, start_time):
        pass 

    def get_duration(self, start_time):
        pass

    # to be acquired through API
    def get_sun_hour(self, sun_hour):
        pass

    # to be acquired through API
    def get_solar_energy_duration(self, start_time):
        pass

    # to be acquired through API
    def get_day_light_length(self, start_time):
        pass

    # to be acquired through API
    def get_solar_insolation(self, solar_insolation):
        pass

    # to be acquired through API
    def get_cloud_cover(self):
        pass

    def calculate_solar_energy(self):
        pass


