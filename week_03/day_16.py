import sqlite3

conn = sqlite3.connect('test.db')
cursor = conn.cursor()

query = "INSERT INTO users(id, name) VALUES(104,'XYZ'),(102,'Ajay'),(103,'ABC');"
cursor.execute(query)
conn.commit()

print("Value inserted.")

query = "SELECT * FROM users;"
cursor.execute(query)
data = cursor.fetchall()
for row in data:
  print(*row)