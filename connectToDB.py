import pymongo
from pymongo import MongoClient


client = None 
db = None

def connect_to_db():
	global client, db 

	client = MongoClient()
	db = client.car
	print(db)