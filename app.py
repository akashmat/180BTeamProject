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


@app.route("/personal_records", methods=['GET', 'POST'])
def personal_records():
    form = TestForm()
    player_id = ""
    if form.validate_on_submit():
        player_id =form.player_id.data
        cursor = mysql.connection.cursor()
        query = "SELECT * FROM PLAYER_SCORE WHERE pscore_id = {0}".format(player_id)
        cursor.execute(query)
        stats = cursor.fetchone()
        print(stats)
        return render_template('stats.html', stats=stats)
        
        """pos = [
            {
                'author': player_id,
                'title': 'NULL',
                'content': 'NULL',
                'date_posted': 'April 30, 2022'
            }]
        return render_template('home.html', posts=pos)"""
        
    return render_template('search.html', title='Login', form=form)

    
    

""" 
@app.route('/index', methods=['GET', 'POST'])
def index():
    search = MusicSearchForm(request.form)
    if request.method == 'POST':
        return search_results(search)
    return render_template('index.html', form=search)


@app.route('/results')
def search_results(search):
    results = []
    search_string = search.data['search']
    if search.data['search'] == '':
        cursor = mysql.connection.cursor()
        query = "SELECT * FROM `MATCH`"
        cursor.execute(query)
        results = cursor.fetchall()
    if not results:
        flash('No results found!')
        return redirect('/')
    else:
        # display results
        return render_template('results.html', results=results)
"""

if __name__ == '__main__':
    app.run(debug=True)