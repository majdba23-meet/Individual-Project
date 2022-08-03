from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

firebaseConfig = {
  "apiKey": "AIzaSyDTv5Sy_92EmCdIJqrFUFdJA8RYHA0p0LE",
  "authDomain": "miniproject-f0d46.firebaseapp.com",
  "databaseURL": "https://miniproject-f0d46-default-rtdb.europe-west1.firebasedatabase.app",
  "projectId": "miniproject-f0d46",
  "storageBucket": "miniproject-f0d46.appspot.com",
  "messagingSenderId": "157785869248",
  "appId": "1:157785869248:web:4a53fc4b4ea6901c5c9625",
  "measurementId": "G-16W7ZWX31T",
  "databaseURL": "https://miniproject-f0d46-default-rtdb.europe-west1.firebasedatabase.app/"
}

firebase= pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
db = firebase.database()


app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'


#my code:


@app.route('/', methods=['GET', 'POST'])
def signin():
	error = ""
	if request.method == 'POST':
		email = request.form['email']
		password = request.form['password']
		try:
			login_session['user'] = auth.sign_in_with_email_and_password(email, password)
			return redirect(url_for('shop'))
		except:
			error = "Authentication failed"
			return error
	return render_template("signin.html")




@app.route('/signup', methods=['GET', 'POST'])
def signup():
	error = ""
	if request.method == 'POST':
		email = request.form['email']
		password = request.form['password']
		full_name = request.form['text']
		try:
			login_session['user'] = auth.create_user_with_email_and_password(email, password)
			user= {'full_name' : full_name}
			db.child("Users").child(login_session['user']['localId']).set(user)
			return redirect(url_for('servey'))
		except:
		   error = "Authentication failed"
	return render_template("signup.html")

@app.route('/servey', methods=['GET', 'POST'])
def servey():
	error = ""
	if request.method == 'POST':
		age = request.form['age']
		diseases = request.form['diseases']
		allergy = request.form['allergy']
		try:
			user= {'age' : age, 'diseases' : diseases, 'allergy' : allergy, "cart" : {'blood':0}}
			db.child("Users").child(login_session['user']['localId']).set(user)
			return redirect(url_for('shop'))
		except:
		   error = "Authentication failed"
	return render_template("servey.html")

@app.route('/shop')
def shop():
	return render_template("shop.html")

@app.route('/add-cart', methods=['GET', 'POST'])
def add_cart():
	error = ""
	if request.method == 'POST':
		try:
			item = request.form['item']
			cart= db.child("Users").child(login_session['user']['localId']).child('cart').get().val()
			if item in cart:
				cart[item] +=1
			else:
				cart[item] = 1
			db.child("Users").child(login_session['user']['localId']).child('cart').update(cart)
			return redirect(url_for('shop'))
		except:
			error = "Authentication failed"
			print(error)
			return render_template("shop.html")


@app.route('/cart')
def cart():
	cart= db.child("Users").child(login_session['user']['localId']).child('cart').get().val()
	return render_template("cart.html", cart= cart)


@app.route('/pay')
def pay():
	return render_template("pay.html")


if __name__ == '__main__':
	app.run(debug=True)