from pprint import pprint
from flask import Flask, abort, render_template, request, flash, redirect, url_for
from forms import Addtocart, AdminForm, Cart_crud, ExForm, LoginForm, RegistrationForm, PasswordForm
from flask_login import UserMixin, login_user, login_required, logout_user, current_user, LoginManager
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin, AdminIndexView, expose
from flask_wtf.file import FileField
from flask import jsonify
from markupsafe import Markup
from flask_admin.contrib import sqla, rediscli
from flask_admin.contrib.fileadmin import FileAdmin
import os
# import os.path as op
from sqlalchemy.event import listens_for
from flask_admin import Admin, form
from wtforms import fields, widgets
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Secret Key
app.config['SECRET_KEY'] = "IITMadrasMAD1"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'

# init db
db = SQLAlchemy(app)
migrate = Migrate(app, db, render_as_batch=True)

class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    is_admin = db.Column(db.Boolean, default=False)
    wallet = db.Column(db.Integer, default= 1000)
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
    category_id = db.Column(db.Integer, db.ForeignKey(
        'category.id'), nullable=False)
    image = db.Column(db.String(255), nullable=True)
    # path = db.Column(db.BLOB, nullable=True)

    def __repr__(self):
        return f'<Products {self.name}>'

    def __str__(self):
        return self.name

# Categories model
class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    image = db.Column(db.String(255), nullable=True)
    products = db.relationship('Products', backref='category', lazy='dynamic')

    def __repr__(self):
        return f'<Category {self.name}>'

    def __str__(self):
        return self.name

# Model for cart
class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey(
        'products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    product = db.relationship('Products', backref='cart_items')
    user = db.relationship('Users', backref='cart_items')

# Model for Orders
class Orders(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    order_date = db.Column(db.DateTime, default=datetime.utcnow)
    total_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.Boolean, default=False)
    delivery_address = db.Column(db.Text, nullable=False)

    user = db.relationship('Users', backref='orders')

    def __repr__(self):
        return f'<Orders {self.id}>'

# Model for Order Items
class OrderItem(db.Model):
    __tablename__ = 'order_items'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    # Define relationships
    order = db.relationship('Orders', backref=db.backref('order_items', lazy='dynamic'))
    product = db.relationship('Products')

    def __repr__(self):
        return f'<OrderItem {self.id}>'

# Flask Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'Login'


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


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
    column_display_pk = True
    column_list = ('id', 'user_id', 'product_id', 'quantity')
    form_columns = ('id', 'user_id', 'product_id', 'quantity')

class ProductModelView(ModelView):
    column_display_pk = True
    column_list = ('id', 'name', 'description', 'price', 'quantity', 'category_id', 'image')
    form_columns = ( 'name', 'description', 'price', 'quantity', 'category_id', 'image')
    form_args = {
        'category': {
            'query_factory': lambda: Category.query.all()
        }
    }

class OrderItemsModelController(ModelView):
    column_list = ('id', 'order_id', 'product_id', 'quantity')
    form_columns = ('id', 'order_id', 'product_id', 'quantity')

class MyAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        if current_user.is_admin == True:
            return super(MyAdminIndexView, self).index()
        next_url = request.endpoint
        login_url = "%s?next=%s" % (url_for('admin_login'), next_url)
        return redirect(login_url)

class OrderItemController(ModelView):
    column_display_pk = True
    column_list = ('id','user_id','order_date','total_amount','status','delivery_address')
    form_columns = ('user_id','order_date','total_amount','status','delivery_address')

admin = Admin(app, name="The Pantry Control Panel", template_mode='bootstrap4',
              index_view=MyAdminIndexView()
              )
admin.add_view(Controller(Users, db.session))
admin.add_view(ProductModelView(Products, db.session))
admin.add_view(Controller(Category, db.session))
admin.add_view(CartItemController(CartItem, db.session))
admin.add_view(OrderItemsModelController(OrderItem, db.session))
admin.add_view(OrderItemController(Orders, db.session))

path = os.path.join(os.path.dirname(__file__), 'static/img')
admin.add_view(FileAdmin(path, '/static/img/', name='Static Files'))


@app.route('/admin-login', methods=['GET', 'POST'])
def admin_login():
    logout_user()
    aform = AdminForm()
    flash("You do not have Admin acces. Please login in if you have admin credentials.")
    # Admin Validation
    if aform.validate_on_submit():
        user = Users.query.filter_by(email=aform.email.data).first()
        if user:
            if check_password_hash(user.password_hash, aform.password.data):
                if user.is_admin == True:
                    login_user(user)
                # flash("Login Succesfull!!")
                return redirect(url_for('index'))
            else:
                flash("You do not have admin acess!! ")
        else:
            flash("Wrong Credentials - Try Again!")
    return render_template('admin_login.html', form=aform)


# cart management function
def cart_items_costs():
    user_id = current_user.id
    print(user_id)
    cart_items_with_products = db.session.query(CartItem, Products)\
        .join(Products, CartItem.product_id == Products.id)\
        .filter(CartItem.user_id == user_id)\
        .all()
    products_in_cart = []
    for cart_item, product in cart_items_with_products:
        pprint(vars(product))
        pprint(vars(cart_item))
        cart_item_data = {
            'product_id': product.id,
            'product_name': product.name,
            'product_desc': product.description,
            'product_price': product.price,
            'quantity': cart_item.quantity,
            'product_category_id': product.category_id,
            'product_image': product.image,
            'subtotal': product.price * cart_item.quantity
        }
        # cart_product['quantity'] = quantity
        products_in_cart.append(cart_item_data)
    print(products_in_cart)
    return products_in_cart


def cart_items_total(cart):
    _total = 0
    for item in cart:
        _total += item['subtotal']
    print(_total)
    return _total


# example
@app.route('/ex', methods=['GET', 'POST'])
def ex():
    username = None
    user = None
    exform = RegistrationForm()
    if exform.validate_on_submit():
        user = Users.query.filter_by(email=exform.email.data).first()
        if user is None:
            # hashing password
            hashed_pw = generate_password_hash(
                exform.password_hash.data, "sha256")
            user = Users(username=exform.username.data,
                         email=exform.email.data, password_hash=hashed_pw)
            db.session.add(user)
            db.session.commit()
        username = exform.username.data
        exform.username.data = ''
        exform.email.data = ''
        exform.password_hash.data = ''

    return upcoming_orders, delivered_orders
    return upcoming_orders, delivered_orders


def remove_from_cart(item_id):
    # _code = request.form['code']
    # cart_item = CartItem.query.get_or_404(item_id)
    item_in_cart = CartItem.query.filter_by(
        user_id=current_user.id, product_id=item_id).all()
    print(item_in_cart)

    # Check if the cart item belongs to the current user
    if item_in_cart.user_id == current_user.id:
        db.session.delete(item_in_cart)
        db.session.commit()
    return "done"

def Myorders():
    upcoming_orders = []
    delivered_orders = []
    order_data = db.session.query(Orders, OrderItem, Products)\
    .join(OrderItem, Orders.id == OrderItem.order_id)\
    .join(Products, OrderItem.product_id == Products.id)\
    .filter(Orders.user_id == current_user.id)\
    .all()
    print(order_data)

    for order, order_item, product in order_data:
    # Access the data from each table
        order_id = order.id
        order_date = order.order_date
        total_amount = order.total_amount
        status = order.status
        delivery_address = order.delivery_address

        order_item_id = order_item.id
        quantity = order_item.quantity

        product_id = product.id
        product_name = product.name
        product_description = product.description
        product_price = product.price

        order_object = {
            "order_id": order_id,
            "order_date": order_date,
            "total_amount": total_amount,
            "status": status,
            "delivery_address": delivery_address,
            "order_item_id": order_item_id,
            "quantity": quantity,
            "product_id": product_id,
            "product_name": product_name,
            "product_description": product_description,
            "product_price": product_price
        }

        if status == False:
            upcoming_orders.append(order_object)
        else:
            delivered_orders.append(order_object)
    return upcoming_orders, delivered_orders
def get_common_data():
    upcoming, delivered = Myorders()
    addtocart = Addtocart()
    order = Cart_crud()
    user = None
    allproducts = Products.query.all()
    categories = Category.query.all()
    products_in_cart = cart_items_costs()
    products_total = cart_items_total(products_in_cart)
    print(products_in_cart)
    sum_products = len(products_in_cart)

    if current_user.is_authenticated:
        user = current_user
    print(user.id)
    remove_items = None
    return upcoming, delivered, addtocart, order, user, allproducts, categories, products_in_cart, products_total, sum_products, remove_items

@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    upcoming, delivered, addtocart, order, user, allproducts, categories, products_in_cart, products_total, sum_products, remove_items = get_common_data()

    display_prod = True
    categories_flag = False
    return render_template('base.html', user=user, upcoming = upcoming, delivered = delivered, order=order, categories=categories , categories_flag=categories_flag, sum_products = sum_products, display_prod=display_prod, products_total=products_total, cart_products=products_in_cart, form=addtocart, allproducts=allproducts, remove_items=remove_items)

@app.route('/search', methods=['GET', 'POST'])
def search():
    upcoming, delivered, addtocart, order, user, allproducts, categories, products_in_cart, products_total, sum_products, remove_items = get_common_data()

    q = request.form.get('query')  # Get the search query from the form data
    print(q)

    # results = Products.query.filter(Products.name.icontains(q)).all() | 1
    # print(results)
    print(q)
    allproducts = Products.query.filter(Products.name.ilike(f'%{q}%')).all()
    categories = Category.query.filter(Category.name.ilike(f'%{q}%')).all()
    display_prod = True
    categories_flag = False
    search_flag = True
    return render_template('search.html', allproducts=allproducts, q=q,user=user, upcoming = upcoming, delivered = delivered, order=order, categories=categories , categories_flag=categories_flag, sum_products = sum_products, display_prod=display_prod, products_total=products_total, cart_products=products_in_cart, form=addtocart, remove_items=remove_items )

@app.route('/add', methods=['POST'])
@login_required
def add_product_to_cart():
    try:
        _quantity = int(request.form['quantity'])
        _code = request.form['code']
        print(f"Quantity: {_quantity}, Code: {_code}")

        if _quantity and _code and request.method == 'POST':
            product = Products.query.get_or_404(_code)
            print(f"Product: {product}")

            item_in_cart = CartItem.query.filter_by(
                user_id=current_user.id, product_id=_code).first()
            print(f"Item in Cart: {item_in_cart}")

            if item_in_cart:
                item_in_cart.quantity += _quantity
            else:
                new_cart_item = CartItem(
                    user_id=current_user.id, product_id=_code, quantity=_quantity)
                db.session.add(new_cart_item)

            if _quantity > product.quantity:
                print("Insufficent quantity")
                flash('Insufficient inventory!', 'error')
                return redirect(url_for('index'))

            db.session.commit()
            flash('Item added to cart successfully!', 'success')
            return redirect(url_for('index'))
        else:
            return "Error while adding item to cart"

    except Exception as e:
        print(f"Exception: {e}")
        # return redirect(url_for('index'))
        return add_product_to_cart

@app.route('/remove_from_cart/<int:item_id>', methods=['POST'])
@login_required
def remove_from_cart(item_id):
    # user_id = current_user.id
    item_in_cart = CartItem.query.filter_by(
        user_id=current_user.id, product_id=item_id).all()
    cart_items_to_delete = []

    # Add cart items to the list
    for cart_item in item_in_cart:
        cart_items_to_delete.append(cart_item)

    print(item_in_cart)
    dir(item_in_cart)
    # if item_in_cart.user_id == current_user.id:
    cart_items_to_delete = []
    for cart_item in item_in_cart:
        cart_items_to_delete.append(cart_item)

    for cart_item in cart_items_to_delete:
        db.session.delete(cart_item)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/Checkout', methods=['POST', 'GET'])
@login_required
def Checkout():
    # wallet balance
    user = Users.query.get(current_user.id)
    wallet = user.wallet
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    total_amount = sum(cart_item.product.price * cart_item.quantity for cart_item in cart_items)
    if wallet >= total_amount:
        wallet -= total_amount
        user.wallet = wallet
        db.session.commit()

        if cart_items:
            order = Orders(
                user_id=current_user.id,
                total_amount=total_amount,
                status=False, 
                # delivery_address=current_user.address  # You can set the delivery address as needed
                delivery_address='home'# You can set the delivery address as needed
            )
            db.session.add(order)
            db.session.commit()

            for cart_item in cart_items:
                order_item = OrderItem(
                    order_id=order.id,  
                    product_id=cart_item.product_id,
                    quantity=cart_item.quantity
                )
                db.session.add(order_item)
                db.session.commit()
                
                # reducing inventory
                product = Products.query.get(cart_item.product_id)
                product.quantity -= cart_item.quantity
                db.session.commit()

            # Clear the cart after placing the order
            CartItem.query.filter_by(user_id=current_user.id).delete()
            db.session.commit()

            flash('Order placed successfully!', 'success')
        else:
            flash('Your cart is empty.', 'info')

    else:
        flash('No Sufficient balance')
    return redirect(url_for('index'))


@app.route('/Users_pwd', methods=['GET', 'POST'])
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
        form.password, form.email = '', ''

        pw_to_check = Users.query.filter_by(email=email).first()
        # check hashed password
        passed = check_password_hash(pw_to_check.password_hash, password)

    return render_template('user.html', password=password, email=email, pw_to_check=pw_to_check, form=form, passed=passed)


@app.route('/category/<int:category_id>', methods=['GET', 'POST'])
@login_required
def category_route(category_id):
    category = Category.query.get(category_id)
    products = Products.query.filter_by(category_id=category_id).all()
    print(category.image)

    upcoming, delivered, addtocart, order, user, allproducts, categories, products_in_cart, products_total, sum_products, remove_items = get_common_data()

    display_prod = False
    categories_flag = True
    return render_template("cat.html", category=category, allproducts=allproducts,user=user, upcoming = upcoming, categories_flag = categories_flag, delivered = delivered, order=order , sum_products = sum_products, display_prod=display_prod, products_total=products_total, cart_products=products_in_cart, form=addtocart, products=products, remove_items=remove_items)

@app.route('/register', methods=['GET', 'POST'])
def add_user():
    username = None
    user = None
    form = RegistrationForm()

    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            # hashing password
            hashed_pw = generate_password_hash(
                form.password_hash.data, "sha256")
            user = Users(username=form.username.data,
                         email=form.email.data, password_hash=hashed_pw)
            db.session.add(user)
            db.session.commit()
        username = form.username.data
        form.username.data = ''
        form.email.data = ''
        form.password_hash.data = ''

        flash("User added Succesful")
    # our_users = Users.query.order_by(Users.date_added)
    return render_template('add_user.html', form=form, username=username, user=user)


@app.route('/login', methods=['POST', 'GET'])
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

    return render_template('login.html', form=lform)

# Logout page
@app.route('/logout', methods=['POST', 'GET'])
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
    # app.run(debug=True, host = 'localhost' , port = '8080')
