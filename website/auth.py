from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        messages = ""
        success = True
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user:
            messages += 'Please enter another non existent email address.  \n'
            success = False
            pass
        if len(email) < 4:
            messages += 'Please enter valid email address. \n'
            success = False
            pass
        if len(password) < 4:
            messages += 'Please enter valid password\n'
            success = False
            pass

        if success == True:
            new_user = User(email=email, name=name, password=generate_password_hash(
                password, method="sha256"))
            db.session.add(new_user)
            db.session.commit()
            flash("Account created !!!", category="success")
            return redirect(url_for('views.home'))
        else:
            flash(messages, category="error")

    return render_template('signup.html', user=current_user)


@auth.route('/signin',  methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user:
            if not check_password_hash(user.password, password):
                flash("Wrong password !!!", category="error")
            else:
                flash("Login successfully !!!", category="success")
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
        else:
            flash("User does not exist !!!", category="error")
    return render_template('signin.html', user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template('logout.html')
