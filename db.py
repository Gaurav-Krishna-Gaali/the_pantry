import sqlite3 as sql

# def add_data(id, name, description, price, category_id, image ):  
def add_data( ):  
  try:
    # Connecting to database
    con = sql.connect('instance\data.db')
    print("Connected to the database")
    # Getting cursor
    c =  con.cursor() 
    # Adding data
    # c.execute("INSERT INTO Products (id, name, description, price, category_id, image ) VALUES (%s, %s,%s, %s,%s, %s)" %(id, name, description, price, category_id, image ))
    # c.execute("""INSERT INTO Products VALUES(1, "Banana", "Banana it is ", 30, 1, "static/img/Banana_Iconic.jpg");""")
    c.execute("""INSERT INTO Products VALUES(2, "Apple", "Fresh red apple ", 40, 1, "static/img/apple.jpg");""")
    # c.execute("""INSERT INTO Products VALUES(3, "Orange", "Juicy orange fruit", 35, 1, "static/img/orange.jpg");""")
    # c.execute("""INSERT INTO Products VALUES(4, "Watermelon", "Sweet and refreshing watermelon", 60, 1, "static/img/watermelon.jpg");""")
    # c.execute("""INSERT INTO Products VALUES(5, "Mango", "Sweet and ripe mango", 65, 1, "static/img/mango.jpg");""")
    # c.execute("""INSERT INTO Products VALUES(6, "Strawberry", "Juicy red strawberry", 55, 1, "static/img/strawberry.jpg");""")
    # c.execute("""INSERT INTO Products VALUES(7, "Pineapple", "Tropical pineapple fruit", 45, 1, "static/img/pineapple.jpg");""")
    # c.execute("""INSERT INTO Products VALUES(8, "Grapes", "Fresh bunch of grapes", 50, 1, "static/img/grapes.jpg");""")

    # Applying changes
    con.commit() 
  except:
    print("An error has occured")

# add_data(1,"Banana", "Banana it is ", 30, 1, "static/img/Banana_Iconic.jpg")
add_data();

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
