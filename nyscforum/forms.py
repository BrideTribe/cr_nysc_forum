from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from nyscforum.models import User

class RegistrationForm(FlaskForm):
    full_name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=100)])
    state_code = StringField('State Code', validators=[DataRequired(), Length(max=20)])
    callup_no = StringField('Callup No', validators=[DataRequired(), Length(max=50)])
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
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), Length(min=4), EqualTo('password')])
    submit = SubmitField('Register')

    #Fields input validation
    def validate_fullname(self, full_name):
        user = User.query.filter_by(full_name=full_name.data).first()
        if user:
            raise ValidationError(f'{self.full_name.data} already exist!')

    def validate_state_code(self, state_code):
        user = User.query.filter_by(state_code=state_code.data).first()
        if user:
            raise ValidationError(f'{self.state_code} already exist, try a different state code.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(f'{self.email} already exist, try a different email address.')
    
    def validate_phone(self, phone):
        user = User.query.filter_by(phone=phone.data).first()
        if user:
            raise ValidationError(f'{self.phone.data} already exist, try another phone number.')

class LoginForm(FlaskForm) :
    email = StringField('E-Mail', validators=[DataRequired(), Email(), Length(max=200)])
    state_code = StringField('State Code', validators=[DataRequired(), Length(max=11)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=4)])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login') 

class UpdateAccountForm(FlaskForm):
    full_name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=100)])
    state_code = StringField('State Code', validators=[DataRequired(), Length(max=20)])
    callup_no = StringField('Callup No', validators=[DataRequired(), Length(max=50)])
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
    
    picture = FileField('Update profile picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    #Fields input validation
    def validate_full_name(self, full_name):
        if full_name.data != current_user.full_name:
            user = User.query.filter_by(full_name=full_name.data).first()
            if user:
                raise ValidationError(f'{self.full_name.data} already exist!')

    def validate_state_code(self, state_code):
        if state_code.data != current_user.state_code:
            user = User.query.filter_by(state_code=state_code.data).first()
            if user:
                raise ValidationError(f'{self.state_code} already exist, try a different state code.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError(f'{self.email} already exist, try a different email address.')

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')