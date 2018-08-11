from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = '8639f43b71b224ad036d1047322a6b39'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///nysc.db'
db = SQLAlchemy(app)

class User(db.Model):
    
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    state_code = db.Column(db.String(20), unique=True, nullable=False)
    callup_no = db.Column(db.String(50), unique=True, nullable=False)
    gender = db.Column(db.String(6), nullable=False)
    marital_status = db.Column(db.String(25), nullable=False)
    phone = db.Column(db.String(15), unique=True, nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    state_of_origin = db.Column(db.String(50), nullable=False)
    lga = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(250), nullable=False)
    institution = db.Column(db.String(250), nullable=False)
    course = db.Column(db.String(100), nullable=False)
    qualification = db.Column(db.String(10), nullable=False)
    ppa = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(60), nullable=False)
    #confirm_password = db.Column(db.String(60), nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    post = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return "User('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(
                    self.full_name, self.state_code, self.callup_no, self.gender, self.marital_status,
                    self.phone, self.email, self.state_of_origin, self.lga, self.address, self.institution, self.course, 
                    self.qualification, self.ppa, self.password, self.image_file)
        
class Post(db.Model):
    
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(users.id), nullable=False)

    def __repr__(self):
        return "Post('{}', '{}')".format(self.title, self.date_posted)

posts = [
    {
        'author': 'Victor Abayomi',
        'title': 'NYSC Forum Post 1',
        'date_posted': 'June 11, 2018',
        'content': 'First NYSC Forum post content'
    },
    {
        'author': 'Opeyemi Emmanuel',
        'title': 'NYSC Forum Post 2',
        'date_posted': 'June 30, 2018',
        'content': 'Second NYSC Forum post content'
    },
    {
        'author': 'Name Susan',
        'title': 'NYSC Forum Post 3',
        'date_posted': 'July 12, 2018',
        'content': 'Third NYSC Forum post content'
    }
]

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        flash('Account created for {RegistrationForm.full_name.data} successfully!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    
    if form.validate_on_submit():
        if form.email.data == 'ritymontero@gmail.com' and form.password.data == 'password':
            flash('Login Successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Email or Password incorrect', 'danger')
    return render_template('login.html', title='Login', form=form)

if __name__ == '__main__':
    app.run(debug=True) 