from flask_login import LoginManager
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from twilio.rest import Client 
from config.settings import TWILIO_SID, TWILIO_TOKEN
from google.cloud import storage
from currency_converter import CurrencyConverter

login_manager = LoginManager()
mongo = PyMongo()
bc = Bcrypt()
twilio_client = Client(TWILIO_SID, TWILIO_TOKEN)
currency_converter = CurrencyConverter()
gcp_storage = storage.Client()