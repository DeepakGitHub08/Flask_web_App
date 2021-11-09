from flask import Blueprint, render_template, request, flash,redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from . import db 
from .model import User, Notes
from flask_login import login_user, login_required, logout_user, current_user

auths = Blueprint('auths', __name__);

@auths.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        email  = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email = email).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else :
                flash('Password or email is not correct', category='error')
        else:
            flash('User does not  exist', category='error')
    return render_template('login.html', user = current_user)    

@auths.route('/logout')
@login_required
def logout():
        logout_user()
        return redirect(url_for('auths.login'))

@auths.route('/signup',  methods = ['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email');
        firstName = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if len(email) < 4:
            flash('email should be greater than 4',category='error')
        elif len(firstName) < 2:
            flash('firstName is too short',category='error')
        elif password1 != password2:
            flash('passwords does not match ',category='error')
        elif len(password1) < 4:
            flash('password is too small',category='error')
        else:
            exist_user = User.query.filter_by(email = email).first()
            if exist_user:
                flash('Email Id already used in another account', category='error')
            else:
                new_user  = User(email = email,first_name = firstName, password=generate_password_hash(
                password1, method='sha256'))
                db.session.add(new_user)
                db.session.commit()
                login_user(new_user, remember=True)
                flash('Account created!', category='success')
                return redirect(url_for('views.home'))

    return render_template("signup.html", user = current_user)


