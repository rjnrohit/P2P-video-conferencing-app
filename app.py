from flask import *
from forms import *
from datetime import *
from flask_sqlalchemy import SQLAlchemy
app=Flask(__name__)


app.config['SECRET_KEY']='c54c32b97493a7ec67c8af77'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'

db = SQLAlchemy(app)

class User(db.Model):
	user_id = db.Column(db.Integer, primary_key = True)
	username = db.Column(db.String(20), unique = True , nullable = False)
	email =  db.Column(db.String(120), unique = True , nullable = False)
	password = db.Column(db.String(60), nullable = False)
	posts = db.relationship('Post',backref = 'author', lazy= True)

	def __repr__(self):
		return f"User('{self.username}','{self.email}','{self.password}')"
class Post(db.Model):
	post_id = db.Column(db.Integer, primary_key= True)
	title= db.Column(db.String(100), nullable = False) 
	date_posted = db.Column(db.DateTime, nullable= False,default = datetime.now)
	content = db.Column(db.Text , nullable = False)
	user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)

	def __repr__(self):
		return f"POST('{self.title}','{self.date_posted}')"

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