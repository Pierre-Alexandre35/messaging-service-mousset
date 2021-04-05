import os
from dotenv import load_dotenv
BASEDIR = os.path.abspath(os.path.dirname(__file__))


load_dotenv(os.path.join(BASEDIR, '.env'))

DEBUG = True
PYTHONDONTWRITEBYTECODE=1
#SERVER_NAME = '127.0.0.1:5000'


# Mongo Database
MONGO_DBNAME = os.getenv('MONGO_DB')
MONGO_URI = os.getenv('MONGO_URI')


# Twilio API 
FLASK_SECRET = os.getenv('FLASK_SECRET')
TWILIO_SID = os.getenv('TWILIO_SID')
TWILIO_TOKEN = os.getenv('TWILIO_TOKEN')

# Mongo Collections
customers_production = 'customers_production'
customers_test = 'customers_test'
users_collection = 'users'


# Twilio segments 
MAX_BYTES_PER_SEGMENT = 1200 # max size of a SMS is 140 octets -> 140 * 8bits = 1120 bits
MAX_CARACTERS_PER_SEGMENT = 160 # max size of a SMS is 140 octets -> 140 * 8bits = 1120 bits
COST_PER_SEGMENT = 0.076 # USD 
