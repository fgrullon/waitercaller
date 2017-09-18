from flask import Flask
from flask import render_template
from flask_login import LoginManager
from flask_login import login_required
from flask_login import login_user
from flask_login import logout_user
from user import User
from flask import redirect
from flask import url_for
from flask import request
from passwordhelper import PasswordHelper
from flask_login import current_user
import config
if config.test:
   from mockdbhelper import MockDBHelper as DBHelper
else:
   from dbhelper import DBHelper
from bitlyhelper import BitlyHelper
import datetime
from forms import RegistrationForm
from forms import LoginForm
from forms import CreateTableForm
from forms import CreateMenuCategorieForm
from forms import AddMenuItemForm


app = Flask(__name__)
DB = DBHelper()
PH = PasswordHelper()
BH = BitlyHelper()
login_manager = LoginManager(app)
app.secret_key = 'gev9wVwKUiRzdgptOzNFrC/3AfaTLAlZ7OmzTC17eV6T2bMTtmvKL5biAl5FnbU999chgOHcoovRNJN0Ky+s6NbQvJc/VkxtBlZA'


@app.route("/")
def home():
	return render_template("home.html", loginform=LoginForm(), registrationform=RegistrationForm())

@app.route("/login", methods=["POST"])
def login():
	form = LoginForm(request.form)
	if form.validate():
		stored_user = DB.get_user(form.loginemail.data)
		if stored_user and PH.validate_password(form.loginpassword.data, stored_user['salt'], stored_user['hashed']):
			user = User(form.loginemail.data)
			login_user(user, remember=True)
			return redirect(url_for('account'))
		form.loginemail.errors.append("Email or password invalid")
	return render_template("home.html", loginform=form,
	registrationform=RegistrationForm())

@app.route("/register", methods=["POST"])
def register():
	form = RegistrationForm(request.form)
	if form.validate():
		if DB.get_user(form.email.data):
			form.email.errors.append("Email addres already registered")
			return render_template('home.html', loginform=LoginForm(), registrationform=form)
		salt = str(PH.get_salt())
		hashed = PH.get_hash(form.password2.data + salt)
		DB.add_user(form.email.data, salt, hashed)
		return render_template("home.html", loginform=LoginForm(), registrationform=form, onloadmessage="Registration successful. Please log in.")
	return render_template('home.html', loginform=LoginForm(), registrationform=form)

@app.route("/logout")
def logout():
	logout_user()
	return redirect(url_for("home"))

@login_manager.user_loader
def load_user(user_id):
	user_password = DB.get_user(user_id)
	if user_password:
		return User(user_id)

@app.route("/dashboard")
@login_required
def dashboard():
	now = datetime.datetime.now()
	requests = DB.get_requests(current_user.get_id())
	for req in requests:
		deltaseconds = (now - req['time']).seconds
		req['wait_minutes'] = "{}.{}".format((deltaseconds/60), str(deltaseconds % 60).zfill(2))
	return render_template("dashboard.html", requests=requests)

@app.route("/dashboard/resolve")
@login_required
def dashboard_resolve():
	request_id = request.args.get("request_id")
	DB.delete_request(request_id)
	return redirect(url_for('dashboard'))

@app.route("/account")
@login_required
def account():
	tables = DB.get_tables(current_user.get_id())
	return render_template("account.html", createtableform=CreateTableForm(), 
	tables=tables, createmenucategorieform=CreateMenuCategorieForm(), addmenuitemform=AddMenuItemForm())

@app.route("/account/createtable", methods=["POST"])
@login_required
def account_createtable():
	form = CreateTableForm(request.form)
	if form.validate():
		tableid = DB.add_table(form.tablenumber.data,
		current_user.get_id())
		new_url = BH.shorten_url(config.base_url + "/newrequest/" +
		str(tableid))
		DB.update_table(tableid, new_url)
		return redirect(url_for('account'))
	return render_template("account.html", createtableform=form,
	tables=DB.get_tables(current_user.get_id()))

@app.route("/account/deletetable", methods=["POST"])
@login_required
def account_deletetable():
	tableid = request.form.get("tableid")
	DB.delete_table(tableid)
	return redirect(url_for('account'))

@app.route("/newrequest/<tid>")
def newrequest(tid):
	if DB.add_request(tid, datetime.datetime.now()):
		return "Your request has been logged and a waiter will be with you shortly."
	return "There is already a request pending for this table. Please be patient, a waiter will be there ASAP."

@app.route("/orders")
@login_required
def order_mag():
	return render_template("orders.html")

@app.route("/orders/addcategorie", methods=["POST"])
@login_required
def order_addcategorie():
	form = CreateMenuCategorieForm(request.form)
	categories = [c['categorie_name'] for c in DB.get_categories_name()]
	if form.validate():
		if form.categorie_name.data in categories:
			form.categorie_name.errors.append("Category already registered")
			return render_template("account.html", createmenucategorieform=form, addmenuitemform=AddMenuItemForm())
		name = form.categorie_name.data
		DB.add_categories(name)
		return redirect(url_for('account'))
	return render_template("account.html", createmenucategorieform=form,
		  addmenuitemform=AddMenuItemForm())

@app.route("/orders/addmenuitem", methods=["POST"])
@login_required
def order_addmenuitem():
	form = AddMenuItemForm(request.form)
	if form.validate():
		name = form.name.data
		item = form.item.data
		description = form.description.data
		price = form.price.data
		DB.add_menu_items(name, item, description, price)
		return redirect(url_for('account'))
	return render_template("account.html")



if __name__ == "__main__":
	app.run(port=5000, debug=True)
