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


@manage_blueprint.route('/article/<int:article_id>/edit', methods=['POST', 'GET'])
@login_required
def edit_article(article_id):
    form = article_form()
    article = Article.query.get_or_404(article_id)
    if form.validate_on_sumbit():
        article.title = form.title.data 
        article.body = form.body.data 
        article.post = Category.query.get(form.category.data)
        db.session.commit()
        flash('Updated', 'success')
        return redirect(url_for('blog.display_article', article_id=article.id))
    form.title.data = article.title
    form.body.data = article.body
    form.category.data = article.category_id
    return render_template('manage/edit_article.html', form=form)

@manage_blueprint.route('article/<int:article_id>/delete', methods=['POST'])
@login_required
def delete_article(article_id):
    article = Article.query.get_or_404(article_id)
    db.session.delete(article)
    db.session.commit()
    flash('Deleted', 'success')
    return redirect_back()

@manage_blueprint.route('/category/manage')
@login_required
def manage_category():
    return render_template('mannage/manage_category.html')

@manage_blueprint.route('/category/<int:category_id>/delete', methods=['POST'])


    
