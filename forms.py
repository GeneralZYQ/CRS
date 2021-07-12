from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed
from wtforms import StringField, PasswordField, BooleanField, IntegerField, SubmitField, HiddenField, SelectField, FileField, SelectMultipleField, widgets, FloatField
from wtforms.validators import InputRequired, Email, Length, EqualTo, NumberRange, Optional, DataRequired, input_required
from wtforms.fields.html5 import DateField
from wtforms.widgets import Input, TextArea
from wtforms import TextAreaField


class RegisterCustomerForm(FlaskForm):
	"""docstring for ClassName"""
	customer_email = StringField("Email*", validators=[InputRequired("Put the email of the website"), Email(message="invalid email")])
	customer_password = PasswordField("Password*", validators=[InputRequired(),Length(min=8,max=80)])#,
	password2 = PasswordField("Repeat the password*", validators=[InputRequired(),Length(min=8,max=80), EqualTo("customer_password",message="The passwords are not the same!")])
	submit = SubmitField('Register')


class LoginCustomerForm(FlaskForm):
	"""docstring for ClassName"""
	
	email_address = StringField("Email", validators=[InputRequired("Put your email"), Email(message="invalid email")])
	user_password = PasswordField("Password", validators=[InputRequired(),Length(min=8,max=80)])

class OrderCarForm(FlaskForm):

	car_code = StringField("State", validators=[Optional(),Length(min=2,max=80)])

	hoursToRent = IntegerField('How many hours would you like to rent', validators=[InputRequired('Please fill in this field'),NumberRange(min=0, max=10000000)])
	
	fiftyCounts = IntegerField('Number of 50 euro notes', validators=[Optional(),NumberRange(min=0, max=10000000)])
	twentyCounts = IntegerField('Number of 20 euro notes', validators=[Optional(),NumberRange(min=0, max=10000000)])
	tenCounts = IntegerField('Number of 10 euro notes', validators=[Optional(),NumberRange(min=0, max=10000000)])
	fiveCounts = IntegerField('Number of 5 euro notes', validators=[Optional(),NumberRange(min=0, max=10000000)])
	twoCounts = IntegerField('Number of 2 euro coins', validators=[Optional(),NumberRange(min=0, max=10000000)])
	oneCounts = IntegerField('Number of 1 euro coins', validators=[Optional(),NumberRange(min=0, max=10000000)])
	fiftycentsCounts = IntegerField('Number of 50 euro notes', validators=[Optional(),NumberRange(min=0, max=10000000)])
	twentycentsCounts = IntegerField('Number of 20 euro notes', validators=[Optional(),NumberRange(min=0, max=10000000)])
		
class ReturnCarForm(FlaskForm):
	"""docstring for ClassName"""
	hoursRented = FloatField('How many hours did rent', validators=[InputRequired('Please fill in this field'),NumberRange(min=0.0, max=10000000.0)])
	returnPlace = StringField("Place to return", [InputRequired(), Length(min=2, max=200)])

class CheckoutForm(FlaskForm):
	"""docstring for ClassName"""
	fiftyCounts = IntegerField('Number of 50 euro notes', validators=[Optional(),NumberRange(min=0, max=10000000)])
	twentyCounts = IntegerField('Number of 20 euro notes', validators=[Optional(),NumberRange(min=0, max=10000000)])
	tenCounts = IntegerField('Number of 10 euro notes', validators=[Optional(),NumberRange(min=0, max=10000000)])
	fiveCounts = IntegerField('Number of 5 euro notes', validators=[Optional(),NumberRange(min=0, max=10000000)])
	twoCounts = IntegerField('Number of 2 euro coins', validators=[Optional(),NumberRange(min=0, max=10000000)])
	oneCounts = IntegerField('Number of 1 euro coins', validators=[Optional(),NumberRange(min=0, max=10000000)])
	fiftycentsCounts = IntegerField('Number of 50 euro notes', validators=[Optional(),NumberRange(min=0, max=10000000)])
	twentycentsCounts = IntegerField('Number of 20 euro notes', validators=[Optional(),NumberRange(min=0, max=10000000)])
		
		
		
		