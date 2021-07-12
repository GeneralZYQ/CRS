from flask import Flask, render_template, redirect, url_for
from flask_login import LoginManager, current_user
from flask_bootstrap import Bootstrap
import pymongo
from pymongo import MongoClient
import connectToDB
from models import User



print('start')

app = Flask(__name__)
Bootstrap(app)

app.config["SECRET_KEY"] = "this is the secret key hey"

connectToDB.connect_to_db()
print(connectToDB.db)

login = LoginManager(app)
login.login_view = 'login_customer'

@app.route('/')
def index():
	# return 'Hello, World!2233'
	if len(current_user.id) > 0:
		return redirect(url_for('user_dashboard'))

	return render_template('index.html')


@app.route('/insert-vehicles-subtype-descriptions/')
def insert_sub_type_descriptions():
	connectToDB.connect_to_db()
	vehicles_sub_descriptions = [{'type' : 'L', 'subType': 'L1', 
	'description': 'A two-wheeled vehicle with an engine cylinder capacity in the case of a thermic engine not exceeding 50 cm3 and whatever the means of propulsion a maximum design speed not exceeding 50 km/h.', 
	'gold_cost_per_hour': 3.75, 'regular_cost_per_hour': 5.05, 'pledge': 100},
	{'type' : 'L', 'subType': 'L2', 
	'description': 'A three-wheeled vehicle of any wheel arrangement with an engine cylinder capacity in the case of a thermic engine not exceeding 50 cm3 or 4kw and whatever the means of propulsion a maximum design speed not exceeding 50 km/h.', 
	'gold_cost_per_hour': 3.85, 'regular_cost_per_hour': 5.15, 'pledge': 100},
	{'type' : 'L', 'subType': 'L3', 
	'description': 'A two-wheeled vehicle with an engine cylinder capacity in the case of a thermic engine exceeding 50 cm3 or 4kw and whatever the means of propulsion a maximum design speed exceeding 50 km/h.', 
	'gold_cost_per_hour': 3.95, 'regular_cost_per_hour': 5.25, 'pledge': 100},
	{'type' : 'L', 'subType': 'L4', 
	'description': 'A vehicle with three wheels asymmetrically arranged in relation to the longitudinal median plane with an engine cylinder capacity in the case of a thermic engine exceeding 50 cm3 or whatever the means of propulsion a maximum design speed exceeding 50 km/h (motor cycles with sidecars).', 
	'gold_cost_per_hour': 3.95, 'regular_cost_per_hour': 5.35, 'pledge': 100},
	{'type' : 'L', 'subType': 'L5', 
	'description': 'A vehicle with three wheels symmetrically arranged in relation to the longitudinal median plane with an engine cylinder capacity in the case of a thermic engine exceeding 50 cm3 or whatever the means of propulsion a maximum design speed exceeding 50 km/h.', 
	'gold_cost_per_hour': 3.95, 'regular_cost_per_hour': 5.35, 'pledge': 100},
	{'type' : 'L', 'subType': 'L6', 
	'description': 'A vehicle with four wheels whose unladen mass is not more than 350 kg, not including the mass of the batteries in case of electric vehicles, whose maximum design speed is not more than 45 km/h, and whose engine cylinder capacity does not exceed 50 cm3 for spark (positive) ignition engines, or whose maximum net power output does not exceed 4 kW in the case of other internal combustion engines, or whose maximum continuous rated power does not exceed 4 kW in the case of electric engines.', 
	'gold_cost_per_hour': 3.95, 'regular_cost_per_hour': 5.35, 'pledge': 100},
	{'type' : 'L', 'subType': 'L7', 
	'description': 'A vehicle with four wheels, other than that classified for the category L6, whose unladen mass is not more than 400 kg[3] (550 kg[3] for vehicles intended for carrying goods), not including the mass of batteries in the case of electric vehicles and whose maximum continuous rated power does not exceed 15 kW.', 
	'gold_cost_per_hour': 3.95, 'regular_cost_per_hour': 5.35, 'pledge': 100},
	{'type' : 'M', 'subType': 'M1', 
	'description': "Vehicles used for carriage of passengers, comprising not more than eight seats in addition to the driver's = 9.( Larger Than Standard Car eg: London Cab / E7 Type Vehicle 8 seat + Driver.)", 
	'gold_cost_per_hour': 8.75, 'regular_cost_per_hour': 9.45, 'pledge': 100},
	{'type' : 'M', 'subType': 'M2', 
	'description': "Vehicles used for the carriage of passengers, comprising more than eight seats in addition to the driver's seat, and having a maximum mass not exceeding 5 tonnes. (Bus)", 
	'gold_cost_per_hour': 8.85, 'regular_cost_per_hour': 9.55, 'pledge': 100},
	{'type' : 'M', 'subType': 'M3', 
	'description': "Vehicles used for the carriage of passengers, comprising more than eight seats in addition to the driver's seat, and having a maximum mass exceeding 5 tonnes. (Bus)", 
	'gold_cost_per_hour': 8.95, 'regular_cost_per_hour': 9.65, 'pledge': 100},
	{'type' : 'N', 'subType': 'N1', 
	'description': "Vehicles used for the carriage of goods and having a maximum mass not exceeding 3.5 tonnes. (Pick-up Truck, Van)", 
	'gold_cost_per_hour': 2.95, 'regular_cost_per_hour': 3.15, 'pledge': 100},
	{'type' : 'N', 'subType': 'N2', 
	'description': "Vehicles used for the carriage of goods and having a maximum mass exceeding 3.5 tonnes but not exceeding 12 tonnes. (Commercial Truck)", 
	'gold_cost_per_hour': 2.95, 'regular_cost_per_hour': 3.15, 'pledge': 100},
	{'type' : 'N', 'subType': 'N3', 
	'description': "Vehicles used for the carriage of goods and having a maximum mass exceeding 12 tonnes. (Commercial Truck)", 
	'gold_cost_per_hour': 2.95, 'regular_cost_per_hour': 3.15, 'pledge': 100},
	{'type' : 'O', 'subType': 'O1', 
	'description': "Trailers with a maximum mass not exceeding 0.75 tonnes.", 
	'gold_cost_per_hour': 17.5, 'regular_cost_per_hour': 19, 'pledge': 300},
	{'type' : 'O', 'subType': 'O2', 
	'description': "Trailers with a maximum mass exceeding 0.75 tonnes, but not exceeding 3.5 tonnes.", 
	'gold_cost_per_hour': 17.5, 'regular_cost_per_hour': 19, 'pledge': 300},
	{'type' : 'O', 'subType': 'O3', 
	'description': "Trailers with a maximum mass exceeding 3.5 tonnes, but not exceeding 10 tonnes.", 
	'gold_cost_per_hour': 17.5, 'regular_cost_per_hour': 19, 'pledge': 300},
	{'type' : 'O', 'subType': 'O4', 
	'description': "Trailers with a maximum mass exceeding 10 tonnes.", 
	'gold_cost_per_hour': 17.5, 'regular_cost_per_hour': 19, 'pledge': 300},
	{'type' : 'T', 'subType': 'T1', 
	'description': "agricultural and Forestry tractors.", 
	'gold_cost_per_hour': 25, 'regular_cost_per_hour': 30, 'pledge': 300},
	{'type' : 'G', 'subType': 'G1', 
	'description': "off-road vehicles.", 
	'gold_cost_per_hour': 25, 'regular_cost_per_hour': 30.05, 'pledge': 300},
	{'type' : 'S', 'subType': 'SA', 
	'description': "Motor caravan.", 
	'gold_cost_per_hour': 25, 'regular_cost_per_hour': 30, 'pledge': 300},
	{'type' : 'S', 'subType': 'SB', 
	'description': "Armoured vehicle.", 
	'gold_cost_per_hour': 55, 'regular_cost_per_hour': 64, 'pledge': 300},
	{'type' : 'S', 'subType': 'SC', 
	'description': "Ambulance.", 
	'gold_cost_per_hour': 19.5, 'regular_cost_per_hour': 23.5, 'pledge': 300},
	{'type' : 'S', 'subType': 'SD', 
	'description': "Hearse.", 
	'gold_cost_per_hour': 35, 'regular_cost_per_hour': 40, 'pledge': 300},
	]

	connectToDB.db.vehicles_subtype_descriptions.insert_many(vehicles_sub_descriptions)
	return 'insert sub types description successfully!'

@app.route('/insert-vehicles-types-descriptions/')
def insert_type_descriptions():
	connectToDB.connect_to_db()
	vehicle_types_description = [{
		'type': 'L',
		'description' : 'motor vehicles with less than four wheels.'},
		{
		'type': 'M',
		'description' : 'vehicles having at least four wheels and used for the carriage of passengers.'},
		{
		'type': 'N',
		'description' : 'power-driven vehicles having at least four wheels and used for the carriage of goods.'},
		{
		'type': 'O',
		'description' : 'trailers.'},
		{
		'type': 'T',
		'description' : 'agricultural and Forestry tractors.'},
		{
		'type': 'G',
		'description' : 'off-road vehicles.'},
		{
		'type': 'S',
		'description' : 'special purpose vehicles.'},
	]
	connectToDB.db.vehicles_types_descriptions.insert_many(vehicle_types_description)
	return 'types inserted'

@app.route('/insert-vehicles/')
def insert_vehicles():
	connectToDB.connect_to_db()
	vehicles = [{
		'car_code' : 'L-L1-001',
		'type' : 'L',
		'sub_type' : 'L1',
		'location': 'A1'},
		{
		'car_code' : 'L-L1-002',
		'type' : 'L',
		'sub_type' : 'L1',
		'location': 'A1'},
		{
		'car_code' : 'L-L2-001',
		'type' : 'L',
		'sub_type' : 'L2',
		'location': 'A1'},
		{
		'car_code' : 'L-L2-002',
		'type' : 'L',
		'sub_type' : 'L2',
		'location': 'A1'},
		{
		'car_code' : 'L-L3-002',
		'type' : 'L',
		'sub_type' : 'L3',
		'location': 'A1'},
		{
		'car_code' : 'L-L3-001',
		'type' : 'L',
		'sub_type' : 'L3',
		'location': 'A1'},
		{
		'car_code' : 'L-L4-002',
		'type' : 'L',
		'sub_type' : 'L4',
		'location': 'A1'},
		{
		'car_code' : 'L-L4-001',
		'type' : 'L',
		'sub_type' : 'L4',
		'location': 'A1'},
		{
		'car_code' : 'L-L5-002',
		'type' : 'L',
		'sub_type' : 'L5',
		'location': 'A1'},
		{
		'car_code' : 'L-L5-001',
		'type' : 'L',
		'sub_type' : 'L5',
		'location': 'A1'},
		{
		'car_code' : 'L-L6-001',
		'type' : 'L',
		'sub_type' : 'L6',
		'location': 'A1'},
		{
		'car_code' : 'L-L6-002',
		'type' : 'L',
		'sub_type' : 'L6',
		'location': 'A1'},
		{
		'car_code' : 'L-L7-001',
		'type' : 'L',
		'sub_type' : 'L7',
		'location': 'A1'},
		{
		'car_code' : 'L-L7-002',
		'type' : 'L',
		'sub_type' : 'L7',
		'location': 'A1'},
		{
		'car_code' : 'M-M1-001',
		'type' : 'M',
		'sub_type' : 'M1',
		'location': 'A1'},
		{
		'car_code' : 'M-M1-002',
		'type' : 'M',
		'sub_type' : 'M1',
		'location': 'A1'},
		{
		'car_code' : 'M-M2-001',
		'type' : 'M',
		'sub_type' : 'M2',
		'location': 'A1'},
		{
		'car_code' : 'M-M2-002',
		'type' : 'M',
		'sub_type' : 'M2',
		'location': 'A1'},
		{
		'car_code' : 'M-M3-001',
		'type' : 'M',
		'sub_type' : 'M3',
		'location': 'A1'},
		{
		'car_code' : 'M-M3-002',
		'type' : 'M',
		'sub_type' : 'M3',
		'location': 'A1'},
		{
		'car_code' : 'N-N1-001',
		'type' : 'N',
		'sub_type' : 'N1',
		'location': 'A1'},
		{
		'car_code' : 'N-N1-002',
		'type' : 'N',
		'sub_type' : 'N1',
		'location': 'A1'},
		{
		'car_code' : 'N-N2-001',
		'type' : 'N',
		'sub_type' : 'N2',
		'location': 'A1'},
		{
		'car_code' : 'N-N2-002',
		'type' : 'N',
		'sub_type' : 'N2',
		'location': 'A1'},
		{
		'car_code' : 'N-N3-001',
		'type' : 'N',
		'sub_type' : 'N3',
		'location': 'A1'},
		{
		'car_code' : 'N-N3-002',
		'type' : 'N',
		'sub_type' : 'N3',
		'location': 'A1'},
		{
		'car_code' : 'O-O1-001',
		'type' : 'O',
		'sub_type' : 'O1',
		'location': 'A1'},
		{
		'car_code' : 'O-O1-002',
		'type' : 'O',
		'sub_type' : 'O1',
		'location': 'A1'},
		{
		'car_code' : 'O-O2-001',
		'type' : 'O',
		'sub_type' : 'O2',
		'location': 'A1'},
		{
		'car_code' : 'O-O2-002',
		'type' : 'O',
		'sub_type' : 'O2',
		'location': 'A1'},
		{
		'car_code' : 'O-O3-001',
		'type' : 'O',
		'sub_type' : 'O3',
		'location': 'A1'},
		{
		'car_code' : 'O-O3-002',
		'type' : 'O',
		'sub_type' : 'O3',
		'location': 'A1'},
		{
		'car_code' : 'O-O4-001',
		'type' : 'O',
		'sub_type' : 'O4',
		'location': 'A1'},
		{
		'car_code' : 'O-O4-002',
		'type' : 'O',
		'sub_type' : 'O4',
		'location': 'A1'},
		{
		'car_code' : 'T-T1-001',
		'type' : 'T',
		'sub_type' : 'T1',
		'location': 'A1'},
		{
		'car_code' : 'T-T1-002',
		'type' : 'T',
		'sub_type' : 'T1',
		'location': 'A1'},
		{
		'car_code' : 'G-G1-001',
		'type' : 'G',
		'sub_type' : 'G1',
		'location': 'A1'},
		{
		'car_code' : 'G-G1-002',
		'type' : 'G',
		'sub_type' : 'G1',
		'location': 'A1'},
		{
		'car_code' : 'S-SA-001',
		'type' : 'S',
		'sub_type' : 'SA',
		'location': 'A1'},
		{
		'car_code' : 'S-SA-002',
		'type' : 'S',
		'sub_type' : 'SA',
		'location': 'A1'},
		{
		'car_code' : 'S-SB-001',
		'type' : 'S',
		'sub_type' : 'SB',
		'location': 'A1'},
		{
		'car_code' : 'S-SB-002',
		'type' : 'S',
		'sub_type' : 'SB',
		'location': 'A1'},
		{
		'car_code' : 'S-SC-001',
		'type' : 'S',
		'sub_type' : 'SC',
		'location': 'A1'},
		{
		'car_code' : 'S-SC-002',
		'type' : 'S',
		'sub_type' : 'SC',
		'location': 'A1'},
		{
		'car_code' : 'S-SD-001',
		'type' : 'S',
		'sub_type' : 'SD',
		'location': 'A1'},
		{
		'car_code' : 'S-SD-002',
		'type' : 'S',
		'sub_type' : 'SD',
		'location': 'A1'},]

	connectToDB.db.vehicles.insert_many(vehicles)
	return 'vehicles inserted'

@login.user_loader
def load_user(user_id):

	connectToDB.connect_to_db()

	users_count = connectToDB.db.users.count_documents({'user_code': user_id})

	if users_count == 1:
		user = connectToDB.db.users.find_one({'user_code': user_id})
		userType = 0
		user_code = user['user_code']
		if user_code.startswith('G'):
			userType = 1

		loggedUser = User(id=str(user_code), userType=userType)
		return loggedUser



import customer


