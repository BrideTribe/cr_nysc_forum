from flask import Flask, render_template, url_for
app = Flask(__name__)

posts = [
    {
        'author': 'Victor Abayomi',
        'title': 'NYSC Forum Post 1',
        'date_posted': 'June 11, 2018',
        'content': 'First NYSC Forum post content'
    },
    {
        'author': 'Opeyemi Susan',
        'title': 'NYSC Forum Post 2',
        'date_posted': 'June 11, 2018',
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

if __name__ == '__main__':
    app.run(debug=True) 