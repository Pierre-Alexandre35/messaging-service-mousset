from flask import Flask, render_template
from web_messaging.blueprints.user import user
from web_messaging.blueprints.texting import texting
from web_messaging.blueprints.customers import customers
from web_messaging.blueprints.billing import billing
from web_messaging.extensions import login_manager, mongo, bc
from web_messaging.context import inject_credit


def register_blueprints(app):
    """ Register blueprints """
    app.register_blueprint(user)
    app.register_blueprint(texting)
    app.register_blueprint(customers)
    app.register_blueprint(billing)
    return app


def create_app(settings_override=None):
    """
    Create a Flask application using the app factory pattern.
    :param settings_override: Override settings
    :return: Flask app
    """
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object('config.settings')
    app.config['MONGO_URI'] = app.config.get('MONGO_URI')
    app.secret_key = app.config.get('FLASK_SECRET')
    if settings_override:
        app.config.update(settings_override)
    error_templates(app)
    app = register_blueprints(app)
    extensions(app)
    configure_context_processors(app)
    return app


def error_templates(app):
    """ Register 0 or more custom error pages (mutates the app passed in) """
    def render_status(status):
        """
        Render a custom template for a specific status
        http://stackoverflow.com/a/30108946
        """
        # Get the status code from the status, default to a 500 so that we
        # catch all types of errors and treat them as a 500.
        code = getattr(status, 'code', 500)
        return render_template('errors/{0}.html'.format(code)), code
    for error in [404, 429, 500]:
        app.errorhandler(error)(render_status)
    return None


def extensions(app):
    """ Register 0 or more extensions (mutates the app passed in) """
    # Create login manager
    login_manager.init_app(app)
    mongo.init_app(app)
    # Create Pymongo
    bc.init_app(app)
    return None


def configure_context_processors(app):
    """
    Inject processors on the app context processor
    to be rendered by template layers
    """
    processors = [inject_credit]
    for processor in processors:
        app.context_processor(processor)
