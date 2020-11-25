from flask import Blueprint
from blog.emails import send_new_comment_reminding, reply_comment
from blog.extensions import db
from blog.models import Article, Category, Comment
from blog.forms import comment_form, admin_comment_form
from flask import render_template, flash, redirect, url_for
from flask import request, current_app

from flask_login import current_user

blog_blueprint = Blueprint('blog', __name__)

@blog_blueprint.route('/')
def index():
    page = request.args.get('page', 1, type = int)
    per_page = current_app.config['ARTICLE_PER_PAGE']
    pagination = Article.query.order_by(Article.timestamp.desc()).paginate(page, per_page = per_page)
    articles = pagination.items
    return render_template('blog/index.html', pagination = pagination, articles = articles)

@blog_blueprint.route('/about')
def about():
    return "This should be a CV webpage, including experience and skills"


@blog_blueprint.route('/article/<int:article_id>', methods=['GET', 'POST'])
def display_article(article_id):
    article = Article.query.get_or_404(article_id)
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['MANAGE_COMMENT_PER_PAGE']
    pagination = Comment.query.with_parent(article).filter_by(
        reviewed = True).order_by(Comment.timestamp.asc()).paginate(page, per_page)
    comments = pagination.items
    
    if current_user.is_authenticated:
        form = admin_comment_form()
        form.person_post.data = current_user.name
    return 'Not done yet.'    

@blog_blueprint.route('/category/<int:category_id>')
def display_category(category_id):
    return 'Not done yet.'