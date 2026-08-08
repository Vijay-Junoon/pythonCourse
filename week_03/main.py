import sqlite3

conn = sqlite3.connect('facebook.db')
cursor = conn.cursor()

def createTable():

  query = 'CREATE TABLE IF NOT EXISTS users(username VARCHAR(50), mail VARCAHR(50), password VARCHAR(15), follows INTEGER, following INTEGER)'
  cursor.execute(query)
  print("Create Table - Users -")

def adminDisplay():

  query = "SELECT * FROM users;"
  cursor.execute(query)
  users = cursor.fetchall()

  for user in users:
    print(*user)

def login():
  # Input from user
  username = input("Enter username: ") 
  mail = input("Enter mail: ")
  password = input("Enter password: ")

  # Collecting details using the username
  query = "SELECT * FROM users WHERE username = ?;"
  cursor.execute(query,(username,))

  # Transferring that data to user_details
  user_details = cursor.fetchone()

  # The user doesn't exist: 
  if not user_details:
    print("No such user exists.")
    return

  # correct mail_id,correct password
  correct_mail = user_details[1]
  correct_pwd = user_details[2]

  # Comparison
  if mail == correct_mail:

    if password == correct_pwd:
      print("Login done. Welcome back.")
    else:
      print("Incorrect password.")
  else:
    print("Incorrect mail.")

def register():

  username = input("Enter username: ")
  mail = input("Enter mail: ")
  password = input("Enter password: ")

  query = "INSERT INTO users(username, mail, password, follows, following) VALUES(?,?,?,0,0);"
  cursor.execute(query,(username,mail,password))
  conn.commit()

  print("Registration completed. Welcome to facebook.")

choice = 0
while choice != 4:
  choice = int(input("Select choice: \n 1)Login 2)Register 3)Admin 4)Exit. Make your choice: "))
  if choice == 1:
    login()
  elif choice == 2:
    register()
  elif choice == 3:
    adminDisplay()

