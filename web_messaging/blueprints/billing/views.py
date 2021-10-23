from flask_login import login_required
from flask_pymongo import pymongo
from flask import (
    Blueprint,
    render_template,
    request, redirect,
    url_for,
    send_file
)


from web_messaging.blueprints.billing.models import Bill
from web_messaging.blueprints.billing.storage import retrieve_file_from_bucket
from web_messaging.extensions import mongo


billing = Blueprint('billing', __name__, template_folder='templates')


@billing.route("/billing/<filename>", methods=['GET'])
@login_required
def get_bill(filename):
    """ Return a bill as an attachment """
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


def create_new_bill(file, billing_date, total_cost_usd):
    """ Create a new Bill object and upload that object on MongoDB"""
    new_bill = Bill(billing_date, int(total_cost_usd), file)
    new_bill.upload_to_gcs()
    mongo.db['billing'].insert_one(new_bill.dict())


@billing.route("/upload-bill", methods=['POST', 'GET'])
@login_required
def upload_bills():
    """ Upload a new bill to the GCS """
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']
        billing_date = request.form['billing-date']
        total_cost_usd = request.form['total-cost-usd']
        create_new_bill(file, billing_date, total_cost_usd)
        return redirect(url_for('billing.bills'))
