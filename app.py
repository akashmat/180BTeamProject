from flask import Flask, render_template, url_for, flash, redirect, request
from forms import RegistrationForm, LoginForm, TestForm
from flask_mysqldb import MySQL
from flask_session import Session
#import pyodbc

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
mysql = MySQL(app)
#connection = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=DESKTOP-31O3JDL\SQLEXPRESS01;DATABASE=nfl;Trusted_Connection=yes;')
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.config['MYSQL_PASSWORD'] = 'mp5301172'
app.config['MYSQL_DB'] = 'nfl'

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
session = Session(app)


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
#    if not session.get("name"):
#        # if not there in the session then redirect to the login page
#        return redirect("/login")

    return render_template('home.html', posts=posts)


@app.route("/about")
def about():
#    if not session.get("name"):
#        return redirect("/login")

    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        session["name"] = request.form.get("name")
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


@app.route("/personal_records", methods=['GET', 'POST'])
def personal_records():
    form = TestForm()
    player_id = ""

    if request.method == 'POST':
        player_id = form.member.data
        #player_id =form.player_id.data
        cursor = mysql.connection.cursor()
        print(player_id)
        query = "SELECT * FROM PLAYER_SCORE WHERE pscore_id = {0}".format(player_id)
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
    cursor = mysql.connection.cursor()
    # Queries the First and Last Names of Players from the Team Member Table
    query_names = "SELECT DISTINCT t.fname, t.lname, t.member_id \
                  FROM TEAM_MEMBER t JOIN PLAYER_SCORE p ON t.member_id = p.pscore_id \
                  ORDER BY t.member_id ASC"
    cursor.execute(query_names)
    # A dictionary of rows of resultant query
    rows = cursor.fetchall()
    players_names = []
    for row in rows:
        players_names.append((row['member_id'], "{0} {1}".format(row['fname'], row['lname'])))  
    
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
        cursor = mysql.connection.cursor()
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
    cursor = mysql.connection.cursor()
    # Queries the First and Last Names of Players from the Team Member Table
    query_names = "SELECT DISTINCT t.fname, t.lname, t.member_id \
                  FROM TEAM_MEMBER t JOIN COACH_SCORE c ON t.member_id = c.cscore_id \
                  ORDER BY t.member_id ASC"
    
    cursor.execute(query_names)
    rows = cursor.fetchall()
    coaches_names = []
    for row in rows:
        coaches_names.append((row['member_id'], "{0} {1}".format(row['fname'], row['lname'])))  
    
    return coaches_names
#------------------------------------teams------------------------------------------------------
@app.route("/team_records", methods=['GET', 'POST'])
def team_records():
    form = TestForm()
    view = 'team_records'
    team_id = ""

    if request.method == 'POST':
        team_id = form.member.data
        cursor = mysql.connection.cursor()
        query_name = "SELECT * FROM TEAM_SCORE ts \
                      WHERE ts.t_name = '{0}'".format(team_id)
        cursor.execute(query_name)
        stats = cursor.fetchall()
    
        return render_template('statsteam.html', stats=stats, view=view)
        
    teams_names = select_teams() 
    form.member.choices = teams_names
    
    return render_template('search.html', title='Team', form=form, view=view)

def select_teams():
    cursor = mysql.connection.cursor()
    query_names = "SELECT DISTINCT t.team_name \
		           FROM TEAM t JOIN TEAM_SCORE ts ON t.team_name = ts.t_name;"
    cursor.execute(query_names)
    rows = cursor.fetchall()
    teams_names = []

    for row in rows:
        teams_names.append((row['team_name'], row['team_name']))  
    
    return teams_names

@app.route("/logout")
def logout():
    session["name"] = None
    return redirect("/")

poll_data = {
   'question' : 'Which team do you think will win?',
   'fields'   : ['team1', 'team2']
   
}

#---------------------------------------------Jesse T-------------------------------------------
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
#---------------------------------------------Jesse T-------------------------------------------

if __name__ == '__main__':
    app.run(debug=True)