from flask_wtf import FlaskForm
from wtforms import StringField, DateField, TimeField
from wtforms.validators import DataRequired, ValidationError, Optional
from datetime import datetime


# validation for form inputs
class Calculator_Form(FlaskForm):
    # this variable name needs to match with the input attribute name in the html file
    # you are NOT ALLOWED to change the field type, however, you can add more built-in validators and custom messages
    BatteryPackCapacity = StringField("Battery Pack Capacity", [DataRequired()])
    InitialCharge = StringField("Initial Charge", [DataRequired()])
    FinalCharge = StringField("Final Charge", [DataRequired()])
    StartDate = DateField("Start Date", [DataRequired("Data is missing or format is incorrect")], format='%d/%m/%Y')
    StartTime = TimeField("Start Time", [DataRequired("Data is missing or format is incorrect")], format='%H:%M')
    ChargerConfiguration = StringField("Charger Configuration", [DataRequired()])
    PostCode = StringField("Post Code", [DataRequired()])

    # use validate_ + field_name to activate the flask-wtforms built-in validator
    # this is an example for you
    def validate_BatteryPackCapacity(self, field):
        if field.data is None:
            raise ValidationError('Field data is none')
        elif field.data == '':
            raise ValueError("cannot fetch data")

    # validate initial charge here
    def validate_InitialCharge(self, field):
        # another example of how to compare initial charge with final charge
        # you may modify this part of the code
        i = int(field.data)
        f = int(self.FinalCharge.data)
        if (i > f) | (i < 0) | (i > 100):
            raise ValueError("Initial charge data error")

    # validate final charge here
    def validate_FinalCharge(self, field):
        f = int(field.data)
        if (f > 100):
            raise ValueError("Final charge data error")

    # validate start date here
    def validate_StartDate(self, field):
        date = datetime(field.data.year, field.data.month, field.data.day)
        if date<datetime(2008, 7, 1):
            raise ValueError('Date should not be ealier than 01/07/2008')

    # validate charger configuration here
    def validate_ChargerConfiguration(self, field):
        configurations = [1, 2, 3, 4, 5, 6, 7, 8]

        if int(field.data) not in configurations:
            raise ValueError("Charger Configuration data error")

    # validate postcode here
    def validate_PostCode(self, field):
        pc = int(field.data)
        if (pc<200) | (pc>299 and pc<800) | (pc>9999):
            raise ValueError("Post Code data error")
