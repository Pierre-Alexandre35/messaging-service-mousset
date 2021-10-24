from flask import Blueprint, redirect, render_template, request
from flask_login import login_required

from config.settings import DOMAIN_NAME, customers_production, customers_test
from web_messaging.blueprints.customers.customer import (create_customer,
                                                         delete_customer)
from web_messaging.blueprints.customers.pagination import (
    generate_pagination, get_number_of_records)

customers = Blueprint('customers', __name__, template_folder='templates')


def get_selected_path(selected_path):
    if str(selected_path) == '/clients':
        return customers_production
    return customers_test


@customers.route('/clients', methods=['GET'], endpoint="clients")
@customers.route('/test', methods=['GET'], endpoint="test")
@login_required
def display_customers_list():
    """ Testing customers list overview page """
    selected_path = request.url_rule
    selected_customer_list = get_selected_path(selected_path)
    page_number = 0
    if 'page' in request.args:
        page_number = int(request.args.get('page'))
    customers, pagination = generate_pagination(
        page_number, selected_customer_list)
    total_number_of_records = get_number_of_records(selected_customer_list)
    return render_template("clients.html",
                           domain_name=DOMAIN_NAME,
                           selected_customer_list=selected_customer_list,
                           customers=customers,
                           pagination=pagination,
                           url_path=selected_path,
                           total_number_of_records=total_number_of_records,
                           phone_error=None)


@customers.route('/delete/<string:selected_list>/<string:phone>')
def delete(selected_list, phone):
    delete_customer(selected_list, phone)
    if selected_list == customers_production:
        return redirect("/clients")
    return redirect("/test")


@customers.route('/add-customer/<string:selected_list>', methods=['POST'])
def create(selected_list):
    """ Create a new User object and insert that new user on the database """
    last_name = request.form['nom']
    first_name = request.form['prenom']
    phone = request.form['phone']
    create_customer(first_name, last_name, phone, selected_list)
    if selected_list == customers_production:
        return redirect("/clients")
    return redirect("/test")
