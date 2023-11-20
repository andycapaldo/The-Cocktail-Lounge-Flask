import requests
from app import app
from flask import render_template, redirect, url_for, flash
from app.forms import SignUpForm


@app.route('/')
def index():
    cocktail_res = requests.get('https://www.thecocktaildb.com/api/json/v1/1/search.php?f=a')
    data = cocktail_res.json()['drinks']
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

        
    return render_template('signup.html', form=form)