**<h1>CRUD APP</h1>**

This is a basic CRUD app created for my personal learning to practice fundamental programming concepts and understand database interactions.

This Flask website application is a super basic CRUD (Create, Read, Update, Delete) system designed for my personal full-stack development learning. It offers an interface for users to input edit search and delete personal information including name, age, phone number, and address.

**<h2>Tech stack</h2>**

- XAMPP 
- Python 3.12

**<h2>Import the database</h2>**

Open XAMPP

- start both Apache and MySQL server
- go into URL "http://localhost/phpmyadmin/"
- click import in dropdown menu
- choose "user_info.sql" inside database folder

**<h2>Create virtual environment</h2>**

change directory to this project folder

    cd path

Install a virtual environment

    pip install virtualenv

create virtual environment

    python -m venv env

activate virtual environment

    source env/bin/activate

**<h2>Install dependencies</h2>**

flask

    pip install flask

MySQL connector

    pip install mysql-connector-python

Run application

    python app.py

