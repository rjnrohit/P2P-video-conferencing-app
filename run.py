from flask import Flask,render_template,redirect , url_for,flash
from forms import LoginForm, RegistrationForm, LogoutForm ,AboutForm, HomeForm
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user,current_user,logout_user
from flask_socketio import SocketIO
#initiating flask app using Flask class
app=Flask(__name__)

#add secret key to app
app.config['SECRET_KEY']='c54c32b97493a7ec67c8af77'


#add url for site.db (Database)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'


#initiating app with flask Sqlalchemy
db = SQLAlchemy(app)
#creating data base models
class User(db.Model, UserMixin):
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


#add features of socket.io in flask app
socketio = SocketIO(app)



#Bcrypt class is used for password encryption and decryption
bcrypt = Bcrypt(app)




#make app compatible with flask-login
login_manager = LoginManager(app)
@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))
"""adding routes to home page
	-we can also access to home
	 page by another route home/username"""

@app.route("/home/")
@app.route("/home/<current_username>")


def home(current_username = None):
	""" if user is authenticated
		then render into home page 
		else direct into login page"""
	if current_user.is_authenticated :
		#A query to find username with given string
		if User.query.filter_by(username = current_username).first():
			current_username = current_username = User.query.filter_by(username = current_username).first().username
		else :
			current_username = None
		# here three were created for navigation to different pages through home pages
		Logout_Form = LogoutForm()
		About_Form = AboutForm()
		Login_Form = LoginForm()
		return render_template('home.html',current_username = current_username,LogoutForm= Logout_Form,LoginForm = Login_Form,AboutForm = About_Form)
	return redirect(url_for('login'))



@app.route("/about/")
@app.route("/about/<current_username>")


def about(current_username = None):
	# same comment as about
	if current_user.is_authenticated :
		if User.query.filter_by(username = current_username).first():
			current_username = current_username = User.query.filter_by(username = current_username).first().username
		else :
			current_username = None
		print(current_username)
		#again forms are created for same as written in above block in home
		Logout_Form = LogoutForm()
		Home_Form = HomeForm()
		Login_Form = LoginForm()
		return render_template('about.html',current_username = current_username,LogoutForm= Logout_Form,LoginForm = Login_Form,HomeForm = Home_Form)
	return redirect(url_for('login'))



@app.route('/register',methods=['GET','POST'])




def register():
	# user authentication
	if current_user.is_authenticated :
		print(current_user)
		return redirect (url_for('home',current_username = current_user.username))
	form = RegistrationForm()
	#validate all entered data before submmit action
	if form.validate_on_submit():
		#hash password
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = User(username = form.username.data, email = form.email.data, password = hashed_password)
		#check existence of user in database before adding it into database
		check_username = User.query.filter_by(username = user.username).first()
		#check existence of user in database before adding it into database
		check_email = User.query.filter_by(email = user.email).first()
		print(form.password.label())
		if check_username == None and check_email == None:
			db.session.add(user)
			db.session.commit()
			flash(f'account has been created successfully for {form.username.data}!','success')
			return redirect(url_for('login'))
		else :
			if check_username :
				error1 = 'username already taken'
				print(error1)
			else :
				error1 = None
			if check_email :
				error2 = 'email already taken'
			else :
				error2= None

			return render_template('register.html',title='register',form=form,error1 = error1,error2 = error2)

	return render_template('register.html',title='register',form=form)



@app.route('/login',methods=['GET','POST'])
@app.route("/",methods=['GET','POST'])



def login():
	if current_user.is_authenticated :
		print(current_user,current_user.is_authenticated)
		return redirect (url_for('home',current_username = current_user.username))
	form = LoginForm()
	if form.validate_on_submit():
		check_existence = User.query.filter_by(email = form.email.data).first()
		if check_existence and bcrypt.check_password_hash(check_existence.password,form.password.data):
			check_existence.id = check_existence.user_id
			login_user(check_existence, remember = False)
			#print(current_user.username)
			flash(f'logged in successfully {form.email.data}!','success')
			return redirect(url_for('home', current_username = check_existence.username))
		else:
			 if check_existence:
			 	print(User.query.filter_by(email = form.email.data),1)
			 	flash('Login unsuccessful. Please check your password that you entered','danger')
			 else :
			 	flash('Login unsuccessful. email not registered, please click at register ','danger')
	return render_template('login.html',title='login',form=form)
@app.route("/logout")
def logout():
	logout_user()
	print(current_user.is_authenticated)
	return redirect(url_for('login'))

if __name__=='__main__':
	db.create_all()
	#app.run(debug=False)
	socketio.run(app)
