import os
from dotenv import load_dotenv

BASEDIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(BASEDIR, 'environments/demo.env'))

# Flask settings 
DEBUG = True
PYTHONDONTWRITEBYTECODE=1
FLASK_SECRET = os.getenv('FLASK_SECRET')

# Twilio - Credentials
TWILIO_SID = os.getenv('TWILIO_SID')
TWILIO_TOKEN = os.getenv('TWILIO_TOKEN')
TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER')

# Twilio - Segments 
MAX_BYTES_PER_SEGMENT = 1200 # max size of a SMS is 140 octets -> 140 * 8bits = 1120 bits
MAX_CHARACTERS_PER_SEGMENT = 160 # max size of a SMS is 140 octets -> 140 * 8bits = 1120 bits
COST_PER_SEGMENT = 0.064 #EUR or USD 0.076 

# MongoDB - DB
MONGO_DBNAME = os.getenv('MONGO_DB')
MONGO_URI = os.getenv('MONGO_URI')

# MongoDB - Collections
customers_production = 'customers_production'
customers_test = 'customers_test'
users_collection = 'users'
ITEMS_PER_PAGE = 4

# Google Cloud - Google Cloud Storage 
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv('GOOGLE_CLOUD_STORAGE_AUTH') 
GCS_BILLING_BUCKET = os.getenv('GCS_BUCKET_BILLING') 

# Local Storage - Temporary files 
UPLOAD_FOLDER = 'tmp/'

