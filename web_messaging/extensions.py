from flask_login import LoginManager
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from twilio.rest import Client 
from currency_converter import CurrencyConverter
try:
    from config.settings import TWILIO_SID, TWILIO_TOKEN
    print(TWILIO_SID)
    print(TWILIO_TOKEN)
except Exception as e:
    print(123456)
    print(e)

login_manager = LoginManager()
mongo = PyMongo()
bc = Bcrypt()
c = CurrencyConverter()
twilio_client = Client(TWILIO_SID, TWILIO_TOKEN)

currency_converter = CurrencyConverter()


