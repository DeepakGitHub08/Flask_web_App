from flask import Blueprint, render_template, request, flash,redirect, url_for,session
from werkzeug.security import generate_password_hash, check_password_hash
import MySQLdb.cursors
from . import mysql

auths = Blueprint('auths', __name__);

@auths.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        email  = request.form.get('email')
        password = request.form.get('password')
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE email = % s AND password = % s', (email, password ))
        user = cursor.fetchone()
        if user:
            session['loggedin'] = True
            session['id'] = user['id']
            session['username'] = user['first_name']
            if user['password'] == password:
                print(user)
                cursor.execute('SELECT * FROM notes WHERE user_id = %(user_id)s ',{'user_id': user['id'] })
                notes = cursor.fetchall()
                session['notes'] = notes
                print(notes)
                return redirect(url_for('views.home'))
            else :
                flash('Password or email is not correct', category='error')
        else:
            flash('User does not  exist', category='error')
    return render_template('login.html')    

@auths.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('first_name', None)
    session.pop('notes',None )
    return redirect(url_for('auths.login'))

@auths.route('/signup',  methods = ['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email');
        firstName = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        if len(email) < 4:
            flash('email should be greater than 4',category='error')
        elif len(firstName) < 2:
            flash('firstName is too short',category='error')
        elif password1 != password2:
            flash('passwords does not match ',category='error')
        elif len(password1) < 4:
            flash('password is too small',category='error')
        else:
            cursor.execute('SELECT * FROM user WHERE email = % s', (email, ))
            exist_user = cursor.fetchone()
            if exist_user:
                flash('Email Id already used in another account', category='error')
            else:
                cursor.execute('INSERT INTO user(email, password, first_name) VALUES (% s, % s, % s)', (email, password1, firstName))
                mysql.connection.commit()
                # login_user(new_user, remember=True)
                flash('Account created!', category='success')
                return redirect(url_for('views.home'))

    return render_template("signup.html")


