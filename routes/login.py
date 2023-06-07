import matplotlib
from flask import Blueprint, render_template, request, redirect, session

matplotlib.use('Agg')
import pandas as pd

from controllers.UserManager import UserManager
from app import Dao

user_view = Blueprint('user_route', __name__, template_folder='/templates')

user_manager = UserManager(Dao)

ECS_data = pd.read_csv("C:/Users/annam/Desktop/Python/projekt/job-offer.csv")


@user_view.route('/', methods=['POST', 'GET'])
@user_manager.user.redirect_if_login
def start():
    return render_template('start.html')


@user_view.route('/login', methods=['POST', 'GET'])
@user_manager.user.redirect_if_login
def login():
    msg = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        _form = request.form

        email = str(_form["email"])
        password = str(_form["password"])

        if email and password:
            user = user_manager.signin(email, password)
            if user:
                session['user'] = int(user['id'])
                return redirect("/dashboard")
            return render_template('login.html', msg="Email or password incorrect")
        else:
            msg = 'Empty values!'
    return render_template('login.html', msg=msg)


@user_view.route('/register', methods=['GET', 'POST'])
@user_manager.user.redirect_if_login
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        _form = request.form

        username = str(_form["username"])
        email = str(_form["email"])
        password = str(_form["password"])

        if username and email and password:
            new_user = user_manager.signup(username, email, password)
            if new_user:
                return render_template("login.html", msg="You have registered! Now you can log in")
            return render_template('register.html', msg="User already exists with this email")
        else:
            return render_template('register.html', msg="All fields are required")
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg=msg)


@user_view.route('/logout', methods=['GET'])
@user_manager.user.login_required
def logout():
    user_manager.logout()
    return redirect("/", code=302)



# TODO Hashing password
# TODO cofanie stron
