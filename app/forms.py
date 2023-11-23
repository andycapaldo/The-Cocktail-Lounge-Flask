from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, SubmitField, BooleanField, RadioField, TextAreaField
from wtforms.validators import InputRequired, EqualTo


class SignUpForm(FlaskForm):
    first_name = StringField('First Name', validators=[InputRequired()])
    last_name = StringField('Last Name', validators=[InputRequired()])
    username = StringField('Username', validators=[InputRequired()])
    email = EmailField('Email Address', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    confirm_pass = PasswordField('Confirm Password', validators=[InputRequired()])
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Log In')


class DrinkForm(FlaskForm):
    drink_name = StringField('Drink Name', validators=[InputRequired()])
    glass_type = StringField('Glass Type', validators=[InputRequired()])
    ingredient_1 = StringField('Ingredient #1', validators=[InputRequired()])
    measure_1 = StringField('Measure #1', validators=[InputRequired()])
    ingredient_2 = StringField('Ingredient #2', validators=[InputRequired()])
    measure_2 = StringField('Measure #2', validators=[InputRequired()])
    ingredient_3 = StringField('Ingredient #3')
    measure_3 = StringField('Measure #3')
    ingredient_4 = StringField('Ingredient #4')
    measure_4 = StringField('Measure #4')
    ingredient_5 = StringField('Ingredient #5')
    measure_5 = StringField('Measure #5')
    ingredient_6 = StringField('Ingredient #6')
    measure_6 = StringField('Measure #6')
    ingredient_7 = StringField('Ingredient #7')
    measure_7 = StringField('Measure #7')
    ingredient_8 = StringField('Ingredient #8')
    measure_8 = StringField('Measure #8')
    ingredient_9 = StringField('Ingredient #9')
    measure_9 = StringField('Measure #9')
    ingredient_10 = StringField('Ingredient #10')
    measure_10 = StringField('Measure #10')
    instructions = TextAreaField('Recipe Instructions', validators=[InputRequired()])
    image_url = StringField('Image URL', validators=[InputRequired()])
    drink_type = BooleanField('Is this an Alcholic Cocktail? (Uncheck if Non-Alcoholic)', validators=[InputRequired()], default='True')
    submit = SubmitField('Create Drink')