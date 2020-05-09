from flask import render_template, url_for, flash, redirect, request
from twatter import app, db, bcrypt
from twatter.models import User, Post
from twatter.forms import RegistrationForm, LoginForm
from flask_login import login_user, current_user, logout_user, login_required

posts = [
    {
        "author": "Ken",
        "title": "Random Preach",
        "text": "The world is a dangerous place",
        "date_posted": 'April 20, 2015'
    },
    {
        "author": "Ken",
        "title": "More Preach",
        "text": "The world is a dangerous place",
        "date_posted": 'March 14, 2016'
    }
]


@app.route("/")
@app.route("/home")
def home_page():
    return render_template('home.html', posts=posts)


@app.route("/about")
def about_page():
    return render_template('about.html')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home_page'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data,
                    email=form.email.data,
                    password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}, you are now able to log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title="Register", form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home_page'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            if next_page: # Is True if our previous screen was not home_page
                return redirect(url_for(next_page))
            return redirect(url_for('home_page'))
        else:
            flash('Login unsuccesful, please check username and passowrd', 'danger')
    return render_template('login.html', title="Login", form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home_page'))

@app.route("/account")
@login_required
def account():
    return render_template('account.html', title="Account")
