from flask import Flask, render_template,url_for, request, flash,redirect
#import various components from the Flask framework
import mysql.connector
#import libary for interacting with MySQL database
import MySQLdb.cursors
#import module for executing SQL statements
from config import SECRET_KEY #for session managing

#initialize Flask web application __name__ for reference this python file name
app = Flask(__name__)

app.config['SECRET_KEY'] = SECRET_KEY

#establish a connection to MySQL database
connection = mysql.connector.connect(
    host="localhost",
    port="3306",
    user="root",
    password="",
    database="user_info",
    auth_plugin='mysql_native_password'
)

#create a cursor object to execute SQL query
db_cursor = connection.cursor(dictionary=True)

#define a route for the root URL
@app.route("/", methods=['GET', 'POST'])
def index():
    records = [] #initialize an empty list to store the retrieved data
    try:
        db_cursor = connection.cursor(MySQLdb.cursors.DictCursor) 
        #MySQL connector library use a object dictionary cursor for manage database
        db_cursor.execute("select * from person left join address on person.person_id = address.person_id")
        records=db_cursor.fetchall()

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    #return HTML page and pass the records to template
    return render_template('index.html',data=records)

@app.route("/info_form", methods=['GET','POST'])
def info_form():
    error_messages = [] #for store error messages
    if request.method == 'POST':
        print("test") #for debugging
        
        # request.form will request an item from inside [''] 
        # which it will retreive from a input field in html page that have matching name
        # and store in a variable that will to insert to the database
        
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        age = request.form['age']
        phone_number = request.form['phone_number']
        street = request.form['street']
        district = request.form['district']
        province = request.form['province']
        postal_code = request.form['postal_code']
        
        #basic error handling
        if not first_name:
            error_messages.append("First name is required")
        
        if age:
            try:
                age = int(age)
                if age < 0:
                    error_messages.append("Age must be non-negative")
            except ValueError:
                error_messages.append("Age must be a number")

        if postal_code: 
            try:
                postal_code = int(postal_code)
                if postal_code < 0:
                    error_messages.append("Postal code must be non-negative")
            except ValueError:
                error_messages.append("Postal code must be a number")
        
        if error_messages: 
            # this if statement for passing an error message with multiple error messages supported
            error_messages = ' , '.join(error_messages) 
            flash(error_messages)
            return render_template('info_form.html', errors=error_messages)

        #database connection
        db_cursor = connection.cursor(MySQLdb.cursors.DictCursor)
        db_cursor.execute("INSERT INTO person (first_name, last_name, age, phone_number) VALUES (%s, %s, %s, %s)",
                (first_name, last_name, age, phone_number,))
        
        person_id = db_cursor.lastrowid 
        #to provide person_id to address table to match the person_id that database auto generated

        db_cursor.execute("INSERT INTO address (person_id, street, district, province, postal_code) VALUES (%s, %s, %s, %s, %s)",
            (person_id, street, district, province, postal_code,))
        db_cursor.execute("""UPDATE person
            SET first_name = CONCAT(UCASE(SUBSTRING(first_name, 1, 1)), LOWER(SUBSTRING(first_name, 2)));""")
        db_cursor.execute("""UPDATE person
            SET last_name = CONCAT(UCASE(SUBSTRING(last_name, 1, 1)), LOWER(SUBSTRING(last_name, 2)));""")
                
        connection.commit() #commit the SQL query to the database

        flash('success') #pass message to the page 
        return redirect(url_for('index'))

    return render_template('info_form.html',)

#error handlers
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'),
#query specific user id
@app.route("/userinfo/<user_id>") #<user_id> will be capture from the URL
def userinfo(user_id):#user_id is passed from the URL above 
    db_cursor = connection.cursor(MySQLdb.cursors.DictCursor)
    query = " select * from person left join address on person.person_id = address.person_id where person.person_id = %s"
    db_cursor.execute(query, (user_id,))
    data =  db_cursor.fetchone()
    return render_template('userinfo.html', data = data)

@app.route("/edit/<user_id>", methods=['GET','POST'])
def edit(user_id):
    error_messages = []
    db_cursor = connection.cursor(MySQLdb.cursors.DictCursor)
    db_cursor.execute(" select * from person left join address on person.person_id = address.person_id where person.person_id = %s", (user_id,))
    data = db_cursor.fetchone()
    
    if request.method == 'POST':
        
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        age = request.form['age']
        phone_number = request.form['phone_number']
        street = request.form['street']
        district = request.form['district']
        province = request.form['province']
        postal_code = request.form['postal_code']

        if not first_name:
            error_messages.append("First name is required")
        
        if age:
            try:
                age = int(age)
                if age < 0:
                    error_messages.append("Age must be non-negative")
            except ValueError:
                error_messages.append("Age must be a number")
        
        if postal_code:
            try:
                postal_code = int(postal_code)
                if postal_code < 0:
                    error_messages.append("Postal code must be non-negative")
            except ValueError:
                error_messages.append("Postal code must be a number")
            
        if error_messages:
            error_messages = ' , '.join(error_messages) #for concatenate multiple error messages
            flash(error_messages)
            return render_template('edit.html',data=data, errors=error_messages)
        
        db_cursor.execute("UPDATE person SET first_name = %s, last_name = %s, age = %s, phone_number = %s WHERE person_id = %s",
                (first_name, last_name, age, phone_number,user_id,))
        db_cursor.execute("UPDATE address SET street = %s, district = %s, province = %s, postal_code = %s WHERE person_id = %s",
                (street, district, province, postal_code, user_id,))
        connection.commit()
        flash('success')
        return redirect(url_for('index'))
    

    return render_template('edit.html', data = data)

@app.route("/delete/<user_id>", methods=['GET', 'POST'])
def delete(user_id):
    db_cursor = connection.cursor(MySQLdb.cursors.DictCursor)
    query1 = "delete from address where person_id = %s"
    query2 = "delete from person where person_id = %s"
    db_cursor.execute(query1, (user_id,))
    db_cursor.execute(query2, (user_id,))
    connection.commit()
    flash('Successfully deleted')

    return redirect(url_for('index'))


@app.route("/search", methods=['GET','POST'])
def search():
    error_messages = []
    
    if request.method == 'POST':
        user_id = request.form['user_id']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        age = request.form['age']
        phone_number = request.form['phone_number']
        street = request.form['street']
        district = request.form['district']
        province = request.form['province']
        postal_code = request.form['postal_code']

        if age:
            try:
                age = int(age)
                if age < 0:
                    error_messages.append("Age must be non-negative")
            except ValueError:
                error_messages.append("Age must be a number")
        
        if postal_code:
            try:
                postal_code = int(postal_code)
                if postal_code < 0:
                    error_messages.append("Postal code must be non-negative")
            except ValueError:
                error_messages.append("Postal code must be a number")

        if user_id:
            try:
                user_id = int(user_id)
                if user_id < 0:
                    error_messages.append("User ID must be non-negative")
            except ValueError:
                error_messages.append("User ID code must be a number")
            
        if error_messages:
            error_messages = ' , '.join(error_messages)
            flash(error_messages)
            return render_template('search.html',errors=error_messages)

        db_cursor = connection.cursor(MySQLdb.cursors.DictCursor)
        db_cursor.execute("""
                    SELECT p.person_id, p.first_name, p.last_name,
                        p.age, p.phone_number, a.street, a.district, a.province, a.postal_code
                    FROM person p
                    JOIN address a ON p.person_id = a.person_id
                    WHERE p.person_id = %s
                        OR p.first_name = %s
                        OR p.last_name = %s
                        OR p.age = %s
                        OR p.phone_number = %s
                        OR a.street = %s
                        OR a.district = %s
                        OR a.province = %s
                        OR a.postal_code = %s 
                      """,
                    (user_id, first_name, last_name, age, phone_number,street,
                     district, province,postal_code,))
        data = db_cursor.fetchall()

        return render_template('search_result.html',data = data)

    return render_template('search.html')

if __name__ == '__main__':
    app.run(debug=True)
