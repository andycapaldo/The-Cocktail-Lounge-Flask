import requests
from datetime import date
from app import app, db
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.forms import SignUpForm, LoginForm, DrinkForm
from app.models import User, Cocktail, Comment


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


# Route for viewing all 3rd party API cocktails
@app.route('/cocktails')
def cocktails():
    alcoholic= requests.get('https://www.thecocktaildb.com/api/json/v2/9973533/filter.php?a=Alcoholic')
    non_alcoholic= requests.get('https://www.thecocktaildb.com/api/json/v2/9973533/filter.php?a=Non_Alcoholic')
    drinks_one = alcoholic.json()['drinks']
    drinks_two = non_alcoholic.json()['drinks']
    data = sorted((drinks_one + drinks_two), key=lambda x: x['strDrink'])
    today = date.today()
    return render_template('cocktails.html', data=data, today=today)


# Route for viewing a specific cocktail from the 3rd party API
@app.route('/cocktails/<drink_id>')
def cocktail_view(drink_id):
    response = requests.get(f'https://www.thecocktaildb.com/api/json/v2/9973533/lookup.php?i={drink_id}')
    data = response.json()['drinks'][0]
    res = {k:v for k,v in data.items() if v is not None}
    ingredients = ['strIngredient1', 'strIngredient2', 'strIngredient3', 'strIngredient4', 'strIngredient5', 'strIngredient6', 'strIngredient7', 'strIngredient8', 'strIngredient9', 'strIngredient10', 'strIngredient11', 'strIngredient12', 'strIngredient13', 'strIngredient14', 'strIngredient15']
    measures = ['strMeasure1', 'strMeasure2', 'strMeasure3', 'strMeasure4', 'strMeasure5', 'strMeasure6', 'strMeasure7', 'strMeasure8', 'strMeasure9', 'strMeasure10', 'strMeasure11', 'strMeasure12', 'strMeasure13', 'strMeasure14', 'strMeasure15']
    return render_template('cocktail.html', res=res, ingredients=ingredients, measures=measures)


# For creating cocktails local to this application's database
@app.route('/create-drink', methods=['GET', 'POST'])
@login_required
def create_drink():
    form = DrinkForm()
    if form.validate_on_submit():
            drink_name = form.drink_name.data
            glass_type = form.glass_type.data
            ingredient_1 = form.ingredient_1.data
            measure_1 = form.measure_1.data
            ingredient_2 = form.ingredient_2.data
            measure_2 = form.measure_2.data
            ingredient_3 = form.ingredient_3.data
            measure_3 = form.measure_3.data
            ingredient_4 = form.ingredient_4.data
            measure_4 = form.measure_4.data
            ingredient_5 = form.ingredient_5.data
            measure_5 = form.measure_5.data
            ingredient_6 = form.ingredient_6.data
            measure_6 = form.measure_6.data
            ingredient_7 = form.ingredient_7.data
            measure_7 = form.measure_7.data
            ingredient_8 = form.ingredient_8.data
            measure_8 = form.measure_8.data
            ingredient_9 = form.ingredient_9.data
            measure_9 = form.measure_9.data
            ingredient_10 = form.ingredient_10.data
            measure_10 = form.measure_10.data
            instructions = form.instructions.data
            image_url = form.image_url.data
            drink_type = form.drink_type.data

            new_drink = Cocktail( drink_name=drink_name, glass_type=glass_type, ingredient_1=ingredient_1, measure_1=measure_1, ingredient_2=ingredient_2, measure_2=measure_2, ingredient_3=ingredient_3, measure_3=measure_3, ingredient_4=ingredient_4, measure_4=measure_4, ingredient_5=ingredient_5, measure_5=measure_5, ingredient_6=ingredient_6, measure_6=measure_6, ingredient_7=ingredient_7, measure_7=measure_7, ingredient_8=ingredient_8, measure_8=measure_8, ingredient_9=ingredient_9, measure_9=measure_9, ingredient_10=ingredient_10, measure_10=measure_10, instructions=instructions, image_url=image_url, drink_type=drink_type, user_id=current_user.id)

            db.session.add(new_drink)
            db.session.commit()
            
            flash(f"{drink_name} has been created!")
            return redirect(url_for('index'))

    return render_template('create_drink.html', form=form)


# Show's information about the user as well as any drinks they've submitted to the database
@app.route('/profile/<user_id>')
def profile_view(user_id):
    user = db.session.get(User, user_id)
    if not user:
        flash('That user does not exist')
        return redirect(url_for('index'))
    cocktails = db.session.execute(db.select(Cocktail).where(Cocktail.user_id==user_id).order_by(db.desc(Cocktail.date_created))).scalars().all()
    return render_template('profile.html', user=user, cocktails=cocktails)



# View for all user submitted cocktails
@app.route('/user-drinks', methods=['GET'])
def user_cocktails_view():
    cocktails = db.session.execute(db.select(Cocktail).order_by(db.desc(Cocktail.drink_name))).scalars().all()
    print([c.image_url for c in cocktails])
    return render_template('user_cocktails.html', cocktails=cocktails)


# Specific view for user-submitted cocktail by drink_id
@app.route('/user-drinks/<drink_id>')
def user_cocktail_view(drink_id):
    cocktail = db.session.get(Cocktail, drink_id)
    if not cocktail:
        flash('That drink does not exist')
        return redirect(url_for('index'))
    return render_template('user_cocktail.html', cocktail=cocktail)


# Route for user to delete a drink that they've submitted
@app.route('/user-drinks/<drink_id>/delete', methods=['GET'])
@login_required
def delete_drink(drink_id):
    cocktail = db.session.get(Cocktail, drink_id)
    if not cocktail:
        flash('That drink does not exist')
        return redirect(url_for('index'))
    if current_user != cocktail.author:
        flash('You can only delete cocktails you have created!')
        return redirect(url_for('user_cocktail_view',  drink_id=cocktail.id))
    
    db.session.delete(cocktail)
    db.session.commit()

    flash(f"{cocktail.drink_name} has been deleted")
    return redirect(url_for('index'))


@app.route('/user-drinks/<drink_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_drink(drink_id):
    cocktail = db.session.get(Cocktail, drink_id)
    if not cocktail:
        flash('That drink does not exist')
        return redirect(url_for('index'))
    if current_user != cocktail.author:
        flash('You can only edit cocktails you have created!')
        return redirect(url_for('user_cocktail.html', drink_id=cocktail.id))
    
    form = DrinkForm()

    if form.validate_on_submit():
        cocktail.drink_name = form.drink_name.data
        cocktail.glass_type = form.glass_type.data
        cocktail.ingredient_1 = form.ingredient_1.data
        cocktail.measure_1 = form.measure_1.data
        cocktail.ingredient_2 = form.ingredient_2.data
        cocktail.measure_2 = form.measure_2.data
        cocktail.ingredient_3 = form.ingredient_3.data
        cocktail.measure_3 = form.measure_3.data
        cocktail.ingredient_4 = form.ingredient_4.data
        cocktail.measure_4 = form.measure_4.data
        cocktail.ingredient_5 = form.ingredient_5.data
        cocktail.measure_5 = form.measure_5.data
        cocktail.ingredient_6 = form.ingredient_6.data
        cocktail.measure_6 = form.measure_6.data
        cocktail.ingredient_7 = form.ingredient_7.data
        cocktail.measure_7 = form.measure_7.data
        cocktail.ingredient_8 = form.ingredient_8.data
        cocktail.measure_8 = form.measure_8.data
        cocktail.ingredient_9 = form.ingredient_9.data
        cocktail.measure_9 = form.measure_9.data
        cocktail.ingredient_10 = form.ingredient_10.data
        cocktail.measure_10 = form.measure_10.data
        cocktail.instructions = form.instructions.data
        cocktail.image_url = form.image_url.data
        cocktail.drink_type = form.drink_type.data

        db.session.commit()
        flash(f"{cocktail.drink_name} has been edited.", 'success')
        return redirect(url_for('index'))
    
    form.drink_name.data = cocktail.drink_name
    form.glass_type.data = cocktail.glass_type
    form.ingredient_1.data = cocktail.ingredient_1
    form.measure_1.data = cocktail.measure_1
    form.ingredient_2.data = cocktail.ingredient_2
    form.measure_2.data = cocktail.measure_2
    form.ingredient_3.data = cocktail.ingredient_3
    form.measure_3.data = cocktail.measure_3
    form.ingredient_4.data = cocktail.ingredient_4
    form.measure_4.data = cocktail.measure_4
    form.ingredient_5.data = cocktail.ingredient_5
    form.measure_5.data = cocktail.measure_5
    form.ingredient_6.data = cocktail.ingredient_6
    form.measure_6.data = cocktail.measure_6
    form.ingredient_7.data = cocktail.ingredient_7
    form.measure_7.data = cocktail.measure_7
    form.ingredient_8.data = cocktail.ingredient_8
    form.measure_8.data = cocktail.measure_8
    form.ingredient_9.data = cocktail.ingredient_9
    form.measure_9.data = cocktail.measure_9
    form.ingredient_10.data = cocktail.ingredient_10
    form.measure_10.data = cocktail.measure_10
    form.instructions.data = cocktail.instructions
    form.image_url.data = cocktail.image_url
    form.drink_type.data = cocktail.drink_type
    return render_template('edit_drink.html', cocktail=cocktail, form=form)


@app.route("/create-comment/<drink_id>", methods=["POST"])
@login_required
def create_comment(drink_id):
    text = request.form.get('text')

    if not text:
        flash('Comment cannot be empty.', 'error')
    else:
        cocktail = Cocktail.query.filter_by(id=drink_id)
        if cocktail:
            comment = Comment(text=text, user_id=current_user.id, cocktail_id=drink_id)
            db.session.add(comment)
            db.session.commit()
        else:
            flash('That drink does not exist.')
    
    return redirect(url_for('index'))


@app.route('/delete-comment/<comment_id>')
@login_required
def delete_comment(comment_id):
    comment = Comment.query.filter_by(id=comment_id).first()

    if not comment:
        flash('Comment does not exist.', 'error')
    elif current_user.id != comment.user_id and current_user.id != comment.cocktail.user_id:
        flash('You do not have permission to delete this comment.', 'error')
    else:
        db.session.delete(comment)
        db.session.commit()

    return redirect(url_for('index'))