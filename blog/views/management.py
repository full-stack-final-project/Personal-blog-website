import os
from flask import Blueprint, render_template
from flask_login import login_user, logout_user
from flask_login import login_required, current_user
from blog.forms import bio_form, article_form, category_form
from blog.extensions import db

from blog.models import Article, Category, Comment
from flask import render_template, flash, redirect, url_for
from flask import  request, current_app

manage_blueprint = Blueprint('management', __name__)

try:
    from urlparse import urlparse, urljoin
except ImportError:
    from urllib.parse import urlparse, urljoin

def safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc

def redirect_to_last_page(default = 'blog.index', **kwargs):
    for target in request.args.get('next'), request.referrer:
        if not target:
            continue
        if safe_url(target):
            return redirect(target)
    return redirect(url_for(default, **kwargs))

@manage_blueprint.route('/article/manage')
@login_required
def manage_article():
    page = request.args.get('page', 1, type=int)
    onepage = Article.query.order_by(
        Article.timestamp.desc()).paginate(
        page, per_page=current_app.config['MANAGE_ARTICLE_PER_PAGE'])
    onepage_articles = onepage.items
    return render_template('manage/manage_article.html', page=page, pagination=onepage, articles=onepage_articles)


@manage_blueprint.route('/article/<int:article_id>/edit', methods=['POST', 'GET'])
@login_required
def edit_article(article_id):
    form = article_form()
    article = Article.query.get_or_404(article_id)
    if form.validate_on_submit():
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

@manage_blueprint.route('/article/<int:article_id>/delete', methods=['POST'])
@login_required
def delete_article(article_id):
    article = Article.query.get_or_404(article_id)
    db.session.delete(article)
    db.session.commit()
    flash('Deleted', 'success')
    return redirect(url_for('blog.display_article', article_id=article.id))

@manage_blueprint.route('/category/manage')
@login_required
def manage_category():
    return render_template('manage/manage_categories.html')

@manage_blueprint.route('/category/<int:category_id>/delete', methods=['POST'])
@login_required
def delete_category(category_id):
    category = Category.query.get_or_404(category_id)
    if category.id == 1:
        flash('This is a default category! Cannot delete!', 'warning')
        return render_template('manage/manage_categories.html')
    category.delete()
    flash('Deleted', 'success')
    return render_template('manage/manage_categories.html')

@manage_blueprint.route('/article/add', methods = ['GET', 'POST'])
@login_required
def add_article():
    form = article_form()
    if form.validate_on_submit():
        title = form.title.data 
        body = form.body.data 
        category = form.category.data    
        article = Article(title=title, body=body, category=category)
        db.session.add(article)
        db.session.commit()
        flash('Added', 'success')
        return redirect(url_for('blog.display_article', article_id=article.id))
    return render_template('manage/add_article.html', form=form)

@manage_blueprint.route('/category/new', methods=['GET','POST'])
@login_required
def add_category():
    form = category_form()
    if form.validate_on_submit():
        name = form.name.data 
        category = Category(name=name)
        db.session.add(category)
        db.session.commit()
        flash('Added', 'success')
        return redirect(url_for('.manage_category'))
    return render_template('manage/add_category.html', form=form)

@manage_blueprint.route('/category/<int:category_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_category(category_id):
    form = category_form()
    category = Category.query.get_or_404(category_id)
    if category.id == 1:
        flash('This is a default category! Cannot Edit!', 'warning')
        return render_template('manage/manage_category.html')
    if form.validate_on_submit():
        category.name = form.name.data
        db.session.commit()
        flash("Edited", 'success')
        return redirect(url_for('.manage_category'))
    form.name.data = category.name 
    return render_template('manage/edit_category.html', form=form)

@manage_blueprint.route('article/<int:article_id>/set-comment')
@login_required
def set_comment(article_id):
    article = Article.query.get_or_404(article_id)
    if article.comment_open:
        article.comment_open = False
    else:
        article.comment_open = True
    db.session.commit()
    return redirect(url_for('.manage_article'))

@manage_blueprint.route('/comment/manage')
@login_required
def manage_comment():
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['MANAGE_COMMENT_PER_PAGE']
    if request.args.get('filter', 'all') == "unreviewed":
        f_comments = Comment.query.filter_by(reviewed=False)
    elif request.args.get('filter', 'all') == "admin":
        f_comments = Comment.query.filter_by(from_admin=True)
    else:
        f_comments = Comment.query
    
    pagination = f_comments.order_by(Comment.timestamp.desc()).paginate(page, per_page=per_page)
    comments = pagination.items
    return render_template('manage/manage_comments.html', Article=Article, comments=comments, pagination=pagination)

@manage_blueprint.route('/comment/<int:comment_id>/accept', methods=['POST'])
@login_required
def accept_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    comment.reviewed = True
    db.session.commit()
    return redirect_to_last_page()


@manage_blueprint.route('/comment/<int:comment_id>/delete', methods=['POST'])
@login_required
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    db.session.delete(comment)
    db.session.commit()
    flash('Deleted', 'success')
    return redirect_to_last_page()





    
