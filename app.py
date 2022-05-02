import email
from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm
from flask_mysqldb import MySQL

from sqlalchemy import create_engine
import pandas as pd

#For Notifications: Mail
from flask_mail import Mail, Message
from apscheduler.schedulers.background import BackgroundScheduler


app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
mysql = MySQL(app)

Server = "DESKTOP-BS4D8BR\SQLEXPRESS"

Database = "nfl"
Driver = "ODBC Driver 17 for SQL Server"
Database_Con = f'mssql://@{Server}/{Database}?driver={Driver}'

engine = create_engine(Database_Con)
con = engine.connect()

app.config['MAIL_SERVER']='smtp.mailtrap.io'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'accf3746129f8f'
app.config['MAIL_PASSWORD'] = '450a1a7b606995'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
mail = Mail(app)

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
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


scheduler = BackgroundScheduler()
def index():
    email_query= 'select email from MATCH join NOTIFIES on match_id=m_id join FAN on p_id =profile_id where  date = CAST( GETDATE()+1 as date)'
    email_data = pd.read_sql_query(email_query, con)
    email_list = email_data['email'].to_list() 
    if len(email_list) > 0:    
        with app.app_context():    
            msg = Message('Hello, Its match day!', sender = 'ankur@mailtrap.io', recipients = email_list)
            msg.body = "Match Notification"
            mail.send(msg)
            print("done")


if __name__ == '__main__':
    app.scheduler = scheduler
    app.scheduler.add_job(index, trigger='cron', year="*", month="*", day="*", hour="10", minute="0", second="0")
    app.scheduler.start()
    app.run(debug=True)