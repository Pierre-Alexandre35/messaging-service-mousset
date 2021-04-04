from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from extensions import mongo, login_manager, c, bc
from blueprints.user.models import User, Anonymous
from extensions import twilio_client, currency_converter
import sys
from urllib.parse import urlparse, urljoin
from flask_pymongo import pymongo
from config.settings import TWILIO_SID, TWILIO_TOKEN, customers_production, customers_test, users_collection

texting = Blueprint('texting', __name__, template_folder='templates')


  

def contact(phone, message_body):
    international_number = "+33" + phone
    twilio_client.messages.create( 
            from_='+33757918166',  
            body=message_body,      
            to= international_number)
    
def text_customers(message):
    collection = mongo.db[customers_test]
    cursor = collection.find()
    errors = 0
    success = 0 
    for customer in cursor:
        try:
            contact(customer['Phone'], message)
            success = success + 1
        except Exception as e:
            errors = errors + 1 
            print(e)
    return str(cursor)

def text_text(message):
    collection = mongo.db[customers_test]
    cursor = collection.find()
    errors = 0
    success = 0 
    for customer in cursor:
        try:
            contact(customer['Phone'], message)
            success = success + 1
        except Exception as e:
            errors = errors + 1 
            print(e)
    return render_template("result.html", errors=errors, success=success)


@texting.route("/launch-campaign", methods=['POST'])
@login_required
def call():
    message = request.form['body']
    selected_list = request.form['list']
    if selected_list == "client-list":
        return text_customers(message)
    return text_text(message)



@texting.route("/cc")
@login_required
def cc():

    records = twilio_client.messages.list(limit=20)
    
    for item in records:
        print(item)
    
    return str(records)