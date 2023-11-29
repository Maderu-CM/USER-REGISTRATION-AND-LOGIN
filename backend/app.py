from flask import Flask,render_template,request, flash
import psycopg2
import psycopg2.extras
import re
from werkzeug.security import generate_password_hash

app= Flask(__name__)
app.secret_key= 'clivemoyia-maderu'

DB_HOST = 'localhost'
DB_NAME = 'postgres'
DB_USER = 'postgres'
DB_PASS = 'AZiza@2812'

conn = psycopg2.connect(dbname=DB_NAME,user=DB_USER, password=DB_PASS,host=DB_HOST)


@app.route('/register', methods= ['GET','POST'])
def register() :

    cursor= conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    #checking if the neccessary fields exist
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        fullname = request.form['fullname']
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        _hashed_password= generate_password_hash(password)

        #check if the user already exists
        cursor.execute('SELECT *FROM employee WHERE username =%s', {username,})
        account = cursor.fetchone()
        print(account)


        #if account exists show the error and validation checks
        if account:
            flash('Account already exists!')
        elif not re.match(r'[^@]+@[^@]+\.[^@]+',email):
            flash(' Invalid email address')
        elif not re.match(r'[A-Za-z0-9]+',username):
            flash(' Username must conatin only characters and numbers!')
        elif not username or not password or not email:
            flash('Please fill out the form!')
        else:
            #Account does not exist with valid form data insert into account
            cursor.execute("INSERT INTO users(fullname, username, password, email) VALUES (%s,%s,%s,%s)",(fullname, username, _hashed_password, email))
            conn.commit()
            flash('You have successfully registered!')
    elif request.method == 'POST':
        #Form is empty
        flash('Please fill out the form!')

    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)