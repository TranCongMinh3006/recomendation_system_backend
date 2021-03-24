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

mycursor.execute("SELECT * FROM users")

myresult = mycursor.fetchall()

for x in myresult:
  id = x[0]
  user_name = str(id)
  password = str(id)
  name = x[3]
  sql = 'INSERT INTO auth_user (id, password, username,first_name,is_superuser,last_name,email,is_staff,is_active,date_joined) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
  val = (x[0], user_name,password,name,False,"last_name","email",True,True,datetime.now())
  mycursor.execute(sql, val)
  mydb.commit()
  print(val)