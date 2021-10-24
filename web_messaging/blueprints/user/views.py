import sys
from urllib.parse import urljoin, urlparse

from flask import Blueprint, abort, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from config.settings import users_collection
from web_messaging.blueprints.user.models import Anonymous, User
from web_messaging.extensions import bc, login_manager, mongo

user = Blueprint('user', __name__, template_folder='templates')
login_manager.anonymous_user = Anonymous
login_manager.login_view = "login"


@user.route('/')
def index():
    return render_template('index.html')


@user.route('/login', methods=['GET', 'POST'])
def login():
    """ Login form - User must be logged in to access most of the pages """
    if request.method == 'GET':
        if current_user.is_authenticated:
            return redirect(url_for('/index'))
        return render_template('login.html')
    users = mongo.db.users
    user_data = users.find_one({'email': request.form['email']}, {'_id': 0})
    if user_data:
        if bc.check_password_hash(user_data['password'], request.form['pass']):
            user = User(user_data['title'],
                        user_data['first_name'],
                        user_data['last_name'],
                        user_data['email'],
                        user_data['password'],
                        user_data['id'])
            login_user(user)
            next = request.args.get('next')
            if not is_safe_url(next):
                return abort(400)
            return redirect(next or url_for('user.profile'))
    return 'Invalid email or password'


@user.route('/profile', methods=['GET'])
@login_required
def profile():
    """ User profile page """
    return render_template('profile.html')


@user.route('/logout', methods=['GET'])
@login_required
def logout():
    """ User session logout """
    logout_user()
    return redirect(url_for('user.index'))


@login_manager.user_loader
def load_user(userid):
    """ Load user informations from the DB to generate a new User object """
    users = mongo.db[users_collection]
    user = users.find_one({'id': userid}, {'_id': 0})
    if user:
        return User(user['title'],
                    user['first_name'],
                    user['last_name'],
                    user['email'],
                    user['password'],
                    user['id'])
    return None


def is_safe_url(target):
    """
    Return True if the url is a safe redirection
    (i.e. it doesn't point to a different host and uses a safe scheme).
    Always returns False on an empty url.
    """
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
        ref_url.netloc == test_url.netloc


def log(data):
    print(repr(data), file=sys.stdout)


@user.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        print(request.form['title'])
        print(request.form['first_name'])
        print(request.form['last_name'])
        print(request.form['email'])
        print(request.form['pass'])
        hashpass = bc.generate_password_hash(
            request.form['pass']).decode('utf-8')
        new_user = User(request.form['title'],
                        request.form['first_name'],
                        request.form['last_name'],
                        request.form['email'],
                        hashpass)
        try:
            mongo.db['users'].insert_one(new_user.dict())
        except Exception as e:
            return str(e)
        return 'ok'
    return render_template('register.html')
