from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from web_messaging.blueprints.user.models import User, Anonymous
from flask_pymongo import pymongo
from web_messaging.extensions import mongo, login_manager, c, bc
from config.settings import customers_production, customers_test

customers = Blueprint('customers', __name__, template_folder='templates')



@customers.route('/test', methods=['GET'])
@login_required
def test():
    #if current_user.id:
    collection = mongo.db[customers_test]
    cursor = collection.find()
    customers = cursor.sort("Last Name", pymongo.ASCENDING)
    return render_template("clients.html", customers=customers)

@customers.route('/clients', methods=['GET'])
@login_required
def clients():
    #if current_user.id:
    collection = mongo.db[customers_production]
    cursor = collection.find()
    customers = cursor.sort("Last Name", pymongo.ASCENDING)
    return render_template("clients.html", customers=customers)


@customers.route('/delete/<string:phone>')
def delete_task(phone):
    to_delete = {'Phone': phone}
    try:
        mongo.db[customers_test].delete_one(to_delete)
        return redirect("/clients")
    except Exception as e:
        return str(e)

@customers.route('/add-customer', methods=['POST'])
def create():
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