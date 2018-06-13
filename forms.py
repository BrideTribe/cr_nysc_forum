from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class RegistrationForm(FlaskForm):
    full_name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=100)])
    state_code = StringField('State Code', validators=[DataRequired(), Length(max=11)])
    gender = StringField('Gender', validators=[DataRequired(), Length(min=4, max=6)])
    marital_status = StringField('Marital Status', validators=[DataRequired(), Length(max=25)])
    phone = StringField('Mobile No', validators=[DataRequired(), Length(max=15)])
    email = StringField('E-Mail', validators=[DataRequired(), Email(), Length(max=200)])
    state_of_origin = StringField('State of Origin', validators=[DataRequired(), Length(max=50)])
    lga = StringField('LGA', validators=[DataRequired(), Length(max=100)])
    address = StringField('Home Address', validators=[DataRequired(), Length(max=250)])
    institution = StringField('Institution', validators=[DataRequired(), Length(max=250)])
    course = StringField('Course of Study', validators=[DataRequired(), Length(max=100)])
    qualification = StringField('Qualification', validators=[DataRequired(), Length(min=3, max=10)])
    ppa = StringField('PPA', validators=[DataRequired(), Length(min=2, max=200)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=4)]) 
    confirm_password = PasswordField('Confirm Password', validators==[DataRequired(), Length(min=4), EqualTo('password')])
    submit = SubmitField('Register')

class LoginForm(FlaskForm) :
    email = StringField('E-Mail', validators=[DataRequired(), Email(), Length(max=200)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=4)])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login') 