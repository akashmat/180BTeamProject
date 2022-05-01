from flask import Flask, render_template, url_for, flash, redirect, request
from forms import RegistrationForm, LoginForm, TestForm
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
mysql = MySQL(app)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.config['MYSQL_PASSWORD'] = 'mp5301172'
app.config['MYSQL_DB'] = 'nfl'

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