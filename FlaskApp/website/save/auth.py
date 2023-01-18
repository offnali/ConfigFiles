from flask import Blueprint, render_template, request, flash, session, redirect, url_for
from flask_login import current_user
from mysql.connector import connect, Error
import mariadb

auth = Blueprint('auth', __name__)

user = "CorendonVluchtBeheer"
password = "CftE25513j86"
host = "localhost"
database = "fys"

def create_connection(user, password, host, database):
    conn = mariadb.connect(user=user, password=password, host=host, database=database)
    return conn

# Create a connection to the database
conn = create_connection(user, password, host, database)

@auth.route('/home')
def home():
    return render_template("home.html")

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # get the seatnumber and lastname from the form in login.html
        seatnumber = request.form['seatnumber']
        lastname = request.form['lastname']

        # create a connection to the MariaDB database

        # execute a SELECT query to retrieve the user from the database
        cursor = conn.cursor()
        sql = ''' SELECT * FROM login_credentials WHERE seat_number = %s AND last_name = %s '''
        val = (seatnumber, lastname)
        cursor.execute(sql, val)
        user = cursor.fetchone()

        # close the connection
        cursor.close()
        conn.close()

        # check if the user exists
        if user is True:
            # login succesful,, redirect to the homepage
            # session['logged_in'] = True
            return redirect(url_for("auth.home"))
        else:
            # login failed, render the login template with an error message
            return redirect("login.html")
    else:
        # render the login template
        return render_template("login.html")

@auth.route('/multimedia')
def multimedia():
    return render_template("multimedia.html")

@auth.route('/contacts')
def contacts():
    return render_template("contacts.html")

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if len(email) < 4:
            flash('email must be greater than 3 characters.', category='error')
        elif len(firstName) < 2:
            flash('First name must be greater than 1 characters.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match', category='success')
        elif len(password1) < 7:
            flash('Password must be atleast 7 characters.', category='error')
        else:
            #add user to database
            flash('account created!', category='succes')


    return render_template("sign_up.html")

@auth.route('/logout')
def logout():
    session.pop("logged_in", True)
    return redirect(url_for('views.home'))

