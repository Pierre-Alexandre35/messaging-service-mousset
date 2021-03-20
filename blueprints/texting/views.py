from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from extensions import mongo, login_manager, c, bc
from blueprints.user.models import User, Anonymous
from twilio.rest import Client 
import sys
from urllib.parse import urlparse, urljoin
from flask_pymongo import pymongo
from config.settings import TWILIO_SID, TWILIO_TOKEN, customers_production, customers_test, users_collection

texting = Blueprint('texting', __name__, template_folder='templates')