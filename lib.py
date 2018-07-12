from flask import Flask, render_template, url_for
from forms import RegistrationForm, LoginForm

app = Flask(__name__)

app.config['SECRET_KEY'] = '8639f43b71b224ad036d1047322a6b39'
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
        'content': 'Second NYSC Forum post content'
    }
]

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/register")
def register():
    form = RegistrationForm()
    return render_template('register.html', title='Register', form=form)

@app.route("/login")
def login():
    form = LoginForm()
    return render_template('login.html', title='Login', form=form)

if __name__ == '__main__':
    app.run(debug=True) 