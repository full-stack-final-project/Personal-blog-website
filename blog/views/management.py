import os
from flask import Blueprint, render_template

from blog.extensions import db
from blog.forms import setting_form, article_form, category_form
from blog.models import Article, Category, Comment


admin_blueprint = Blueprint('admin', __name__)


@admin_blueprint.route('/article/manage')
@login_required
def manage_article():
    page = request.args.get('page', 1, type=int)
    onepage = Post.query.order_by(
        Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['BLUELOG_MANAGE_POST_PER_PAGE'])
    onepage_articles = onepage.items
    return render_template('admin/manage_article.html', page=page, pagination=onepage, onepage_articles=onepage_articles)
    