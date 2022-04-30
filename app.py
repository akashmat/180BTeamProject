from flask import Flask, request, render_template, url_for, flash, redirect, session
from datetime import date
import random

#from flask_mysqldb 
#from flask_sqlalchemy import SQLAlchemy
#db = SQLAlchemy()

import db_operations as dbOp


app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
#mysql = MySQL(app)

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
    session['user'] = 'user1'
    return redirect(url_for("homeAdmin"))
'''
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'adminPassword':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        elif form.email.data == 'user@blog.com' and form.password.data == 'userPassword':
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')

    return render_template('login.html', title='Login', form=form)
'''

@app.route("/createPoll", methods=['POST', 'GET'])
def createPoll():
    if request.method == "POST":
        team1 = request.form['team1']
        team2 = request.form['team2']
        duration = request.form['duration']
        poll_name = request.form['poll_name']
        creation_date = date.today()
        creator_name = session['user']
        poll_percentage = "00%-00%"
        poll_predictions = 0
        poll_data['question'] = poll_name

        rand_id = random.randint(1, 1000)

        df_id = dbOp.read_sql_raw("SELECT poll_id from POLLS")

        #ensures that member_id will be unique
        check_random = 1
        while check_random == 1:
            for id in df_id['poll_id']:
                if rand_id == id:
                    rand_id = random.randint(1, 1000)
                    continue
            check_random = 0

        sql_op = f"{rand_id}, \'{creator_name}\', {duration}, \'{creation_date}\', \'{poll_name}\', \'{poll_percentage}\', {poll_predictions}, \'{team1}\', \'{team2}\'"
        check_flag = dbOp.insert_sql("POLLS", sql_op)
        if check_flag:
            flash('Poll: Created', 'success')
        else:
            flash('Poll: Not Created', 'danger')
        #opDB = "INSERT INTO " + str(team2) + " "
    return render_template("homeAdmin.html")

poll_data = {
   'question' : 'Which team do you think will win?',
   'fields'   : ['team1', 'team2']
   
}

#Polling 
@app.route("/rootPoll")
def poll():
    df_com = dbOp.read_sql_raw("select * from POLLS")
    return render_template('poll.html', data=poll_data, data1=df_com['poll_name'].iloc[0], a=df_com['team_name1'].iloc[0], b=df_com['team_name2'].iloc[0])

@app.route("/poll", methods =['POST', 'GET'])
def countVote():

    df_poll = dbOp.read_sql_raw("select * from POLLS")
    #array_pollid = df_poll['poll_id']
    array_name = df_poll['poll_name']
    array_prcentage = df_poll['poll_percentage']


    string_percentage = array_prcentage[1]

    vote = request.args.get('field')
    
    out = open('data.txt', 'a')
    out.write( vote + '\n' )
    out.close()

    votes = {}
    for f in poll_data['fields']:
        votes[f] = 0
        total = 0
        count1 = 0
        count2 = 0
        
    f = open('data.txt', 'r')
    for line in f:
        vote = line.rstrip("\n")
        votes[vote] += 1
        total += 1
        if vote == 'team1':
            count1 += 1
        else:
            count2 += 1

    percentage1 = (count1 / total) * 100
    percentage2 = (count2 / total) * 100

    df_comments = dbOp.read_sql_raw("select * from INTERACTS as I join POLLS as P on I.ip_id = P.poll_id where poll_name = 'poll1'")
    comments = df_comments['comments']
    print(comments)
    #dbOp.update_sql('polls', "poll_percentage = \'{vote}\'", "poll_name = \'{data.question}\'")
        #10%-90%
    return render_template('results.html', comments=comments, total=total, percentage1=percentage1, percentage2=percentage2, data=poll_data, votes=votes)


# Database operations by Administer
@app.route("/homeAdmin")
def homeAdmin():
    if not ('user' in session and session['user'] == 'user1'):
        return redirect(url_for('login'))
    else:
        return render_template('homeAdmin.html')

@app.route("/readDB", methods=['POST', 'GET'])
def readDB():
    if request.method == "POST":
        name = request.form['read']

        df = dbOp.read_sql("*", str(name), "", "", "", "")
        return render_template("homeAdmin.html", tables=[df.to_html(classes='data', header="true")])
    else:
        return render_template("homeAdmin.html")



if __name__ == '__main__':
    app.run(debug=True)