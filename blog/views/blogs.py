from flask import Blueprint
from blog.emails import send_new_comment_reminding, reply_comment
from blog.extensions import db
from blog.models import Article, Category, Comment
from blog.forms import comment_form, admin_comment_form
from flask import render_template, flash, redirect, url_for
from flask import request, current_app

blogs_blueprint = Blueprint('blogs', __name__)

@blogs_blueprint.route('/')
def index():
    page = request.args.get('page', 1, type = int)
    per_page = current_app.config['ARTICLE_PER_PAGE']
    pagination = Article.query.order_by(Article.timestamp.desc()).paginate(page, per_page = per_page)
    articles = pagination.items
    return render_template('blog/index.html', pagination = pagination, articles = articles)

@blogs_blueprint.route('/about')
def DirectCv():
    return "This should be a CV webpage, including experience and skills"


@blogs_blueprint.route('/category/<int:category_id>')
def DirectCategory():
    return "The blog webpage you want to read"