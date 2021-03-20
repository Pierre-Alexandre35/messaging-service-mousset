import os
from dotenv import load_dotenv
load_dotenv()

DEBUG = True
PYTHONDONTWRITEBYTECODE=1
SERVER_NAME = '127.0.0.1:5000'


# Mongo Database
MONGO_DBNAME = os.getenv('MONGO_DB')
MONGO_URI = os.getenv('MONGO_URI')

# Mongo Collections
customers_production = 'customers_test'
customers_test = 'customers_test'
users_collection = 'users'

# Twilio API 
SECRET_KEY = os.getenv('FLASK_SECRET')
TWILIO_SID = os.getenv('TWILIO_SID')
TWILIO_TOKEN = os.getenv('TWILIO_TOKEN')

