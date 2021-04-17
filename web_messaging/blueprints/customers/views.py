from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from web_messaging.blueprints.user.models import User, Anonymous
from flask_pymongo import pymongo
from web_messaging.extensions import mongo, login_manager, bc
from config.settings import customers_production, customers_test
from web_messaging.blueprints.customers.models import Pagination
import math

customers = Blueprint('customers', __name__, template_folder='templates')
ITEMS_PER_PAGE = 3

@customers.route('/test', methods=['GET'])
@login_required
def test():
    """ Testing customers list overview page """
    #if current_user.id:
    collection = mongo.db[customers_test]
    cursor = collection.find()
    customers = cursor.sort("Last Name", pymongo.ASCENDING)
    return render_template("clients.html", customers=customers)



@customers.route('/clients', methods=['GET'])
@login_required
def clients():
    """ Client customers list overview page """
    collection = mongo.db[customers_production]
    number_of_items = collection.count()
    first_page = 0
    last_page = math.ceil(number_of_items / ITEMS_PER_PAGE)
    current_page = int(request.args.get('page'))
    if not current_page:
        current_page = 0
    to_skip = current_page * ITEMS_PER_PAGE
    cursor = collection.find().skip(to_skip).limit(ITEMS_PER_PAGE)
    customers = cursor.sort("Last Name", pymongo.ASCENDING)
    return render_template("clients.html", customers=customers, page=current_page)

@customers.route('/delete/<string:phone>')
def delete_task(phone):
    """ TO FIX  """
    to_delete = {'Phone': phone}
    try:
        mongo.db[customers_test].delete_one(to_delete)
        return redirect("/clients")
    except Exception as e:
        return str(e)

@customers.route('/add-customer', methods=['POST'])
def create():
    """ Create a new User object and insert that new user on the database """
    last_name = request.form['nom']
    first_name = request.form['prenom']
    phone = request.form['phone']
    customer_type = request.form['customers-list'] 
    new_user = {'First Name' : first_name, 'Last Name': last_name, 'Phone' : phone}
    if customer_type == 'real':
        try:
            collection = mongo.db[customers_production]
            collection.insert_one(new_user)
            return redirect("/clients")
        except Exception as e:
            return str(e)
    else:  
        try:
            collection = mongo.db[customers_test]
            collection.insert_one(new_user)
            return redirect("/test")
        except Exception as e:
            return str(e)