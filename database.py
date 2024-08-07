import mysql.connector

def ConnectorMySQL():
    mydb = mysql.connector.connect(
        host="",
        user="",
        passwd="",
        database="",
        auth_plugin='mysql_native_password'
    )

    return mydb