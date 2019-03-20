from flask import *
app=Flask(__name__)
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
if __name__=='__main__':
	app.run(debug=True)