from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from web_messaging.blueprints.user.models import User, Anonymous
from web_messaging.extensions import twilio_client, currency_converter, mongo, login_manager, c, bc
import sys
from urllib.parse import urlparse, urljoin
from config.settings import TWILIO_SID, TWILIO_TOKEN, customers_production, customers_test, users_collection, MAX_CARACTERS_PER_SEGMENT, COST_PER_SEGMENT
import math

texting = Blueprint('texting', __name__, template_folder='templates')

def total_cost_estimation(quantity, input_length):
    number_of_segments = math.ceil(input_length / MAX_CARACTERS_PER_SEGMENT)
    if number_of_segments < 1: 
        number_of_segments = 1
    estimated_cost_per_sms = number_of_segments * COST_PER_SEGMENT
    total_estimated_cost = estimated_cost_per_sms * quantity
    return round(total_estimated_cost, 2)


@texting.route("/get_cost_estimation", methods=['GET', 'POST'])
def get_cost_estimation():
    currency = '&euro;'
    input_length = request.json['input_length']
    selected_list = request.json['selected_list']  
    if selected_list == 'test-list':
        count = mongo.db[customers_test].count()
    else:
        count = mongo.db[customers_production].count()
    estimated_cost = str(total_cost_estimation(count, input_length))
    return jsonify(
        estimated_cost=estimated_cost,
        currency=currency,
    )

@texting.route("/campaigns", methods=['GET'])
@login_required
def campaigns():
    return render_template('campaigns.html', currency='€', cost_per_sms = 0, max_caracters = MAX_CARACTERS_PER_SEGMENT)

  

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