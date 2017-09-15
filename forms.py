from flask_wtf import FlaskForm
from wtforms import PasswordField
from wtforms import SubmitField
from wtforms.fields.html5 import EmailField
from wtforms import validators
from wtforms import TextField
from wtforms import SelectField
from dbhelper import DBHelper

DB = DBHelper()


class RegistrationForm(FlaskForm):
	email = EmailField('email',
	validators = [validators.DataRequired(), validators.Email()])
	password = PasswordField('password',
	validators = [validators.DataRequired(),
	validators.Length(min=8, message="Please choose a password of at least 8 characters")])
	password2 = PasswordField('password2',
	validators = [validators.DataRequired(),
	validators.EqualTo('password', message="Passwords must match")])
	submit = SubmitField('submit', [validators.DataRequired()])

class LoginForm(FlaskForm):
	loginemail = EmailField('email',
	validators = [validators.DataRequired(), validators.Email()])
	loginpassword = PasswordField('password',
	validators = [validators.DataRequired(message="Password is required")])
	submit = SubmitField('submit', [validators.DataRequired()])

class CreateTableForm(FlaskForm):
	tablenumber = TextField('tablenumber',
	validators = [validators.DataRequired()])
	submit = SubmitField('createtablesubmit',
	validators = [validators.DataRequired()])

class CreateMenuCategorieForm(FlaskForm):
	categorie_name = TextField('categorie_name',
	validators = [validators.DataRequired()])
	submit = SubmitField('createmenucategorie',
	validators = [validators.DataRequired()])

class AddMenuItemForm(FlaskForm):
	item = TextField('item', 
	validators = [validators.DataRequired()])
	description = TextField('description',
	validators = [validators.DataRequired()])
	price = TextField('price',
	validators = [validators.DataRequired()])
	submit = SubmitField('addmenuitem',
	validators = [validators.DataRequired()])

