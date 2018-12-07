import os #to capture picture extension
import secrets  #this is for the picture function
from PIL import Image #python image processing module
from flask import render_template, url_for, flash, redirect,request, abort
from nyscforum import app, db, bcrypt
from nyscforum.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from nyscforum.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required

@app.route("/")
@app.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
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

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/images', picture_fn)
    
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

@app.route("/account", methods=['GET','POST'])
@login_required
def account():
    form = UpdateAccountForm()

    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.full_name = form.full_name.data
        current_user.state_code = form.state_code.data 
        current_user.callup_no = form.callup_no.data
        current_user.gender = form.gender.data
        current_user.marital_status = form.marital_status.data
        current_user.phone = form.phone.data
        current_user.email = form.email.data
        current_user.state_of_origin = form.state_of_origin.data
        current_user.lga = form.lga.data
        current_user.address = form.address.data
        current_user.institution = form.institution.data
        current_user.course = form.course.data 
        current_user.qualification = form.qualification.data
        current_user.ppa = form.ppa.data

        db.session.commit()
        #Process complete message.
        flash('Your account has been updated successfully!', 'success')

        return redirect(url_for('account'))

    elif request.method == 'GET':
        form.full_name.data = current_user.full_name 
        form.state_code.data =  current_user.state_code 
        form.callup_no.data = current_user.callup_no 
        form.gender.data = current_user.gender 
        form.marital_status.data = current_user.marital_status 
        form.phone.data = current_user.phone 
        form.email.data = current_user.email 
        form.state_of_origin.data = current_user.state_of_origin 
        form.lga.data = current_user.lga 
        form.address.data = current_user.address 
        form.institution.data = current_user.institution
        form.course.data =  current_user.course 
        form.qualification.data = current_user.qualification 
        form.ppa.data =current_user.ppa 
    image_file = url_for('static', filename='images/'+ current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form) 

@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()

    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title='New Post', 
                            form=form, legend='New Post')

@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)

@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post', 
                            form=form, legend='Update Post')

@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted', 'success')
    return redirect(url_for('home'))


@app.route("/user/<string:full_name>")
def user_posts(full_name):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(full_name=full_name).first_or_404()
    posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc())\
            .paginate(page=page, per_page=5)
    return render_template('user_posts.html', posts=posts, user=user) 