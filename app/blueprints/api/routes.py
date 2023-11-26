from . import api
from app import db
from app.models import User, Cocktail, Comment

# Get all user created cocktails
@api.route('/cocktails', methods=['GET'])
def get_cocktails():
    cocktails = db.session.execute(db.select(Cocktail)).scalars().all()
    return [cocktail.to_dict() for cocktail in cocktails]


# Get a user created cocktail by ID
@api.route('/cocktails/<cocktail_id>')
def get_cocktail(cocktail_id):
    cocktail = db.session.get(Cocktail, cocktail_id)
    if not cocktail:
        return {'error': f'Cocktail with an ID of {cocktail_id} does not exist'}, 404
    return cocktail.to_dict()


# Get all comments on user created cocktails
@api.route('/comments')
def get__comments():
    comments = db.session.execute(db.select(Comment)).scalars().all()
    return [comment.to_dict() for comment in comments]


# Get all comments for a specific cocktail
@api.route('/comments/<cocktail_id>')
def get_comments_unique(cocktail_id):
    comments = Comment.query.where(Comment.cocktail_id==cocktail_id)
    if not comments:
        return {'error': f"No comments exist for cocktail with an ID of {cocktail_id}"}, 404
    return [comment.to_dict() for comment in comments]