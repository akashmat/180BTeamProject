from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo


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
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class TestForm(FlaskForm):
    member = SelectField('Select Member ', choices =[])
    submit = SubmitField('Search')    

class SearchOption(FlaskForm):
    choices = [('/personal_records', 'Players'), ('/coach_records', 'Coaches'), ('/team_records', 'Teams')]
    member = SelectField('Select Member Type ', choices =choices)
    submit = SubmitField('Search')
