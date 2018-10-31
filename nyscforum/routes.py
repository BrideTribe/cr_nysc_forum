from flask import render_template, url_for, flash, redirect,request
from nyscforum import app, db, bcrypt
from nyscforum.forms import RegistrationForm, LoginForm
from nyscforum.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required

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
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = RegistrationForm()
    #field validation and hash password
    if form.validate_on_submit():
        h_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(full_name=form.full_name.data, state_code=form.state_code.data, callup_no=form.callup_no.data,
                    gender=form.gender.data, marital_status=form.marital_status.data, phone=form.phone.data,
                    email=form.email.data, state_of_origin=form.state_of_origin.data, lga=form.lga.data,
                    address=form.address.data, institution=form.institution.data, course=form.course.data, 
                    qualification=form.qualification.data, ppa=form.ppa.data, password=h_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.full_name.data} successfully!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()
    
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data, state_code=form.state_code.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Check your email, state code, password and try again', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/account")
@login_required
def account():
    return render_template('account.html', title='Account') 