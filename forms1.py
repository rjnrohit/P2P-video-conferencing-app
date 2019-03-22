from flask_wtf import *
from wtforms import *
from wtforms.validators import *
class RegistrationForm(FlaskForm):
	  username= StringField('Username',validators=[DataRequired(),Length(min=2,max=20)]
	  email = StringField('email',validators=[DataRequired(),Email()])
	  password = passwordField('password',validators=[DataRequired()])
	  confirm_password = passwordField('confirm_password',validators=[DataRequired(),EqualTo('password')])
	  submit = SubmitField('Sign Up')
class LoginForm(FlaskForm):
	  email = StringField('email',validators=[DataRequired(),Email()])
	  password = passwordField('password',validators=[DataRequired()])
	  remember = BooleanField('Remember me')
	  submit = SubmitField('login')

