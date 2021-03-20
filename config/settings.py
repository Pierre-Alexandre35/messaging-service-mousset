DEBUG = True
PYTHONDONTWRITEBYTECODE=1
SERVER_NAME = '127.0.0.1:5000'
MONGO_DBNAME = 'mousset'
MONGO_URI = 'mongodb+srv://pierre:Bonjour2021!@cluster0.fut2y.mongodb.net/mousset?ssl=true&ssl_cert_reqs=CERT_NONE'
SECRET_KEY = 'pizarro351995'

'''
import os
from dotenv import load_dotenv

load_dotenv()

DEBUG = True
PYTHONDONTWRITEBYTECODE=1
SERVER_NAME = '127.0.0.1:5000'

db_name = os.getenv('DB_NAME')
uri = os.getenv('DB_URI')
secret = os.getenv('FLASK_SECRET')
account_sid = os.getenv('TWILIO_SID')
auth_token = os.getenv('TWILIO_TOKEN')

'''