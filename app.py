# SJSU CMPE 138 Spring 2022 TEAM9 

from flask import Flask, request, render_template, url_for, flash, redirect, session
from datetime import date
import random
from admin import admin
from polling import polling
import pandas as pd
import db_operations as dbOp
from forms import RegistrationForm, LoginForm, TestForm, SearchOption, SearchForm, ProfileForm

import pyodbc

from sqlalchemy import create_engine
from flask_mail import Mail, Message
from apscheduler.schedulers.background import BackgroundScheduler

import logging
import logging.config

import hashlib
import json
from tabnanny import check
from sqlalchemy import true
from os import abort
from flask_session import Session
import signup_api, login_api, profile_api


app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.register_blueprint(admin, url_prefix="")
app.register_blueprint(polling, url_prefix="")

# mail configurations
app.config['MAIL_SERVER']='smtp.mailtrap.io'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'accf3746129f8f'
app.config['MAIL_PASSWORD'] = '450a1a7b606995'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
mail = Mail(app)

USER_ID = -1
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
session = Session(app)

Server = "DESKTOP-TIANPEN\SQLEXPRESS"
Database = "nfl"
Driver = "ODBC Driver 17 for SQL Server"
Database_Con = f'mssql://@{Server}/{Database}?driver={Driver}'
engine = create_engine(Database_Con)
con = engine.connect()

connection = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=DESKTOP-TIANPEN\SQLEXPRESS;DATABASE=nfl;Trusted_Connection=yes;')

logging.basicConfig(filename="output.log",
                    filemode='a',
                    # format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)



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
        request_data = json.loads(json.dumps(request.form))
        if signup_api.success(request_data):
            flash(f'Account created for {form.username.data}!', 'success')
            #logging.info('%s Account created successfully', form.username.data)
            return render_template('login.html', title='Login', form = LoginForm())
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
'''
@app.route("/fansearch", method=['GET', 'POST'])
def fansearch():
    form = SearchForm()
    if request.method=="POST":
        data = profile_api.search(form.playername.data)
        return render_template("search.html", data=data)
    else:
        return render_template("search.html", title = "Search Profile", form=form)
'''        

@app.route('/logout', methods=['GET'])
def logout():
    global USER_ID
    USER_ID = -1
    return redirect("/")



'''
@app.route("/login", methods=['GET', 'POST'])
def login():
    session['user'] = 'Tenson89'
    session['admin'] = 'Manny'
    return render_template("homeAdmin.html")
'''

@app.route("/homeAdmin")
def homeAdmin():
    return render_template('homeAdmin.html', posts=posts, logout=True)
    

poll_data = {
   'question' : ' ',
   'team1' : ' ',
   'team2' : ' '
}

################################################ --- Jesse ---- ############################################################################
#Polling 
@app.route("/rootPoll")
def poll():
    poll = dbOp.read_sql_raw("SELECT poll_id FROM POLLS")
    size = len(poll['poll_id'].tolist())
    polls = poll['poll_id'].tolist()
    rand_id = random.randint(0, size - 1)
    poll_id = polls[rand_id]
    session['poll_id'] = poll_id
    print(poll_id)
    query1 = dbOp.read_sql_raw(f"select * from POLLS where poll_id = {poll_id}")
    poll_data['question'] = query1['poll_name'].iloc[0]
    poll_data['team1'] = query1['team_name1'].iloc[0]
    poll_data['team2'] = query1['team_name2'].iloc[0]

    return render_template('poll.html', data=poll_data)

''''
# Database operations by Administer
@app.route("/homeAdmin")
def homeAdmin():
    if not ('user' in session and session['user'] == 'user1'):
        return redirect(url_for('login'))
    else:
        return render_template('homeAdmin.html')
'''        

################################################ --- Ankur ---- ############################################################################

scheduler = BackgroundScheduler()
def index():
    print("Initiated")
    email_query= 'select email from MATCH join NOTIFIES on match_id=m_id join FAN on p_id =profile_id where  date = CAST( GETDATE()+1 as date)'
    email_data = pd.read_sql_query(email_query, con)
    email_list = email_data['email'].to_list()
    print(email_list)
    if len(email_list) > 0:    
        with app.app_context():    
            msg = Message('Hello, Its match day!', sender = 'ankur@mailtrap.io', recipients = email_list)
            msg.body = "Match Notification"
            mail.send(msg)
            print("done")


################################################ --- Akash ---- ############################################################################

@app.route("/personal_records", methods=['GET', 'POST'])
def personal_records():
    form = TestForm()
    player_id = ""

    if request.method == 'POST':
        player_id = form.member.data
        #player_id =form.player_id.data
        cursor = connection.cursor()
        print(player_id)
        #query = "SELECT * FROM PLAYER_SCORE WHERE pscore_id = {0}".format(player_id)
        query_name = "SELECT * FROM TEAM_MEMBER t \
                      JOIN PLAYER_SCORE p ON t.member_id = p.pscore_id \
                      WHERE p.pscore_id = {0} \
                      ORDER BY member_id ASC".format(player_id)
        cursor.execute(query_name)
        stats = cursor.fetchall()
    
        return render_template('stats.html', stats=stats)

    players_names = select_players() 
    form.member.choices = players_names
    view = 'personal_records'
    return render_template('search.html', title='Player', form=form, view=view)

def select_players():
    cursor = connection.cursor()
    # Queries the First and Last Names of Players from the Team Member Table
    query_names = "SELECT DISTINCT t.fname, t.lname, t.member_id \
                  FROM TEAM_MEMBER t JOIN PLAYER_SCORE p ON t.member_id = p.pscore_id \
                  ORDER BY t.member_id ASC"
    cursor.execute(query_names)
    # A dictionary of rows of resultant query
    rows = cursor.fetchall()
    
    players_names = []
    for row in rows:
        players_names.append((row[2], "{0} {1}".format(row[0], row[1])))  
    
    #Returing a list of tuples (Member_ID, FirstName LastName)
    return players_names

#------------------------------------Coach------------------------------------------------------
@app.route("/coach_records", methods=['GET', 'POST'])
def coach_records():
    form = TestForm()
    view = 'coach_records'
    coach_id = ""

    if request.method == 'POST':
        coach_id = form.member.data
        cursor = connection.cursor()
        query_name = "SELECT * FROM TEAM_MEMBER t \
                      JOIN COACH_SCORE c ON t.member_id = c.cscore_id \
                      WHERE c.cscore_id = {0} \
                      ORDER BY member_id ASC".format(coach_id)
        cursor.execute(query_name)
        stats = cursor.fetchall()
    
        return render_template('statscoach.html', stats=stats, view=view)
        
    players_names = select_coaches() 
    form.member.choices = players_names
    
    return render_template('search.html', title='Coach', form=form, view=view)

def select_coaches():
    cursor = connection.cursor()
    # Queries the First and Last Names of Players from the Team Member Table
    query_names = "SELECT DISTINCT t.fname, t.lname, t.member_id \
                  FROM TEAM_MEMBER t JOIN COACH_SCORE c ON t.member_id = c.cscore_id \
                  ORDER BY t.member_id ASC"
    
    cursor.execute(query_names)
    rows = cursor.fetchall()
    coaches_names = []
    #print(rows[0])
    for row in rows:
        coaches_names.append((row[2], "{0} {1}".format(row[0], row[1])))  
    
    return coaches_names
#------------------------------------teams------------------------------------------------------
@app.route("/team_records", methods=['GET', 'POST'])
def team_records():
    form = TestForm()
    view = 'team_records'
    team_id = ""

    if request.method == 'POST':
        team_id = form.member.data
        cursor = connection.cursor()
        query_name = "SELECT * FROM TEAM_SCORE ts \
                      WHERE ts.t_name = '{0}'".format(team_id)
        cursor.execute(query_name)
        stats = cursor.fetchall()
    
        return render_template('statsteam.html', stats=stats, view=view)
        
    teams_names = select_teams() 
    form.member.choices = teams_names
    
    return render_template('search.html', title='Team', form=form, view=view)

def select_teams():
    cursor = connection.cursor()
    query_names = "SELECT DISTINCT t.team_name \
		           FROM TEAM t JOIN TEAM_SCORE ts ON t.team_name = ts.t_name;"
    cursor.execute(query_names)
    rows = cursor.fetchall()
    teams_names = []
    #print(rows[0])
    for row in rows:
        teams_names.append((row[0], row[0]))  
    
    return teams_names

@app.route("/search", methods=['GET', 'POST'])
def search():
    form = SearchOption()
    option = ""
    view = "search"

    if request.method == 'POST':
        option = form.member.data

        if option == '/personal_records':
            return redirect(url_for('personal_records'))
        elif option == '/coach_records':
            return redirect(url_for('coach_records'))
        elif option == '/team_records':
            return redirect(url_for('team_records'))
    
    return render_template('search.html', title='Search', form=form, view=view)
    

if __name__ == '__main__':
    app.scheduler = scheduler
    app.scheduler.add_job(index, trigger='cron', year="*", month="*", day="*", hour="10", minute="0", second="0")
    # app.scheduler.add_job(index, trigger='cron', minute="*", second='10')
    app.scheduler.start()
    app.run(debug=True)