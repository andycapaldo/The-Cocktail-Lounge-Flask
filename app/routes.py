import requests
from app import app
from flask import render_template, redirect, url_for, flash


@app.route('/')
def index():
    cocktail_res = requests.get('https://www.thecocktaildb.com/api/json/v1/1/search.php?s=margarita')
    data = cocktail_res.json()
    return render_template('index.html', data=data)