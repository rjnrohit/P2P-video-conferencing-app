from flask_wtf import *
from wtforms import *
from wtforms.validators import *
class LoginForm(FlaskForm):
		  email = StringField('email',validators=[DataRequired(),Email()])
		  password = PasswordField('password',validators=[DataRequired()])
		  remember = BooleanField('Remember me')
		  submit = SubmitField('login')
class RegistrationForm(FlaskForm):
	username= StringField('Username',validators=[DataRequired(),Length(min=2,max=20)])
	email = StringField('email',validators=[DataRequired(),Email()])
	password = PasswordField('password',validators=[DataRequired()])
	confirm_password = PasswordField('confirm_password',validators=[DataRequired(),EqualTo('password')])
	submit = SubmitField('Sign Up')
class AboutForm(FlaskForm):
	submit= SubmitField('About')
class LogoutForm(FlaskForm):
	submit = SubmitField('log out')
class HomeForm(FlaskForm):
	submit = SubmitField('home')