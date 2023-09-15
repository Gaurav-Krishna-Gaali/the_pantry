# E-commerce Web Application

This is an e-commerce web application built using Python and the Flask framework. It provides functionality for user registration, login, product browsing, adding products to a cart, placing orders, and managing admin access.

## Features

- User Registration: Users can create an account by providing their username, email, and password.
- User Login: Registered users can log in to their accounts using their credentials.
- Product Browsing: Users can browse through various product categories and view detailed information about each product.
- Cart Management: Users can add products to their cart, remove products from the cart, and view the contents of their cart.
- Order Placement: Users can place orders for the products in their cart, providing delivery address and payment details.
- Admin Access: Admin users have additional privileges to manage products, categories, and user accounts.

## Installation

1. Clone the repository: `git clone https://github.com/Gaurav-Krishna-Gaali/the_pantry`
2. Navigate to the project directory: `cd the_pantry`
3. Create a virtual environment: `python -m venv venv`
4. Activate the virtual environment:
   - For Windows: `venv\Scripts\activate`
   - For Unix/Linux: `source venv/bin/activate`
5. Install the required dependencies: `pip install -r requirements.txt`
6. Set up the database:
   - Modify the `SQLALCHEMY_DATABASE_URI` in `app.py` to your desired database connection string.
   - Run the database migrations: `flask db upgrade`
7. Start the application: `flask run`

## Usage

- Access the application in your web browser at `http://localhost:5000`.
- Register a new user account or log in with existing credentials.
- Browse through the available products, add them to your cart, and place orders.
- Admin users can access the admin panel at `http://localhost:5000/admin` to manage products, categories, and user accounts.

## License
This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).
