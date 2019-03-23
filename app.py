from flask import *
from forms import *
from flask_sqlalchemy import SQLAlchemy
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
	'content' : 'in reply , india gave air strikes to pak terrorists'
	}
]
@app.route("/home")
def home():
	form = AboutForm()
	return render_template('home.html',posts=posts,form= form)
@app.route("/about/")
def about():
	return render_template('about.html')
@app.route('/register',methods=['GET','POST'])
def register():
	form = RegistrationForm()
	if form.validate_on_submit():
		flash(f'account created successfully for {form.username.data}!','success')
		return redirect(url_for('login'))

	return render_template('register.html',title='register',form=form)
@app.route('/login',methods=['GET','POST'])
@app.route("/",methods=['GET','POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		flash(f'logged in successfully {form.email.data}!','success')
		return redirect(url_for('home'))
	return render_template('login.html',title='login',form=form)
if __name__=='__main__':
	app.run(debug=True)