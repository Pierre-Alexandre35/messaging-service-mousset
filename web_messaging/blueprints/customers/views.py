from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from web_messaging.blueprints.user.models import User, Anonymous
from flask_pymongo import pymongo
from web_messaging.extensions import mongo, login_manager, bc
from config.settings import ITEMS_PER_PAGE, customers_production, customers_test
import math

customers = Blueprint('customers', __name__, template_folder='templates')

@customers.route('/test', methods=['GET'])
@login_required
def test():
    """ Testing customers list overview page """
    collection = mongo.db[customers_test]
    collection.find()
    cursor = collection.find()
    customers = cursor.sort("Last Name", pymongo.ASCENDING)
    return render_template("clients.html", selected_list=customers_test, customers=customers)



@customers.route('/clients', methods=['GET'])
@login_required
def clients():
    """ Client customers list overview page """
    collection = mongo.db[customers_production]
    collection.find()
    cursor = collection.find()
    customers = cursor.sort("Last Name", pymongo.ASCENDING)
    return render_template("clients.html", selected_list=customers_production, customers=customers)

@customers.route('/delete/<string:phone>')
def delete_task(phone):
    """ TO FIX  """
    to_delete = {'Phone': phone}
    try:
        mongo.db[customers_test].delete_one(to_delete)
        return redirect("/clients")
    except Exception as e:
        return str(e)


def insert_user_to_db(selected_list, new_user):
    collection = mongo.db[selected_list]
    collection.insert_one(new_user)

@customers.route('/add-customer/<string:selected_list>', methods=['POST'])
def create(selected_list):
    """ Create a new User object and insert that new user on the database """    
    last_name = request.form['nom']
    first_name = request.form['prenom']
    phone = request.form['phone']
    new_user = {'First Name' : first_name, 'Last Name': last_name, 'Phone' : phone}
    insert_user_to_db(selected_list, new_user)
    return redirect("/clients")


    
    
    
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