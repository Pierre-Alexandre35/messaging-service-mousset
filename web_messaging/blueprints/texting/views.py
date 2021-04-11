from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from web_messaging.blueprints.user.models import User, Anonymous
from web_messaging.extensions import twilio_client, currency_converter, mongo, login_manager, c, bc, gcp_storage
import sys, math
from urllib.parse import urlparse, urljoin
from config.settings import TWILIO_SID, TWILIO_TOKEN, UPLOAD_FOLDER, customers_production, customers_test, users_collection, MAX_CHARACTERS_PER_SEGMENT, COST_PER_SEGMENT
from web_messaging.blueprints.texting.models import Campaign
import time
from web_messaging.context import get_twilio_credits
import tempfile
import os
import datetime
texting = Blueprint('texting', __name__, template_folder='templates')


@texting.route("/tmp", methods=['GET'])
def tmp():
    cp1 = Campaign('ulysse est ggg', 'customers', '37.00', '457', '0')
    time.sleep(3)
    cp2 = Campaign('.....', 'test', '2.10', '3', '1')
    cp3 = Campaign('NON', 'customers', '29.74', '357', '100')
    time.sleep(5)
    cp4 = Campaign('dfd', 'customers', '2.14', '4', '0')
    mongo.db['campaigns'].insert_one(cp1.dict())
    mongo.db['campaigns'].insert_one(cp2.dict())
    mongo.db['campaigns'].insert_one(cp3.dict())
    mongo.db['campaigns'].insert_one(cp4.dict())
    return "d"


def create_campaign_report(customer_list, message, successes, failures, previous_twilio_balance):
    time.sleep(15)
    current_twilio_balance = get_twilio_credits()
    cost = current_twilio_balance[0] - previous_twilio_balance[0]
    new_campaign = Campaign(message, customer_list, cost, successes, failures)
    mongo.db['campaigns'].insert_one(new_campaign.dict())
    return "ok"


def total_cost_estimation(quantity, input_length):
    number_of_segments = math.ceil(input_length / MAX_CHARACTERS_PER_SEGMENT)
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
        table = customers_test
    else:
        table = customers_production
    count = mongo.db[table].count()
    estimated_cost = str(total_cost_estimation(count, input_length))
    return jsonify(
        estimated_cost=estimated_cost,
        currency=currency,
    )

@texting.route("/new-campaign", methods=['GET'])
@login_required
def new_campaign():
    return render_template('new-campaign.html', currency='€', cost_per_sms = 0, max_characters = MAX_CHARACTERS_PER_SEGMENT)

@texting.route("/campaigns", methods=['GET'])
@login_required
def campaigns():
    collection = mongo.db['campaigns']
    campaigns = collection.find()
    return render_template('campaigns.html', campaigns=campaigns)


def contact(phone, message_body):
    international_number = "+33" + phone
    twilio_client.messages.create( 
            from_='+33755536282',  
            body=message_body,      
            to= international_number)
    
def text_customers(message):
    collection = mongo.db[customers_test]
    cursor = collection.find()
    errors = 0
    success = 0 
    for customer in cursor:
        print(1111111111)
        try:
            contact(customer['Phone'], message)
            success = success + 1
        except Exception as e:
            errors = errors + 1 
            print(e)
    return str(cursor)

def text_text(message):
    current_twilio_balance = get_twilio_credits()
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
    create_campaign_report('test', message, success, errors, current_twilio_balance)
    return render_template("result.html", errors=errors, success=success)


@texting.route("/launch-campaign", methods=['POST'])
@login_required
def call():
    message = request.form['body']
    selected_list = request.form['list']
    if selected_list == "client-list":
        return text_customers(message)
    return text_text(message)