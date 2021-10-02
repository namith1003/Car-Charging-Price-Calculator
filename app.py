from flask import Flask, flash
from flask import render_template
from flask import request
from app.calculator import *

from app.calculator_form import *
import os
SECRET_KEY = os.urandom(32)

ev_calculator_app = Flask(__name__)
ev_calculator_app.config['SECRET_KEY'] = SECRET_KEY


@ev_calculator_app.route('/', methods=['GET', 'POST'])
def operation_result():
    # request.form looks for:
    # html tags with matching "name="

    calculator_form = Calculator_Form(request.form)

    # validation of the form
    if request.method == "POST" and calculator_form.validate():
        # if valid, create calculator to calculate the time and cost
        calculator = Calculator()

        # extract information from the form
        battery_capacity = request.form['BatteryPackCapacity']
        initial_charge = request.form['InitialCharge']
        final_charge = request.form['FinalCharge']
        start_date = request.form['StartDate']
        start_time = request.form['StartTime']
        charger_configuration = request.form['ChargerConfiguration']
        postcode = request.form['PostCode']

        power = [2, 3.6, 7.2, 11, 22, 36, 90, 350]
        base_price = [5, 7.5, 10, 12.5, 15, 20, 30, 50]

        time = calculator.time_calculation(initial_charge, final_charge, battery_capacity, power[int(charger_configuration)-1])
        start_point = datetime.strptime(start_date + ' ' + start_time, '%d/%m/%Y %H:%M')
        end_point = calculator.get_endtime(start_date, start_time, time)                    
                
        # you may change the logic as your like
        costs = 0

        for point in [start_point, start_point.replace(year=start_point.year-1), start_point.replace(year=start_point.year-2)]:
            current = point.date()
            api = calculator.get_api(postcode, str(point.date()))
            is_holiday = calculator.is_holiday(point.date())
            while point < end_point:
                if point.date() != current:
                    is_holiday = calculator.is_holiday(point.date())
                    api = calculator.get_api(postcode, str(point.date()))
                is_peak = calculator.is_peak(point.time())
                si , dl, cc, = calculator.get_solar_insolation(api), calculator.get_day_light_length(api), calculator.get_cloud_cover(api, point.hour)

                solar = calculator.calculate_solar_energy(si, dl, cc, 1/60)
                charger = power[int(charger_configuration)-1]/60
                net = charger - solar
                if net < 0:
                    net = 0

                costs += calculator.cost_calculation(net, base_price[int(charger_configuration)-1], is_peak, is_holiday)
                point += timedelta(minutes=1)
            end_point = end_point.replace(year = end_point.year - 1)

        cost = costs/3

        # you may change the return statement also
        
        # values of variables can be sent to the template for rendering the webpage that users will see
        return render_template('calculator.html', cost = '$' + "{:.2f}".format(cost), time = "{:.2f}".format(time*60) + ' minutes', calculation_success = True, form = calculator_form)
        # return render_template('calculator.html', calculation_success=True, form=calculator_form)

    else:
        # battery_capacity = request.form['BatteryPackCapacity']
        # flash(battery_capacity)
        # flash("something went wrong")
        flash_errors(calculator_form)
        return render_template('calculator.html', calculation_success = False, form = calculator_form)

# method to display all errors
def flash_errors(form):
    """Flashes form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'error')


if __name__ == '__main__':
    ev_calculator_app.run()
