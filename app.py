from flask import Flask, render_template, request, flash, redirect,url_for
from forms import LoginForm, RegistrationForm,PasswordForm
from flask_login import UserMixin, login_user, login_required, logout_user, current_user, LoginManager
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__    )

# Secret Key
app.config['SECRET_KEY'] = "IITMadrasMAD1"
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///data.db'

# init db
db = SQLAlchemy(app)
migrate = Migrate(app, db)

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

class Products(db.Model):
    productId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(200))
    imgage = db.Column(db.String, nullable=False)
    stock = db.Column(db.Integer)
    categoryId = db.Column(db.Integer, foreign_keys=True, nullable=False)


# Flask Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'Login'

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


@app.route('/', methods=['GET','POST'])
@login_required
def index():
    user = None
    if current_user.is_authenticated:
        user = current_user
    return render_template('base.html',user=user)


@app.route('/Users_pwd', methods=['GET','POST'])
def Users_pwd():
    email = None
    password = None
    pw_to_check = None
    passed = None
    form = PasswordForm()
    # Validation
    if form.validate_on_submit():
        email = form.email.data
        password = form.password_hash.data
        form.password, form.email = '',''

        pw_to_check = Users.query.filter_by(email=email).first()
        # check hashed password
        passed = check_password_hash(pw_to_check.password_hash, password)

    return render_template('user.html', password=password ,email= email,pw_to_check=pw_to_check, form=form , passed=passed)

@app.route('/register',methods=['GET','POST'])
def add_user():
    username = None
    user = None
    form = RegistrationForm()
    
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is  None:
            # hashing password
            hashed_pw = generate_password_hash(form.password_hash.data, "sha256")
            user = Users(username=form.username.data, email=form.email.data, password_hash=hashed_pw)
            db.session.add(user)
            db.session.commit()
        username = form.username.data
        form.username.data  =''
        form.email.data = ''
        form.password_hash.data =''

        flash("User added Succesful")
    # our_users = Users.query.order_by(Users.date_added)
    return render_template('add_user.html', form=form, username=username,user=user)


@app.route('/login', methods=['POST','GET'])
def Login():
    lform = LoginForm()
    # validation
    if lform.validate_on_submit():
        user = Users.query.filter_by(email=lform.email.data).first()
        if user:
            if check_password_hash(user.password_hash, lform.password.data):
                login_user(user)
                flash("Login Succesfull!!")
                return redirect(url_for('index'))
            else:
                flash("Wrong Password - Try Again!")
        else:
            flash("User does'nt exist - Try Again!")

    return render_template('login.html',form=lform)

# Logout page
@app.route('/logout', methods=['POST','GET'])
@login_required
def logout():
    logout_user()
    flash("You have been Logged out!")
    return redirect(url_for('index'))

# @app.route('/register', methods=['POST','GET'])
# def Register():
#     rform = RegistrationForm()
#     # validation
#     if rform.validate_on_submit():
#         username = rform.username.data
#         email = rform.email.data
#         password = rform.password.data
#         confirm_password = rform.confirm_password.data
#         flash("Login Succesful")
#     print(username, email)
#     return render_template('register.html',form=rform)

if __name__ == '__main__':
    app.debug = True
    app.run()