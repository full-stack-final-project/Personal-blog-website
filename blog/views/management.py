import os
from flask import Blueprint, render_template

from blog.extensions import db
from blog.forms import setting_form, article_form, category_form
from blog.models import Article, Category, Comment


manage_blueprint = Blueprint('management', __name__)


@manage_blueprint.route('/article/manage')
@login_required
def manage_article():
    page = request.args.get('page', 1, type=int)
    onepage = Article.query.order_by(
        Article.timestamp.desc()).paginate(
        page, per_page=current_app.config['MANAGE_ARTICLE_PER_PAGE'])
    onepage_articles = onepage.items
    return render_template('manage/manage_article.html', page=page, pagination=onepage, onepage_articles=onepage_articles)
    