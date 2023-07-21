from flask import Flask, render_template, request, flash
from forms import LoginForm, NamForm,RegistrationForm
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

# class Users(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(200), nullable=False)
#     email = db.Column(db.String(100), nullable=False, unique=True)
#     id = db.Column(db.Integer)

# DB Model for Test name
class Test(db.Model):
    id  = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200),nullable=False)
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



@app.route('/', methods=['GET','POST'])
def index():
    return render_template('base.html')


@app.route('/name', methods=['GET','POST'])
def name():
    name = None
    email = None
    form = NamForm();
    # Validation
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        form.name, form.email = '',''
        flash('Form submitted Successfully')
    return render_template('user.html', name=name,email= email, form=form)

@app.route('/name/add',methods=['GET','POST'])
def add_user():
    name = None
    form = NamForm();
    if form.validate_on_submit():
        user = Test.query.filter_by(email=form.email.data).first()
        if user is  None:
            # hashing password
            hashed_pw = generate_password_hash(form.password_hash.data, "sha256")
            user = Test(name=form.name.data, email=form.email.data, password_hash=hashed_pw)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        # email = form.email.data
        form.name.data  =''
        form.email.data = ''
        form.password_hash.data =''

        flash("User added Succesful")
    our_users = Test.query.order_by(Test.date_added)
    return render_template('add_user.html', form=form, name=name,our_users=our_users)


@app.route('/login', methods=['POST','GET'])
def Login():
    lform = LoginForm()
    email = None
    password = None
    # validation
    if lform.validate_on_submit():
        email = lform.email.data
        password = lform.password.data
        lform.email , lform.password = None, None
        flash("Login Succesful")
    # email = request.form.get('email')
    # password = request.form.get('password')
    print(email, password)
    # if request.args.get('email'):

    return render_template('login.html',email=email,password=password,form=lform)


@app.route('/register', methods=['POST','GET'])
def Register():
    rform = RegistrationForm()
    username = None
    email = None
    password = None
    confirm_password = None
    # validation
    if rform.validate_on_submit():
        username = rform.username.data
        email = rform.email.data
        password = rform.password.data
        confirm_password = rform.confirm_password.data
        rform.email ,rform.username , rform.password , rform.confirm_password = None, None, None,None
        flash("Login Succesful")
    print(username, email)

    return render_template('register.html',username=username, email=email,password=password,confirm_password=confirm_password,form=rform)

if __name__ == '__main__':
    app.debug = True
    app.run()