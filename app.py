from flask import *
from forms import *
app=Flask(__name__)
app.config['SECRET_KEY']='c54c32b97493a7ec67c8af77'
posts=[
	{
	'author' : 'rajiv ranjan',\
	'post_title': 'about pulwama',\
	'date_posted' : '21 apr 2019',\
	'content' : 'pak terrorists attacked on indian army in pulwama at 31st feb'
	},\
	{
	'author' : 'rohit ranjan',\
	'post_title' :'about air strike',\
	'date_posted' :'22 apr 2019',\
	'content' : 'in reply , india gives air strikes to pak terrorists'
	}
]
@app.route("/")
@app.route("/home")
def home():
	return render_template('home.html',posts=posts)
@app.route("/about/")
def about():
	return render_template('about.html')
@app.route('/register')
def register():
	form = RegistrationForm()
	return render_template('register.html',title='register',form=form)
@app.route('/login')
def login():
	form = LoginForm()
	return render_template('login.html',title='login',form=form)
if __name__=='__main__':
	app.run(debug=True)