import mysql.connector

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="user_info",
    auth_plugin='mysql_native_password'
)

db_cursor = connection.cursor()

selectquery= 'select * from person'

db_cursor.execute(selectquery)
records=db_cursor.fetchall()

for row in records:
    print("user id",row[0])
    print("first name",row[1])
    print("last name",row[2])
    print("")

db_cursor.close()
connection.close()
