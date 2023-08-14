from flask import Flask, abort, render_template, request, flash, redirect,url_for
from forms import Addtocart, AdminForm, ExForm, LoginForm, RegistrationForm,PasswordForm
from flask_login import UserMixin, login_user, login_required, logout_user, current_user, LoginManager
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin, AdminIndexView, expose
from flask_wtf.file import FileField


app = Flask(__name__    )

# Secret Key
app.config['SECRET_KEY'] = "IITMadrasMAD1"
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///data.db'

# init db
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# admin = Admin(app, name="The pantry Control Panel")
# Dummy data for Product model
# products = {  id: 1, name : "Banana", description: "Banana it is ", price: 30, category_id:  1, image: "static/img/Banana_Iconic.jpg"}

# DB Model for Users name
class Users(db.Model, UserMixin):
    id  = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200),nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    is_admin = db.Column(db.Boolean, default=False)
    profile_pic = FileField("Profile Pic")
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
    quantity = db.Column(db.Integer)
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
    
# Model for cart
class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)

    product = db.relationship('Products', backref='cart_items')
    user = db.relationship('Users', backref='cart_items')

    
# Flask Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'Login'

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


# @app.before_request
# def before_req():
#     user = current_user

class Controller(ModelView):
    column_display_pk = True
    column_hide_backrefs = False
    # column_list = ('id')
    def is_accessible(self):
        if current_user.is_admin == True:
            return current_user.is_authenticated
        else:
            if current_user.is_admin == True:
                return redirect(url_for('create_admin'))
        
    def not_auth(self):
        return "You do not have admin access!!"
    

class CartItemController(Controller):
    column_list =  ('id', 'user_id', 'product_id', 'quantity')
class MyAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        if current_user.is_admin == True:
            return super(MyAdminIndexView,self).index()
        next_url = request.endpoint
        login_url = "%s?next=%s" % (url_for('admin_login'), next_url)
        return redirect(login_url)


admin = Admin(app, name="The Pantry Control Panel", index_view=MyAdminIndexView())
admin.add_view(Controller(Users, db.session))
admin.add_view(Controller(Products, db.session))
admin.add_view(Controller(Category, db.session))
admin.add_view(CartItemController(CartItem, db.session))

# @app.route('/admin', methods=['GET','POST'])
# @login_required
# def admin():
#     # if current_user.is_admin == True:
#         return "Hi"

@app.route('/admin-login', methods=['GET','POST'])
def admin_login():
    logout_user()
    aform = AdminForm()
    flash("You do not have Admin acces. Please login in if you have admin credentials.")
    # Admin Validation
    if aform.validate_on_submit():
        user = Users.query.filter_by(email=aform.email.data).first()
        if user :
            if check_password_hash(user.password_hash, aform.password.data):
                if user.is_admin == True:
                    login_user(user)
                # flash("Login Succesfull!!")
                return redirect(url_for('index'))
            else:
                flash("You do not have admin acess!! ")
        else:
            flash("Wrong Credentials - Try Again!")
    return render_template('admin_login.html', form =aform)


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

# cart management function
def cart_items_costs():
    user_id = current_user.id
    cart_items_with_products = db.session.query(CartItem, Products)\
    .join(Products, CartItem.product_id == Products.id)\
    .filter(CartItem.user_id == user_id)\
    .all()
    products_in_cart = []
    for cart_item, product in cart_items_with_products:
        # pprint(vars(product))
        # pprint(vars(cart_item))
        cart_item_data = {
            'product_id': product.id,
            'product_name': product.name,
            'product_desc': product.description,
            'product_price': product.price,
            'quantity': cart_item.quantity,
            'product_category_id': product.category_id,
            'product_image':product.image,
            'subtotal': product.price * cart_item.quantity
        }
        # cart_product['quantity'] = quantity
        products_in_cart.append(cart_item_data)
    print(products_in_cart)
    return products_in_cart
    
# example
@app.route('/ex', methods=['GET','POST'])
def ex():
    username = None
    user = None
    exform = RegistrationForm()
    if exform.validate_on_submit():
        user = Users.query.filter_by(email=exform.email.data).first()
        if user is  None:
            # hashing password
            hashed_pw = generate_password_hash(exform.password_hash.data, "sha256")
            user = Users(username=exform.username.data, email=exform.email.data, password_hash=hashed_pw)
            db.session.add(user)
            db.session.commit()
        username = exform.username.data
        exform.username.data  =''
        exform.email.data = ''
        exform.password_hash.data =''

        flash("User added Succesful")
    exform = ExForm()
    display_prod = False
    return render_template('ex.html', display_prod=display_prod, form = exform,username=username,user=user)

@app.route('/', methods=['GET','POST'])
@login_required
def index():
    addtocart = Addtocart()
    user = None
    products = Products.query.all()

    products_in_cart = cart_items_costs()

    # for cart_item, product in cart_items_with_products:
    #  print(f"Product: {product.name}, Quantity: {cart_item.quantity}")

    if current_user.is_authenticated:
        user = current_user

    cart_modal = False
    remove_items = None
    display_prod = True
    return render_template('base.html', cart_modal = cart_modal,user=user,display_prod=display_prod, cart_products=products_in_cart, form = addtocart, products=products, remove_items=remove_items )

@app.route('/add', methods=['POST'])
@login_required
def add_product_to_cart():
    cart_modal = True
    try:
        _quantity = int(request.form['quantity'])
        _code = request.form['code']
        # vaidation
        if _quantity and _code and  request.method == 'POST':
            product = Products.query.get_or_404(_code)
            # quantity = int(request.form.get('quantity'))
            item_in_cart = CartItem.query.filter_by(user_id=current_user.id, product_id=_code).first()

            if item_in_cart:
                item_in_cart.quantity += _quantity
            else:
                new_cart_item = CartItem(user_id=current_user.id, product_id=_code, quantity=_quantity)
                db.session.add(new_cart_item)

            db.session.commit()
            flash('Item added to cart successfully!', 'success')
            return redirect(url_for('index'))
        else:
            return "Error while adding item to cart"
    
    except Exception as e:
        print (e)
    finally:
        pass
        # cursor.close()
        # conn.close()
    
@app.route('/cart', methods=['GET','POST'])
@login_required
def cart():
#     user = None
#     if current_user.is_authenticated:
#         user = current_user
    return render_template('Cart.html')

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