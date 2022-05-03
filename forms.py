# SJSU CMPE 138 Spring 2022 TEAM9 

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo
import signup_api, login_api, profile_api


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    usertype = SelectField('User Type', choices = [('fan', 'Fan'), ('admin', 'Admin')])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

''''
class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
'''
class TestForm(FlaskForm):
    member = SelectField('Select Member ', choices =[])
    submit = SubmitField('Search')    

class SearchOption(FlaskForm):
    choices = [('/personal_records', 'Players'), ('/coach_records', 'Coaches'), ('/team_records', 'Teams')]
    member = SelectField('Select Member Type ', choices =choices)
    submit = SubmitField('Search')

class ProfileForm(FlaskForm):
    data = profile_api.getteams()
    print(data)
    li = []
    for d in data:
        li.append(d[0])
    print(li)
    favteam = SelectField('FavTeam', choices=li,)
    followteam = SelectField('FollowTeam', choices=li,)
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])

class SearchForm(FlaskForm):
    playername = SelectField()