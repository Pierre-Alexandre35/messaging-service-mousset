from flask import Blueprint, render_template, request, jsonify, redirect, url_for, send_file
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from web_messaging.blueprints.user.models import User, Anonymous
from web_messaging.extensions import login_manager, bc
from web_messaging.blueprints.billing.models import Bill
from web_messaging.blueprints.billing.storage import retrieve_file_from_bucket
from web_messaging.extensions import mongo
from flask_pymongo import pymongo

billing = Blueprint('billing', __name__, template_folder='templates')


#db.oldname.rename('newname')

@billing.route("/billing/<filename>", methods=['GET'])
@login_required
def d(filename):
    path = retrieve_file_from_bucket(filename)
    return send_file(path, as_attachment=True)


@billing.route("/billing", methods=['GET'])
@login_required
def bills():
    """ Billing overview page """
    
    collection = mongo.db['billing']
    cursor = collection.find()
    bills = cursor.sort("date", pymongo.ASCENDING)  

    return render_template("billing.html", bills=bills)
    
    
@billing.route("/upload-bill", methods = ['POST', 'GET'])
@login_required
def upload_bills():
    """ Upload a new bill to the GCS """
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']
        if file.filename == '':
            return 'No selected file'
        if file:
            try: 
                new_bill = Bill('2021-02-12', 37.48, file)
                new_bill.upload_to_gcs()
                mongo.db['billing'].insert_one(new_bill.dict())
            except Exception as e:
                return str(e)
        return "ok"
    
