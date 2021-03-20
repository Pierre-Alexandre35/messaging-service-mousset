from flask_login import LoginManager
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from currency_converter import CurrencyConverter


login_manager = LoginManager()
mongo = PyMongo()
bc = Bcrypt()
c = CurrencyConverter()


