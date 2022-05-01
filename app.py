from flask import Flask, request, render_template, url_for, flash, redirect, session
from datetime import date
import random
from admin import admin
from polling import polling
from forms import RegistrationForm, LoginForm

#from flask_mysqldb 
#from flask_sqlalchemy import SQLAlchemy
#db = SQLAlchemy()

import db_operations as dbOp


app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
#mysql = MySQL(app)
app.register_blueprint(admin, url_prefix="")
app.register_blueprint(polling, url_prefix="")

#Testing: Remove posts.
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


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'adminPassword':
            flash('You have been logged in!', 'success')
            return redirect(url_for('homeAdmin'))
        elif form.email.data == 'user@blog.com' and form.password.data == 'userPassword':
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)




poll_data = {
   'question' : 'Which team do you think will win?',
   'fields'   : ['team1', 'team2']
   
}

#Polling 
@app.route("/rootPoll")
def poll():
    #poll = dbOp.read_sql_raw("SELECT poll_id FROM POLLS")
    #poll_id = poll['poll_id'].tolist()
    #session['poll_id'] = poll_id
    #print(poll_id)
    return render_template('poll.html', data=poll_data)


# Database operations by Administer
@app.route("/homeAdmin")
def homeAdmin():
    if not ('user' in session and session['user'] == 'user1'):
        return redirect(url_for('login'))
    else:
        return render_template('homeAdmin.html')



if __name__ == '__main__':
    app.run(debug=True)