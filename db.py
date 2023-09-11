import sqlite3 as sql

def add_data(id, name, description, price, quantity, category_id, image):  
# def add_data( ):  
  try:
    # Connecting to database
    con = sql.connect('instance\\data.db')
    print("Connected to the database")
    # Getting cursor
    c =  con.cursor() 
    # Adding data
    c.execute("INSERT INTO Products (id, name, description, price, quantity, category_id, image ) VALUES (?, ?, ?, ?, ?, ?, ?)", (id, name, description, price, quantity, category_id, image ))

    # Applying changes
    con.commit() 
  except :
    print("An error has occured")

# add_data(1,"Banana", "Banana it is ", 30, 10, 1, "static/img/Banana_Iconic.jpg")
add_data(2, "Apple", "Fresh red apple", 20, 10, 1, "images/img/apple.jpg")
# add_data();

# products = [
#     {
#         'name': 'Apple',
#         'description': 'Fresh red apple',
#         'price': 1.99,
#         'category_id': 1,
#         'image': 'images/apple.jpg',
#     },
#     {
#         'name': 'Banana',
#         'description': 'Yellow banana',
#         'price': 0.99,
#         'category_id': 1,
#         'image': 'images/banana.jpg',
#     },
#     {
#         'name': 'Orange',
#         'description': 'Juicy orange',
#         'price': 1.49,
#         'category_id': 1,
#         'image': 'images/orange.jpg',
#     },
#     {
#         'name': 'Milk',
#         'description': 'Fresh milk',
#         'price': 2.49,
#         'category_id': 2,
#         'image': 'images/milk.jpg',
#     },
#     {
#         'name': 'Bread',
#         'description': 'Whole wheat bread',
#         'price': 3.99,
#         'category_id': 2,
#         'image': 'images/bread.jpg',
#     },
#     # Add more dummy products as needed
# ]



