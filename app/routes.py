import requests
from app import app, db
from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.forms import SignUpForm, LoginForm
from app.models import User


@app.route('/')
def index():
    response = requests.get(f'https://www.thecocktaildb.com/api/json/v2/9973533/filter.php?a=Alcoholic')
    data = response.json()['drinks']
    return render_template('index.html', data=data)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        first_name = form.first_name.data
        last_name = form.last_name.data
        username = form.username.data
        email = form.email.data
        password = form.password.data

        check_user = db.session.execute(db.select(User).where( (User.username==username) | (User.email==email) )).scalars().all()
        if check_user:
            flash('A user with that username and/or email already exists')
            return redirect(url_for('signup'))
        
        new_user = User(first_name=first_name, last_name=last_name, username=username, email=email, password=password)

        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)

        flash(f"{new_user.username} has been created.")

        return redirect(url_for('index'))
    return render_template('signup.html', form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remember_me = form.remember_me.data

        user = db.session.execute(db.select(User).where(User.username==username)).scalar()

        if user is not None and user.check_password(password):
            login_user(user, remember=remember_me)
            flash(f"{user.username} has successfully logged in.")
            return redirect(url_for('index'))
        else:
            flash('Incorrect username and/or password')
            return redirect(url_for('login'))
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    flash('You have successfully logged out')
    return redirect(url_for('index'))

@app.route('/alldrinks')
def alldrinks():
    response = requests.get('https://www.thecocktaildb.com/api/json/v2/9973533/filter.php?a=Alcoholic')
    data = response.json()['drinks']
    return render_template('alldrinks.html', data=data)



@app.route('/cocktails/<drink_id>')
def cocktail_view(drink_id):
    response = requests.get(f'https://www.thecocktaildb.com/api/json/v2/9973533/lookup.php?i={drink_id}')
    data = response.json()['drinks']
    return render_template('cocktail.html', data=data)
