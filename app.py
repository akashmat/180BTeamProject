from flask import Flask, render_template, url_for, flash, redirect, request
from forms import RegistrationForm, LoginForm
import db_operations as dbOp
#from flask_mysqldb import MySQL

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
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('homeAdmin'))
        elif form.email.data == 'user@blog.com' and form.password.data == 'user_password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

#Database operations by Administer
@app.route("/homeAdmin")
def homeAdmin():
    return render_template('homeAdmin.html', posts=posts)

@app.route("/readDB", methods=['POST', 'GET'])
def readDB():
    try:
        if request.method == "POST":
            name = request.form['read']
            df = dbOp.read_sql("select * from " + name, 0)
            flash('Read successful!', 'success')
            return render_template("homeAdmin.html", tables=[df.to_html(classes='data', header="true")])
        else:
            return render_template("homeAdmin.html")
    except:
        return render_template("homeAdmin.html")

@app.route("/insertDB", methods=['POST', 'GET'])
def insertDB():
    try:
        if request.method == "POST":
            relation = request.form['relation']
            values = request.form.getlist('values')

            opDB = "INSERT INTO " + str(relation) + " "
            str_values = ""
            for x in values:
                str_values += str(x)
            opDB += "VALUES(" + str_values + ")"
            #print(opDB)
            dbOp.read_sql(opDB, 1)
            #flash('Write Success!', 'success')
            return render_template("homeAdmin.html")
        else:
            return render_template("homeAdmin.html")
    except:
        return render_template("homeAdmin.html")    


if __name__ == '__main__':
    app.run(debug=True)
