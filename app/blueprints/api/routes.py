from flask import request
from . import api
from app import db
from app.models import User, Cocktail, Comment
from .auth import basic_auth, token_auth
from .helpers import camel_to_snake

# Endpoint to get token - requires username/password
@api.route('/token')
@basic_auth.login_required
def get_token():
    auth_user = basic_auth.current_user()
    token = auth_user.get_token()
    return {'token': token}


# Endpoint to create a new User
@api.route('/users', methods=['POST'])
def create_user():
    if not request.is_json:
        return {'error': 'Your content type must be application/json.'}, 400
    
    data = request.json

    required_fields = ['firstName', 'lastName', 'email', 'username', 'password']
    missing_fields = []
    for field in required_fields:
        if field not in data:
            missing_fields.append(field)
        if missing_fields:
            return {'error': f"{', '.join(missing_fields)} must be in the request body."}, 400
        
    first_name = data.get('firstName')
    last_name = data.get('lastName')
    email = data.get('email')
    username = data.get('username')
    password = data.get('password')

    check_user = db.session.execute(db.select(User).where( (User.username==username) | (User.email==email) )).scalars().all()
    if check_user:
        return {'error': 'A user with that username and/or email already exists.'}, 400
    
    new_user = User(first_name=first_name, last_name=last_name, email=email, username=username, password=password)

    db.session.add(new_user)
    db.session.commit()

    return new_user.to_dict(), 201


# Endpoint to get user based on token
@api.route('/users/me', methods={'GET'})
@token_auth.login_required
def get_me():
    current_user = token_auth.current_user()
    return current_user.to_dict()


# Endpoint to edit user info using token auth
@api.route('/users/<user_id>', methods=['PUT'])
@token_auth.login_required
def edit_user(user_id):
    if not request.is_json:
        return {'error': 'Your content-type must be application/json'}, 400
    user = db.session.get(User, user_id)
    if user is None:
        return {'error': f"User with an ID of {user_id} does not exist."}, 404
    current_user = token_auth.current_user()
    if user != current_user:
        return {'error': 'You do not have permission to edit this user'}, 403
    
    data = request.json
    required_fields = ['email']
    missing_fields = []
    for field in required_fields:
        if field not in data:
            missing_fields.append(field)
    if missing_fields:
        return {'error': f"{', '.join(missing_fields)} must be in the request body"}, 400
    
    for field in data:
        if field in {'email'}:
            setattr(user, 'email', data[field])
    db.session.commit()
    return user.to_dict()


# Endpoint to delete a user profile using token auth
@api.route('/users/<user_id>', methods=['DELETE'])
@token_auth.login_required
def delete_user(user_id):
    user = db.session.get(User, user_id)
    if user is None:
        return {'error': f"User with an ID of {user_id} does not exist."}, 404
    
    current_user = token_auth.current_user()
    if user != current_user:
        return {'error': 'You do not have permission to delete this user'}, 403
    db.session.delete(user)
    db.session.commit()
    return {'success': f"{user.username} has been deleted."}


# Endpoint to get all user created cocktails
@api.route('/cocktails', methods=['GET'])
def get_cocktails():
    cocktails = db.session.execute(db.select(Cocktail)).scalars().all()
    return [cocktail.to_dict() for cocktail in cocktails]


# Endpoint to get a user created cocktail by ID
@api.route('/cocktails/<cocktail_id>')
def get_cocktail(cocktail_id):
    cocktail = db.session.get(Cocktail, cocktail_id)
    if not cocktail:
        return {'error': f'Cocktail with an ID of {cocktail_id} does not exist.'}, 404
    return cocktail.to_dict()


# Endpoint to get all comments on user created cocktails
@api.route('/comments', methods=['GET'])
def get__comments():
    comments = db.session.execute(db.select(Comment)).scalars().all()
    return [comment.to_dict() for comment in comments]


# Endpoint to get all comments for a specific cocktail
@api.route('/comments/<cocktail_id>', methods=['GET'])
def get_comments_unique(cocktail_id):
    comments = Comment.query.where(Comment.cocktail_id==cocktail_id)
    if not comments:
        return {'error': f"No comments exist for cocktail with an ID of {cocktail_id}."}, 404
    return [comment.to_dict() for comment in comments]


# Endpoint to get a specific comment by comment ID
@api.route('/comment/<comment_id>', methods=['GET'])
def get_comment(comment_id):
    comment = db.session.get(Comment, comment_id)
    if not comment:
        return {'error': f"Comment with an ID of {comment_id} does not exist."}, 404
    return comment.to_dict()


# Endpoint to create a comment on a specific cocktail
@api.route('/comments/<cocktail_id>', methods=['POST'])
@token_auth.login_required
def create_comment(cocktail_id):
    if not request.is_json:
        return {'error': 'Your content-type must be application/json'}, 400
    data = request.json

    required_fields = ['text']
    missing_fields = []
    for field in required_fields:
        if field not in data:
            missing_fields.append(field)
    if missing_fields:
        return {'error': f"{', '.join(missing_fields)} must be in the request body"}, 400
    
    text = data.get('text')
    current_user = token_auth.current_user()

    new_comment = Comment(text=text, user_id=current_user.id, cocktail_id=cocktail_id)
    db.session.add(new_comment)
    db.session.commit()
    return new_comment.to_dict(), 201


# Endpoint to delete a comment
@api.route('/comment/<comment_id>', methods=['DELETE'])
@token_auth.login_required
def delete_comment(comment_id):
    comment = db.session.get(Comment, comment_id)
    if not comment:
        return {'error': f"Comment with an ID of {comment_id} does not exist."}, 404
    current_user = token_auth.current_user()
    if comment.author != current_user:
        return {'error': 'You do not have permission to delete this comment.'}, 403
    
    db.session.delete(comment)
    db.session.commit()
    return {'success': f"Comment #{comment.id} has been deleted."}


# Endpoint to create a new cocktail
@api.route('/cocktails', methods=['POST'])
@token_auth.login_required
def create_drink():
    if not request.is_json:
        return {'error': 'Your content type must be application/json.'}, 400
    
    data = request.json

    required_fields = ['drinkName', 'glassType', 'instructions', 'imageUrl', 'drinkType', 'ingredient1', 'measure1', 'ingredient2', 'measure2']
    missing_fields = []
    for field in required_fields:
        if field not in data:
            missing_fields.append(field)
    if missing_fields:
        return {'error': f"{', '.join(missing_fields)} must be in the request body."}, 400
    drink_name = data.get('drinkName')
    glass_type = data.get('glassType')
    instructions = data.get('instructions')
    image_url = data.get('imageUrl')
    drink_type = data.get('drinkType')
    ingredient_1 = data.get('ingredient1')
    measure_1 = data.get('measure1')
    ingredient_2 = data.get('ingredient2')
    measure_2 = data.get('measure2')
    ingredient_3 = data.get('ingredient3')
    measure_3 = data.get('measure3')
    ingredient_4 = data.get('ingredient4')
    measure_4 = data.get('measure4')
    ingredient_5 = data.get('ingredient5')
    measure_5 = data.get('measure5')
    ingredient_6 = data.get('ingredient6')
    measure_6 = data.get('measure6')
    ingredient_7 = data.get('ingredient7')
    measure_7 = data.get('measure7')
    ingredient_8 = data.get('ingredient8')
    measure_8 = data.get('measure8')
    ingredient_9 = data.get('ingredient9')
    measure_9 = data.get('measure9')
    ingredient_10 = data.get('ingredient10')
    measure_10 = data.get('measure10')

    current_user = token_auth.current_user()

    new_drink = Cocktail(drink_name=drink_name, glass_type=glass_type, instructions=instructions, image_url=image_url, drink_type=drink_type, ingredient_1=ingredient_1, measure_1=measure_1, ingredient_2=ingredient_2, measure_2=measure_2, ingredient_3=ingredient_3, measure_3=measure_3, ingredient_4=ingredient_4, measure_4=measure_4, ingredient_5=ingredient_5, measure_5=measure_5, ingredient_6=ingredient_6, measure_6=measure_6, ingredient_7=ingredient_7, measure_7=measure_7, ingredient_8=ingredient_8, measure_8=measure_8, ingredient_9=ingredient_9, measure_9=measure_9, ingredient_10=ingredient_10, measure_10=measure_10, user_id=current_user.id)
    
    db.session.add(new_drink)
    db.session.commit()
    return new_drink.to_dict(), 201



# Endpoint to edit an existing cocktail
@api.route('/cocktails/<cocktail_id>', methods=['PUT'])
@token_auth.login_required
def edit_cocktail(cocktail_id):
    if not request.is_json:
        return {'error': 'Your content type must be application/json.'}, 400
    
    cocktail = db.session.get(Cocktail, cocktail_id)
    if cocktail is None:
        return {'error': f"Cocktail with an ID of {cocktail_id} does not exist."}, 404
    
    current_user = token_auth.current_user()
    if cocktail.author != current_user:
        return {'error': 'You do not have permission to edit this cocktail.'}, 403
    data = request.json
    for field in data:
        if field in {'drinkName', 'glassType', 'instructions', 'imageUrl', 'drinkType', 'ingredient1', 'measure1', 'ingredient2', 'measure2', 'ingredient3', 'measure3', 'ingredient4', 'measure4', 'ingredient5', 'measure5', 'ingredient6', 'measure6', 'ingredient7', 'measure7', 'ingredient8', 'measure8', 'ingredient9', 'measure9', 'ingredient10', 'measure10'}:
                setattr(cocktail, camel_to_snake(field), data[field])

    db.session.commit()
    return cocktail.to_dict()
    



# Endpoint to delete an existing cocktail
@api.route('/cocktails/<cocktail_id>', methods=["DELETE"])
@token_auth.login_required
def delete_cocktail(cocktail_id):
    cocktail = db.session.get(Cocktail, cocktail_id)
    if cocktail is None:
        return {'error': f"Cocktail with an ID of {cocktail_id} does not exist."}, 404
    
    current_user = token_auth.current_user()
    if cocktail.author != current_user:
        return {'error': 'You do not have permission to delete this cocktail.'}, 403
    
    db.session.delete(cocktail)
    db.session.commit()
    return {'success': f"{cocktail.drink_name} has been deleted."}