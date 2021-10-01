from datetime import date, datetime, timedelta
from workalendar.oceania import Australia
from flask import Flask, render_template, request
import requests


class Calculator():
    # you can choose to initialise variables here, if needed.
    def __init__(self, postcode=None, date=None):
        self.cost = 0
        self.time = 0
        self.si = 0
        self.du = 0
        self.dl = 0
        self.cc = 0

        # # ====== API ======
        # location id
        if postcode is None:
            postcode = request.form['PostCode']
        l = requests.get('http://118.138.246.158/api/v1/location?postcode=' + postcode)
        json = l.json()
        locationId =  str(json[0]['id'])

        # date
        if date is None:
            date = request.form['StartDate']
        d, m, y = date.split('/')
        day, month, year = int(d), int(m), int(y)

        # handles date over 24/09/2021
        while datetime(year, month, day)>datetime(2021, 9, 24):
            year -= 1
            try:
                datetime(year, month, day)
            except ValueError:
                day = 28
                d = str(day)
        
        api = requests.get('http://118.138.246.158/api/v1/weather?location=' + locationId + '&date=' + str(year) + '-' + m + '-' + d)
        self.api = api.json()

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

        cost = (int(final_state) - int(initial_state)) / 100 * int(capacity) * base_price / 100 * surcharge_factor
        return cost

    # you may add more parameters if needed, you may also modify the formula.
    def time_calculation(self, initial_state, final_state, capacity, power):
        self.time = (int(final_state) - int(initial_state)) / 100 * int(capacity) / power * 60
        return self.time

    # you may create some new methods at your convenience, or modify these methods, or choose not to use them.
    def is_holiday(self, start_date):
        day, month, year = start_date.split('/')
        aus = Australia()

        return aus.is_working_day(date(int(year), int(month), int(day))) == False

    def is_peak(self, start_time):
        t = start_time.split(':')
        hour = int(t[0])

        return hour < 18 & hour > 5

    def peak_period(self, start_time):
        fmt = '%H:%M'
        return datetime.strptime('18:00', fmt) - datetime.strptime(start_time, fmt)

    def get_duration(self, start_time):
        pass

    def get_endtime(self, start_date, start_time, duration):
        return datetime.strptime(start_date + ' ' + start_time, '%D/%M/%Y %H:%M') + timedelta(hours=duration)

    def get_no_of_days(self, start_date, start_time, duration):
        endCharge = datetime.strptime(start_date + ' ' + start_time, '%D/%M/%Y %H:%M') + timedelta(hours=duration)
        print(endCharge)
        endDate, _ = endCharge.split(' ')
        days = datetime.strptime(endDate, '%Y-%m-%d') - datetime.strptime(start_date, '%d/%m/%Y')
        return days

    def get_api(postcode, date):
        # location
        l = requests.get('http://118.138.246.158/api/v1/location?postcode=' + postcode)
        json = l.json()
        locationId =  str(json[0]['id'])

        # date
        d, m, y = date.split('/')
        day, month, year = int(d), int(m), int(y)

        # handles date over 24/09/2021
        while datetime(year, month, day)>datetime(2021, 9, 24):
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
        return self.dl

    # to be acquired through API
    def get_day_light_length(self, start_time):
        fmt = '%H:%M:%S'
        self.dl = str(datetime.strptime(self.api['sunset'], fmt) - datetime.strptime(self.api['sunrise'], fmt))
        return self.dl

    # to be acquired through API
    def get_solar_insolation(self, solar_insolation):
        self.si = str(self.api['sunHours'])
        return self.si

    # to be acquired through API
    def get_cloud_cover(self):
        z = {}
        for i in range(24):
            z.update({"hour" + str(i): str(self.api['hourlyWeatherHistory'][i]['cloudCoverPct'])})

        self.cc = z
        return self.cc

    def calculate_solar_energy(self, si, dl, cc, hour):
        return si*hour/dl*(1-cc/100)*50*0.2
