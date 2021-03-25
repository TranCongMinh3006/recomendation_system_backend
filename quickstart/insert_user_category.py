import mysql.connector
from datetime import datetime

mydb = mysql.connector.connect(
  host="127.0.0.1",
  user="root",
  password="123456",
  database="vnexpressdemo",
  auth_plugin='mysql_native_password'
)

mycursor = mydb.cursor()

mycursor.execute("SELECT * FROM category")

myresult = mycursor.fetchall()
id = 2
for x in myresult:
  categoryID = x[0]
  sql = 'INSERT INTO user_category (id,userID, categoryID) VALUES (%s,%s,%s)'
  val = (id,1, categoryID)
  id +=1
  mycursor.execute(sql, val)
  mydb.commit()
  print(val)