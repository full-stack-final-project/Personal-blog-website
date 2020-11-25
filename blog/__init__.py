import os

from blog.views.management import manage_blueprint
from blog.views.authorization import authorization_buleprint
from blog.views.blogs import blogs_blueprint
from blog.config import config
from blog.extensions import db, csrf, bootstrap
from blog.models import Admin, Article, Category, Comment
from flask_wtf.csrf import CSRFError
from blog.extensions import mail, moment

from flask_sqlalchemy import get_debug_queries
from flask import Flask, render_template
from flask_login import current_user
import click
from blog.extensions import login_manager, ckediter

def register_blueprints(app):
    app.register_blueprint(blogs_blueprint)
    app.register_blueprint(authorization_buleprint, url_prefix='/authorization')
    app.register_blueprint(manage_blueprint, url_prefix='/management')
    

def register_extensions(app):
    db.init_app(app)
    csrf.init_app(app)
    bootstrap.init_app(app)
    ckediter.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    login_manager.init_app(app)

def register_shell(app):
    @app.shell_context_processor
    def make_shell_context():
        return dict(db=db, Admin=Admin, Article=Article, Category=Category, Comment=Comment)

def register_commands(app):
    @app.cli.command()
    @click.option('--drop', is_flag=True)
    def init_database(drop):
        if drop:
            db.drop_all()
        db.crete_all()


    @app.cli.command()
    @click.option('--username', prompt=True)
    @click.option('--password', prompt=True, 
                                hide_input=True, 
                                confirmation_prompt=True)
    @click.option('--site_title', prompt=True)
    def init(username, password):

        click.echo('Initializing...')
        

        admin = Admin.query.first()
        if admin is not None:
            admin.username = username
            admin.set_password(password)
        
        else:
            admin = Admin(username=username, 
                          name='Admin', 
                          site_title=site_title, about="")
            admin.set_password(password)
            db.session.add(admin)

        if Category.query.first() is None:
            category = Category(name='Default')
            db.session.add(category)
        
        db.session.commit()

    @app.cli.command()
    @click.option('--num_category', default=10)
    @click.option('--num_article', default=50)
    @click.option('--num_comment', default=100)
    def make_faker(num_category, num_article, num_comment):
        from blog.fake_data import fake_admin, fake_articles, fake_categories, fake_comments

        db.drop_all()
        db.create_all()
        
        fake_admin()
        fake_categories(num_category)
        fake_articles(num_article)
        fake_comments(num_comment)

def register_template(app):
    @app.context_processor
    def make_template_context():
        
        admin = Admin.query.first()
        categories = Category.query.order_by(Category.name).all()
        if current_user.is_authenticated:
            unread_comments = Comment.query.filter_by(reviewed=False).count()
        else:
            unread_comments = None
        return dict(admin=admin,
            categories=categories,
            unread_comments=unread_comments) 



def create_app(config_name=None):
    
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    app = Flask('blog')
    app.config.from_object(config[config_name])

    register_blueprints(app)
    register_extensions(app)
    register_commands(app)
    register_template(app)

    register_errors(app)
    register_shell(app)

    return app

def register_errors(app):

    @app.errorhandler(CSRFError)
    def handle_csrf_error(e):
        return 
