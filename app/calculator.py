from datetime import date, datetime, timedelta, time
from workalendar.oceania import Australia
from flask import Flask, render_template, request
import requests


class Calculator():
    # you can choose to initialise variables here, if needed.
    def __init__(self, postcode=None, date=None):
        pass
    
    # you may add more parameters if needed, you may modify the formula also.
    def cost_calculation(self, net, base_price, is_peak, is_holiday):
        if is_peak:
            discount = 1
        else:
            discount = 0.5

        if is_holiday:
            surcharge = 1.1
        else:
            surcharge = 1

        cost = base_price / 100 * net * surcharge * discount

        return cost

    # you may add more parameters if needed, you may also modify the formula.
    def time_calculation(self, initial_state, final_state, capacity, power):
        return (int(final_state) - int(initial_state)) / 100 * int(capacity) / power

        # you may create some new methods at your convenience, or modify these methods, or choose not to use them.

    def is_holiday(self, d):
        aus = Australia()
        return aus.is_working_day(date(d.year, d.month, d.day)) == False

    def is_peak(self, t):
        return time(18) > t >= time(6)

    def peak_period(self, start_time):
        pass

    def get_duration(self, start_time):
        pass

    def get_endtime(self, start_date, start_time, duration):
        return datetime.strptime(start_date + ' ' + start_time, '%d/%m/%Y %H:%M') + timedelta(hours=duration)

    def get_api(self, postcode, date):
        # location
        l = requests.get('http://118.138.246.158/api/v1/location?postcode=' + postcode)
        json = l.json()
        locationId = str(json[0]['id'])

        # date
        y, m, d = date.split('-')
        day, month, year = int(d), int(m), int(y)

        # handles date over 24/09/2021
        while datetime(year, month, day) > datetime(2021, 9, 24):
            year -= 1
            try:
                datetime(year, month, day)
            except ValueError:
                day = 28
                d = str(day)
        
        api = requests.get('http://118.138.246.158/api/v1/weather?location=' + locationId + '&date=' + str(year) + '-' + m + '-' + d)
        return api.json()

    # to be acquired through API
    def get_sun_hour(self, sun_hour):
        pass

    # to be acquired through API
    def get_solar_energy_duration(self, start_time):
        pass

    # to be acquired through API
    def get_day_light_length(self, api):
        fmt = '%H:%M:%S'
        length = datetime.strptime(api['sunset'], fmt) - datetime.strptime(api['sunrise'], fmt)
        return length.total_seconds() / 60 / 60

    # to be acquired through API
    def get_solar_insolation(self, api):
        return api['sunHours']

    # to be acquired through API
    def get_cloud_cover(self, api, hour):
        return api['hourlyWeatherHistory'][hour]['cloudCoverPct']

    def calculate_solar_energy(self, si, dl, cc, hour):
        if dl == 0:
            return 0
        else:
            return si * hour / dl * (1 - cc / 100) * 50 * 0.2
