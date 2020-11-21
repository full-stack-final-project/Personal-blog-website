from flask import Blueprint

blogs_blueprint = Blueprint('blogs', __name__)

@blogs_blueprint.route('CV')
def DirectCv():
    return "This should be a CV webpage, including experience and skills"


@blogs_blueprint.route('/category/<int:category_id>')
def DirectCategory():
    return "The blog webpage you want to read"