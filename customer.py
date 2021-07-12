from datetime import datetime
from flask import Flask, jsonify, redirect, url_for, render_template, request, jsonify, flash, session, send_file, send_from_directory
from flask_bootstrap import Bootstrap
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from forms import LoginCustomerForm, OrderCarForm
import connectToDB
from app import app
from models import User
import json
import math
import random

@app.route("/user-dashboard/", methods=["GET"])
@login_required
def user_dashboard():

	connectToDB.connect_to_db()
	
	user = connectToDB.db.users.find_one({'user_code' : current_user.id})
	user_code = user['user_code']

	# { "_id" : ObjectId("60eb33a0bc722ad2a7753c2c"), "user_code" : "N-00000000", "car_code" : "S-SE-001", "status" : "Reserved", "pin_code" : "000000", "start_date" : 1, "expected_length" : 100000, "start_location" : "A1", "back_location" : "B1", "returned_date" : 4, "cost" : 400 }
	latest_rents = list(connectToDB.db.vehicle_customer.find({'user_code': current_user.id}).sort([('start_date', -1)]).limit(1))
	renting_type = '' # '', Reserved, Using, Returned
	pin_code = ''
	using_length = ''
	cost = 0
	car_code = ''
	if len(latest_rents) > 0:

		latest_rent = latest_rents[0]
		car_code = latest_rent['car_code']
		renting_type = latest_rent['status']
		if renting_type == 'Reserved':
			pin_code = latest_rent['pin_code']
		if renting_type == 'Using':
			start_date = latest_rent['start_date']
			now = datetime.now().timestamp()
			delta = now - start_date
			hour = round(delta / 3600.0, 1)
			if hour < 4:
				hour = 4
			using_length = str(hour)
			
			car_type = car_code.split('-')[0]
			car_subtype = car_code.split('-')[1]

			car_descriptions = list(connectToDB.db.vehicles_subtype_descriptions.find({'type': car_type, 'subType': car_subtype}))
			if len(car_descriptions) > 0:
				car_description = car_descriptions[0]
				if current_user.userType == 1:
					cost = car_description['gold_cost_per_hour'] * math.ceil(hour)
				else:
					cost = car_description['regular_cost_per_hour'] * math.ceil(hour)


	return render_template("dashboard-user.html", user_code=user_code, renting_type=renting_type, pin_code=pin_code, using_length=using_length, cost=cost, car_code=car_code)


@app.route("/login-customer/", methods=["GET","POST"])
def login_customer():

	loginForm = LoginCustomerForm()

	if loginForm.validate_on_submit():
		connectToDB.connect_to_db()
		user = connectToDB.db.users.find_one({'email': loginForm.email_address.data})
		if str(user['password']) == loginForm.user_password.data:#The user is found
			user_code = user['user_code']
			userType = 0
			if user_code.startswith('G'):
				userType = 1
			logginedUser = User(id=user['user_code'], userType=userType)
			login_user(logginedUser, remember=True)
			
			return redirect(url_for("user_dashboard"))
		else:
			return render_template("login-customer.html", form=loginForm)
	else:
		return render_template("login-customer.html", form=loginForm)

@app.route("/car-list/", methods=["GET"])
@login_required
def car_list():
	connectToDB.connect_to_db()
	cars = list(connectToDB.db.vehicles.find({}, {"_id": 0}))
	final_cars = []

	for car in cars:

		car_dict = {}

		car_code = car['car_code']
		car_type = car['type']
		car_subtype = car['sub_type']
		car_dict['car_code'] = car_code
		car_dict['car_type'] = car_type
		car_dict['car_subtype'] = car_subtype
		car_description_doc = connectToDB.db.vehicles_subtype_descriptions.find_one({"type": car_type, "subType": car_subtype})
		car_dict['description'] = car_description_doc['description']
		if current_user.userType == 1:
			car_dict['pledge'] = 0
			car_dict['price'] = car_description_doc['gold_cost_per_hour']
		else:
			car_dict['pledge'] = car_description_doc['pledge']
			car_dict['price'] = car_description_doc['regular_cost_per_hour']
		latest_rent = connectToDB.db.vehicle_customer.find({'car_code': car_code}).sort([('start_date', -1)]).limit(1)
		car_dict['available'] = 'Yes'
		if latest_rent.count() > 0:
			if latest_rent['status'] != '':
				car_dict['available'] = 'No'
			else:
				car_dict['available'] = 'Yes'

		final_cars.append(car_dict)

	
	return render_template('find_car.html', cars=final_cars, user_code=current_user.id)


@app.route('/return-car/<string:car_id>',methods=['GET', 'POST'])
def return_car():
	
	return 'return car'


@app.route('/start-car/<string:car_id>',methods=['GET', 'POST'])
def start_car(car_id):

	connectToDB.connect_to_db()
	connectToDB.db.vehicle_customer.update_one({"car_code": car_id, "user_code": current_user.id}, {"$set": {"status": "Using"}})

	return redirect(url_for('user_dashboard'))


@app.route('/order-car/<string:car_id>',methods=['GET', 'POST'])
def order_car(car_id):

	connectToDB.connect_to_db()

	car_type = car_id.split('-')[0]
	car_subtype = car_id.split('-')[1]
	price = 0
	pledge = 0
	car_description_doc = connectToDB.db.vehicles_subtype_descriptions.find_one({"type": car_type, "subType": car_subtype})
	if current_user.userType == 1:
		price = car_description_doc['gold_cost_per_hour']
	else:
		price = car_description_doc['regular_cost_per_hour']
		plege = car_description_doc['pledge']

	if request.method == 'GET':
		
		orderForm = OrderCarForm(car_code=car_id)


		return render_template('order_car.html', price=price, form=orderForm, car_code=car_id, pledge=pledge, message='')
	else:

		orderForm = OrderCarForm()

		if orderForm.validate_on_submit():
			hours = orderForm.hoursToRent.data
			if hours < 4:
				hours = 4
			total_price = pledge + hours * price
			print(total_price)

			fiftyCounts = orderForm.fiftyCounts.data if orderForm.fiftyCounts.data is not None else 0
			twentyCounts = orderForm.twentyCounts.data if orderForm.twentyCounts.data is not None else 0
			tenCounts = orderForm.tenCounts.data if orderForm.tenCounts.data is not None else 0
			fiveCounts = orderForm.fiveCounts.data if orderForm.fiveCounts.data is not None else 0
			twoCounts = orderForm.twoCounts.data if orderForm.twoCounts.data is not None else 0
			oneCounts = orderForm.oneCounts.data if orderForm.oneCounts.data is not None else 0
			fiftycentsCounts = orderForm.fiftycentsCounts.data if orderForm.fiftycentsCounts.data is not None else 0
			twentycentsCounts = orderForm.twentycentsCounts.data if orderForm.twentycentsCounts.data is not None else 0

			given_price = fiftycentsCounts * 50.0 + twentyCounts * 20.0 + tenCounts * 10.0 + fiveCounts * 5.0 + twoCounts * 2.0 + oneCounts*1.0 + fiftycentsCounts * 0.5 + twentycentsCounts * 0.2

			delta = given_price - total_price
			print(given_price)
			print(delta)
			cash_back = []
			if delta < 0:
				render_template('order_car.html', price=price, form=orderForm, car_code=car_id, pledge=pledge, message='The money is not enough')
			elif delta == 0:
				return 'to dashboard page'
			else:
				dec_part,int_part=math.modf(delta)
				if dec_part >= 0.0 and dec_part <= 0.19:
					dec_part = 0.2
				elif dec_part >= 0.21 and dec_part <= 0.39:
					dec_part = 0.4
				elif dec_part >= 0.41 and dec_part <= 0.49:
					dec_part = 0.5
				elif dec_part >= 0.51 and dec_part <= 0.59:
					dec_part = 0.6
				elif dec_part >= 0.61 and dec_part <= 0.69:
					dec_part = 0.7
				elif dec_part >= 0.71 and dec_part <= 0.79:
					dec_part = 0.8
				elif dec_part >= 0.81 and dec_part <= 0.89:
					dec_part = 0.9
				elif dec_part >= 0.91 and dec_part <= 0.99:
					dec_part = 1.0

				remaining = int_part + dec_part

				print(remaining)
				
				for x in [50.0, 20.0, 10.0, 5.0, 2.0, 1.0, 0.5, 0.2]:
					int_number = int(remaining / x)
					des = "%d * %f" %(int_number, x)
					cash_back.append(des)
					remaining = remaining - int_number * x
					if remaining == 0:
						break

				print(cash_back)

				#random number 

				#inser to vehicle_customer

			car = connectToDB.db.vehicles.find_one({'car_code': car_id})
			car_location = car['location']


			pin_code = random.randint(100000,999999)
			now = datetime.now().timestamp()
			expected_length = hours * 3600
			connectToDB.db.vehicle_customer.insert_one({'user_code':current_user.id, 'car_code': car_id,
				'status' : 'Reserved', 'pin_code': str(pin_code), 'start_date' : now, 'expected_length' : expected_length,
				'start_location' : car_location, 'back_location' : '', 'returned_date': 0, 'cost' : given_price, 'price_per_hour': price
				})

			return render_template('reserved_car.html', pin_code=pin_code, location=car_location, car_id=car_id)
		else:
			render_template('order_car.html', price=price, form=orderForm, car_code=car_id, pledge=pledge, message = '')


		return price





