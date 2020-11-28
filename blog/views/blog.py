from flask import Blueprint
from blog.extensions import db
from blog.models import Article, Category, Comment
from blog.forms import comment_form, admin_comment_form
from flask import render_template, flash, redirect, url_for
from flask import request, current_app
from blog.emails import send_reply_comment, send_new_comment_reminding

from flask_login import current_user
from blog.views.management import redirect_to_last_page

blog_blueprint = Blueprint('blog', __name__)

@blog_blueprint.route('/')
def index():
    return render_template('blog/index.html')

@blog_blueprint.route('/recommand')
def recommand():
    page = request.args.get('page', 1, type = int)
    per_page = current_app.config['ARTICLE_PER_PAGE']
    
    pagination = Article.query.order_by(Article.count_read.desc()).paginate(page, per_page = per_page)
    articles = pagination.items
    return render_template('blog/recommand.html', pagination = pagination, articles = articles)

@blog_blueprint.route('/display')
def display():
    page = request.args.get('page', 1, type = int)
    per_page = current_app.config['ARTICLE_PER_PAGE']
    pagination = Article.query.order_by(Article.timestamp.desc()).paginate(page, per_page = per_page)
    articles = pagination.items
    return render_template('blog/display.html', pagination = pagination, articles = articles)

@blog_blueprint.route('/about')
def about():
    return "This should be a CV webpage, including experience and skills"


@blog_blueprint.route('/article/<int:article_id>', methods=['GET', 'POST'])
def display_article(article_id):
    article = Article.query.get_or_404(article_id)
    article.count_read = article.count_read + 1
    db.session.commit()
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['MANAGE_COMMENT_PER_PAGE']
    pagination = Comment.query.with_parent(article).filter_by(
        reviewed = True).order_by(Comment.timestamp.asc()).paginate(page, per_page)
    comments = pagination.items
    
    if current_user.is_authenticated:
        form = admin_comment_form()
        form.person_post.data = current_user.name
        form.email.data = current_app.config['MAIL_ADDRESS']
        from_admin = True
        reviewed = True 
        form.site.data = url_for('.index')
    else:
        form = comment_form()
        from_admin = False
        reviewed = False

    if form.validate_on_submit():
        person_post = form.person_post.data 
        email = form.email.data    
        body = form.body.data 
        site = form.site.data 
        comment = Comment(
            person_post=person_post,
            email=email,
            site=site,
            body=body,           
            article=article,
            from_admin=from_admin,
            reviewed=reviewed
        )
        reply_id = request.args.get('reply')
        if reply_id:
            replied_comment = Comment.query.get_or_404(reply_id)
            comment.replied = replied_comment
            send_reply_comment(replied_comment)
        db.session.add(comment)
        db.session.commit()

        if current_user.is_authenticated:
            flash('Displayed')
        else:
            flash('Will display after being accepted', 'success')
            send_new_comment_reminding(article)
        return redirect(url_for('.display_article', article_id=article_id))
    return render_template('blog/article.html', article=article, 
                                                pagination=pagination, 
                                                form=form, 
                                                comments=comments)

@blog_blueprint.route('/reply/comment/<int:comment_id>')
def reply_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    if not comment.article.comment_open:
        flash('Cannot comment this article')
        return redirect(url_for('.display_article', article_id=comment.article.id))
    return redirect( url_for('.display_article', article_id=comment.article_id, 
        reply=comment_id, person_post=comment.person_post) + '#comment-form')                                        
        


@blog_blueprint.route('/category/<int:category_id>')
def display_category(category_id):
    category = Category.query.get_or_404(category_id)
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['ARTICLE_PER_PAGE']
    pagination = Article.query.with_parent(category).order_by(Article.timestamp.desc()).paginate(page, per_page)
    articles = pagination.items
    return render_template('blog/category.html', category=category, 
        pagination=pagination, articles=articles)