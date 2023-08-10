
from flask_login import UserMixin, login_user, login_required, logout_user, current_user, LoginManager
from app import db
import datetime 
from werkzeug.security import generate_password_hash, check_password_hash



# DB Model for Users name
class Users(db.Model, UserMixin):
    id  = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200),nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    # password
    password_hash = db.Column(db.String(128))
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<Name %r>' % self.name

# Products table 
class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    image = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return f'<Products {self.name}>'

# Categories model
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    products = db.relationship('Products', backref='category', lazy=True)

    def __repr__(self):
        return f'<Category {self.name}>'
    
