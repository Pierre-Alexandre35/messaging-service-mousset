from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from web_messaging.blueprints.user.models import User, Anonymous
from flask_pymongo import pymongo
from web_messaging.extensions import mongo, login_manager, bc
from config.settings import ITEMS_PER_PAGE, customers_production, customers_test
import math

customers = Blueprint('customers', __name__, template_folder='templates')

@customers.route('/clients', methods=['GET'], endpoint="clients")
@customers.route('/test', methods=['GET'], endpoint="test")
@login_required
def display_customers_list():
    """ Testing customers list overview page """
    selected_path = str(request.url_rule)
    if selected_path == '/clients':
        selected_list = customers_production 
    else:
        selected_list = customers_test
    collection = mongo.db[selected_list]
    collection.find()
    cursor = collection.find()
    customers = cursor.sort("Last Name", pymongo.ASCENDING)
    return render_template("clients.html", selected_list=selected_list, customers=customers, phone_error=None)


@customers.route('/delete/<string:selected_list>/<string:phone>')
def delete_task(selected_list, phone):
    collection = mongo.db[selected_list]
    to_delete = {'Phone': phone}
    collection.delete_one(to_delete)
    if selected_list == customers_production:
        return redirect("/clients")
    return redirect("/test")


def user_already_exits(collection, new_user):
    new_user_phone = new_user['Phone']
    is_already_present =  collection.find_one({ 'Phone': new_user_phone})
    return is_already_present
    

def insert_user_to_db(selected_list, new_user):
    collection = mongo.db[selected_list]
    new_user_phone = new_user['Phone']
    exists = collection.find_one({ 'Phone': new_user_phone})
    print(exists)
    collection.insert_one(new_user)

@customers.route('/add-customer/<string:selected_list>', methods=['POST'])
def create(selected_list):
    """ Create a new User object and insert that new user on the database """    
    last_name = request.form['nom']
    first_name = request.form['prenom']
    phone = request.form['phone']
    new_user = {'First Name' : first_name, 'Last Name': last_name, 'Phone' : phone}
    collection = mongo.db[selected_list]
    if user_already_exits(collection, new_user):
        return "alrady exits"
    
    if selected_list == customers_production:
        return redirect("/clients")
    return redirect("/test")


    
    
    
'''
@customers.route('/clients', methods=['GET'])
@login_required
def clients():
    """ Client customers list overview page """
    page = request.args.get(key='page', default=0)
    collection = mongo.db[customers_production]
    number_of_items = collection.count()
    client_pagination = Pagination(number_of_items, ITEMS_PER_PAGE, 3)
    items_to_skip = client_pagination.number_of_previous_items()
    cursor = collection.find().skip(items_to_skip).limit(ITEMS_PER_PAGE)
    cursor = collection.find()
    customers = cursor.sort("Last Name", pymongo.ASCENDING)
    page_data = client_pagination.dict()

    return render_template("clients.html", selected_list='customers_production', customers=customers)
'''
