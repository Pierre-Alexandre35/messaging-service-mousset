import math
import re
import time
import traceback

from flask import Blueprint, jsonify, render_template, request
from flask_login import login_required

from config.settings import (COST_PER_SEGMENT, MAX_CHARACTERS_PER_SEGMENT,
                             TWILIO_PHONE_NUMBER, customers_production,
                             customers_test)
from web_messaging.blueprints.texting.models import Campaign
from web_messaging.context import get_twilio_credits
from web_messaging.extensions import mongo, twilio_client

texting = Blueprint('texting', __name__, template_folder='templates')


@texting.route("/new-campaign", methods=['GET'])
@login_required
def new_campaign():
    """ Form to create a new campaign """
    return render_template('new-campaign.html',
                           currency='€',
                           cost_per_sms=0,
                           max_characters=MAX_CHARACTERS_PER_SEGMENT
                           )


@texting.route("/campaigns", methods=['GET'])
@login_required
def campaigns():
    """ All campaigns overview page """
    collection = mongo.db['campaigns']
    campaigns = collection.find()
    return render_template('campaigns.html', campaigns=campaigns)


@texting.route("/get_cost_estimation", methods=['GET', 'POST'])
def get_cost_estimation():
    """
    Estimate the total cost of a campaign.
    Total cost = cost per segment * number of messages * segment number
    Read more about segments:
    https://www.twilio.com/blog/2017/03/what-the-heck-is-a-segment.html
    """
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
        currency=currency
    )


@texting.route("/launch-campaign", methods=['POST'])
@login_required
def call():
    """ Launch a new texting-campaign  """
    message = request.form['body']
    selected_list = request.form['list']
    if selected_list == 'production-list':
        return text_customers(message)
    return text_test(message)


def contact(phone, message_body):
    """ Send the text message to a list of recipients  """
    international_number = "+33" + phone
    twilio_client.messages.create(
        from_=TWILIO_PHONE_NUMBER,
        body=message_body,
        to=international_number)


def validate_phone(phone):
    if re.match("^[0-9]{10}$", phone) and phone.startswith(('06', '07')):
        return True
    return False


def text_customers(message):
    """ Send a text-message to all customers-customers  """
    collection = mongo.db[customers_production]
    cursor = collection.find()
    errors = 0
    success = 0
    for customer in cursor:
        try:
            contact(customer['Phone'], message)
            success = success + 1
        except Exception:
            errors = errors + 1
            print(traceback.format_exc())
    return str(cursor)


def text_test(message):
    """ Send a text-message to all test-customers  """
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
    create_campaign_report('test', message, success,
                           errors, current_twilio_balance)
    return render_template("result.html", errors=errors, success=success)


def create_campaign_report(customer_list,
                           message,
                           successes,
                           failures,
                           previous_twilio_balance):
    """ Generate a new texting-campaign Object and store it in the DB """
    time.sleep(15)
    current_twilio_balance = get_twilio_credits()
    cost = current_twilio_balance[0] - previous_twilio_balance[0]
    new_campaign = Campaign(message, customer_list, cost, successes, failures)
    mongo.db['campaigns'].insert_one(new_campaign.dict())
    return "ok"


def total_cost_estimation(quantity, input_length):
    """
    Estimate the total cost of a campaign.
    Total cost = cost per segment * number of messages * segment number
    Read more about segments:
    https://www.twilio.com/blog/2017/03/what-the-heck-is-a-segment.html
    """
    # celing because a segment is always an integer.
    number_of_segments = math.ceil(input_length / MAX_CHARACTERS_PER_SEGMENT)
    if number_of_segments < 1:
        number_of_segments = 1
    estimated_cost_per_sms = number_of_segments * COST_PER_SEGMENT
    total_estimated_cost = estimated_cost_per_sms * quantity
    return round(total_estimated_cost, 2)
