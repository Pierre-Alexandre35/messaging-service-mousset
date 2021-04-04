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

# Twilio segments 
MAX_BYTES_PER_SEGMENT = 1200 # max size of a SMS is 140 octets -> 140 * 8bits = 1120 bits
MAX_CARACTERS_PER_SEGMENT = 160 # max size of a SMS is 140 octets -> 140 * 8bits = 1120 bits
COST_PER_SEGMENT = 0.076 # USD 
