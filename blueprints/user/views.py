from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from extensions import mongo, login_manager, c, bc
from blueprints.user.models import User, Anonymous
from twilio.rest import Client 
import sys
from urllib.parse import urlparse, urljoin
from flask_pymongo import pymongo
from config.settings import TWILIO_SID, TWILIO_TOKEN, customers_production, customers_test, users_collection

user = Blueprint('user', __name__, template_folder='templates')
login_manager.anonymous_user = Anonymous
login_manager.login_view = "login"
client = Client(TWILIO_SID, TWILIO_TOKEN)


@user.route("/campaigns", methods=['GET'])
@login_required
def campaigns():
    return render_template('campaigns.html')


def get_current_credits():    
    balance_data = client.api.v2010.balance.fetch()
    balance = float(balance_data.balance)
    currency = balance_data.currency
    return balance, currency    
    
def contact(phone, message_body):
    international_number = "+33" + phone
    client.messages.create( 
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
    
    
@user.context_processor
def inject_credit():
    credit, currency = get_current_credits()
    if currency != "EUR":
        credit = c.convert(credit, currency, 'EUR')
    return dict(credit=(round(credit,2)))
    
@user.route("/launch-campaign", methods=['POST'])
@login_required
def call():
    message = request.form['body']
    selected_list = request.form['list']
    if selected_list == "client-list":
        return text_customers(message)
    return text_text(message)


@user.route('/delete/<string:phone>')
def delete_task(phone):
    to_delete = {'Phone': phone}
    try:
        mongo.db[customers_test].delete_one(to_delete)
        return redirect("/clients")
    except Exception as e:
        return str(e)

@user.route('/add-customer', methods=['POST'])
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
   
@user.route('/')
def index():
    try:
        return render_template('index.html')
    except Exception as e:
        return str(e)


@user.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if current_user.is_authenticated:
            return redirect(url_for('/index'))
        return render_template('login.html')
    users = mongo.db.users
    user_data = users.find_one({'email': request.form['email']}, {'_id' : 0 })
    if user_data:
        if bc.check_password_hash(user_data['password'], request.form['pass']):
            user = User(user_data['title'], user_data['first_name'], user_data['last_name'], user_data['email'], user_data['password'], user_data['id'])
            login_user(user)

            #Check for next argument (direct user to protected page they wanted)
            next = request.args.get('next')
            if not is_safe_url(next):
                return abort(400)

            return redirect(next or url_for('user.profile'))

    return 'Invalid email or password'


@user.route('/profile', methods=['GET'])
@login_required
def profile():
    return render_template('profile.html')


@user.route('/test', methods=['GET'])
@login_required
def test():
    #if current_user.id:
    log(current_user.is_authenticated)
    collection = mongo.db[customers_test]
    cursor = collection.find()
    customers = cursor.sort("Last Name", pymongo.ASCENDING)
    return render_template("clients.html", customers=customers)

@user.route('/clients', methods=['GET'])
@login_required
def clients():
    #if current_user.id:
    log(current_user.is_authenticated)
    collection = mongo.db[customers_production]
    cursor = collection.find()
    customers = cursor.sort("Last Name", pymongo.ASCENDING)
    return render_template("clients.html", customers=customers)


@user.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('user.index'))


# Login Manager requirements

@login_manager.user_loader
def load_user(userid):
    # Return user object or none
    users = mongo.db[users_collection]
    user = users.find_one({'id': userid}, {'_id' : 0 })
    if user:
        return User(user['title'], user['first_name'], user['last_name'], user['email'], user['password'], user['id'])
    return None



# Safe URL
def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc

# Logging
def log(data):
    print(repr(data), file=sys.stdout)
    

'''
@user.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        users = mongo.db[users_collection]
        existing_user = users.find_one({'email' : request.form['email']}, {'_id' : 0 })

        if existing_user is None:
            logout_user()
            hashpass = bc.generate_password_hash(request.form['pass']).decode('utf-8')
            new_user = User(request.form['title'], request.form['first_name'], request.form['last_name'], request.form['email'], hashpass)
            login_user(new_user)
            users.insert_one(new_user.dict())
            return redirect(url_for('profile'))

        return 'That email already exists!'

    return render_template('register.html')
'''
