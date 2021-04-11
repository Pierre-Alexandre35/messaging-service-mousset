from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from web_messaging.blueprints.user.models import User, Anonymous
from web_messaging.extensions import login_manager, c, bc
from web_messaging.blueprints.billing.storage import upload_file_to_temporary_folder, upload_file_to_gcp

billing = Blueprint('billing', __name__, template_folder='templates')


@billing.route("/billing", methods=['GET'])
@login_required
def bills():
    '''
    bucket = gcp_storage.get_bucket('twilio-billing')
    for blob in bucket.list_blobs(prefix=''):
        print(blob)
    '''
    return render_template("billing.html")

    
@billing.route("/upload-bill", methods = ['POST', 'GET'])
@login_required
def upload_bills():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']
        if file.filename == '':
            return 'No selected file'
        if file:
            bill_local_path = upload_file_to_temporary_folder(file)
            upload_file_to_gcp(bill_local_path, 'use.png')
        return "ok"