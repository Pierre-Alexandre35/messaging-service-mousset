import os
from dotenv import load_dotenv

load_dotenv()

db_name = os.getenv('DB_NAME')
uri = os.getenv('DB_URI')
secret = os.getenv('FLASK_SECRET')
account_sid = os.getenv('TWILIO_SID')
auth_token = os.getenv('TWILIO_TOKEN')