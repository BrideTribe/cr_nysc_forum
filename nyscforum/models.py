from datetime import datetime
from nyscforum import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    
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
        return f"User('{self.full_name}', '{self.state_code}', '{self.callup_no}', '{self.gender}', '{self.marital_status}', '{self.phone}', '{self.email}', '{self.state_of_origin}', '{self.lga}', '{self.address}', '{self.institution}', '{self.course}', '{self.qualification}', '{self.ppa}', '{self.password}', '{self.image_file}')"
        
class Post(db.Model):
    
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"