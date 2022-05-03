import hashlib
import json
from tabnanny import check
from flask import Flask, render_template, url_for, flash, redirect, request, session
from sqlalchemy import true
from forms import ProfileForm, RegistrationForm, LoginForm, SearchForm
from admin import admin
from os import abort
from flask_session import Session
import signup_api, login_api, profile_api


#from datetime import date
#import db_operations as dbOp
#import random
#from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
#mysql = MySQL(app)
app.register_blueprint(admin, url_prefix="")
USER_ID = -1
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
session = Session(app)


# Testing: Remove posts.
posts = [
    {
        'author': 'AM 1',
        'title': 'Post 1',
        'content': 'Post 1 content',
        'date_posted': 'April 14, 2022'
    },
    {
        'author': 'PM 2',
        'title': 'Post 2',
        'content': 'Post 2 content',
        'date_posted': 'April 15, 2022'
    }
]


@app.route("/")

@app.route("/home")
def home():
    return render_template('home.html', posts=posts)

@app.route("/homeAdmin")
def homeAdmin():
    return render_template('homeAdmin.html', posts=posts, logout=True)

@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        request_data = json.loads(json.dumps(request.form))
        if signup_api.success(request_data):
            flash(f'Account created for {form.username.data}!', 'success')
            return render_template('login.html', title='Login', form=form)
        else:
            flash('Registration unsuccessful. Please try again later!', 'danger')
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    print(form.validate_on_submit())
    if form.validate_on_submit():
        pwd = hashlib.md5(form.password.data.encode()).hexdigest()
        data = login_api.success(form.email.data, pwd, form.usertype.data)
        global USER_ID
        USER_ID = data
        if data:
            flash('You have been logged in!', 'success')
            if form.usertype.data == 'fan':
                return render_template('home.html', logout=True)
            else:
                return render_template('homeAdmin.html', logout=True)
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/profile", methods=['GET', 'POST'])
def profile():
    form = ProfileForm()
    if form.validate_on_submit():
        data = profile_api.update_success(form.username.data, form.followteam.data, form.favteam.data, form.firstname.data, form.lastname.data, USER_ID)
        if data:
            flash('Profile updated successfully!', 'success')
        else:
            flash('Could not update profile. Please try again later!', 'danger')
    return render_template('profile.html', title='Edit Profile', form = form, logout = True)

@app.route("/viewprofile", methods=['GET', 'POST'])
def viewprofile():
    global USER_ID
    data = profile_api.getdata(USER_ID)
    if data:
        return render_template('view_profile.html', title='View Profile', data = data)
    else:
        flash('Could not retrieve profile information. Please try again later!', 'danger')

@app.route("/fansearch", method=['GET', 'POST'])
def fansearch():
    form = SearchForm()
    if request.method=="POST":
        data = profile_api.search(form.playername.data)
        return render_template("search.html", data=data)
    else:
        return render_template("fansearch.html", title = "Search Fan Profiles", form=form)

@app.route('/logout', methods=['GET'])
def logout():
    global USER_ID
    USER_ID = -1
    return redirect("/")

if __name__ == '__main__':
    app.run(debug=True)
