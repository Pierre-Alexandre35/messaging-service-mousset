# Module imports
from flask import Flask, render_template, request, url_for, request, redirect, abort
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from urllib.parse import urlparse, urljoin
from twilio.rest import Client 
import sys, os
from web_messaging.blueprints.user import user
from web_messaging.blueprints.texting import texting
from web_messaging.blueprints.customers import customers
from web_messaging.extensions import login_manager, mongo, bc, currency_converter, twilio_client
from web_messaging.context import inject_credit
import dns # required for connecting with SRV

def create_app(settings_override=None):
    """
    Create a Flask application using the app factory pattern.

    :param settings_override: Override settings
    :return: Flask app
    """
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object('config.settings')
    app.config.from_pyfile('settings.py', silent=True)
    app.config['MONGO_URI'] = app.config.get('MONGO_URI')
    app.secret_key= app.config.get('FLASK_SECRET')
    if settings_override:
        app.config.update(settings_override)

    error_templates(app)
    app.register_blueprint(user)
    app.register_blueprint(texting)
    app.register_blueprint(customers)
    extensions(app)
    configure_context_processors(app)
    return app

def error_templates(app):
    """
    Register 0 or more custom error pages (mutates the app passed in).

    :param app: Flask application instance
    :return: None
    """

    def render_status(status):
        """
         Render a custom template for a specific status.
           Source: http://stackoverflow.com/a/30108946

         :param status: Status as a written name
         :type status: str
         :return: None
         """
        # Get the status code from the status, default to a 500 so that we
        # catch all types of errors and treat them as a 500.
        code = getattr(status, 'code', 500)
        return render_template('errors/{0}.html'.format(code)), code

    for error in [404, 429, 500]:
        app.errorhandler(error)(render_status)

    return None


def extensions(app):
    """
    Register 0 or more extensions (mutates the app passed in).

    :param app: Flask application instance
    :return: None
    """
    # Create login manager
    login_manager.init_app(app)
    mongo.init_app(app)
    # Create Pymongo
    bc.init_app(app)
    return None


def configure_context_processors(app):
    processors = [inject_credit]
    for processor in processors:
        app.context_processor(processor)