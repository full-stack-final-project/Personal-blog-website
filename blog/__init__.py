import os

from blog.views.management import manage_blueprint
from blog.views.authorization import authorization_buleprint
from blog.views.blog import blog_blueprint
from blog.config import config
from blog.extensions import db, csrf, bootstrap
from blog.models import Admin, Article, Category, Comment
from flask_wtf.csrf import CSRFError
from blog.extensions import mail, moment, migrate

from flask_sqlalchemy import get_debug_queries
from flask import Flask, render_template, request
from flask_login import current_user
import click
from blog.extensions import login_manager, ckeditor
import logging
from logging.handlers  import SMTPHandler, RotatingFileHandler

root = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

def register_blueprints(app):
    app.register_blueprint(blog_blueprint)
    app.register_blueprint(authorization_buleprint, url_prefix='/authorization')
    app.register_blueprint(manage_blueprint, url_prefix='/management')

def register_logging(app):
    class RequsetFormatter(logging.Formatter):

        def format(self, record):
            record.url = request.url
            record.remote_addr = request.remote_addr
            return super(RequsetFormatter, self).format(record)

    request_formatter = RequsetFormatter(
        '[%(asctime)s] %(remote_addr)s requested %(url)s\n'
        '%(levelname)s in %(module)s: %(message)s'
    ) 
    formatter =  logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler = RotatingFileHandler(os.path.join(root, 'logs/blog.log'), maxBytes=124*10240, backupCount=10)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)

    mail_handler = SMTPHandler(
        mailhost=app.config['MAIL_SERVER'],
        fromaddr=app.config['MAIL_USERNAME'],
        toaddrs=app.config['MAIL_USERNAME'],
        subject='Site Application Error',
        credentials=(app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD']))
    mail_handler.setLevel(logging.ERROR)
    mail_handler.setFormatter(request_formatter)

    if not app.debug:
        app.logger.addHandler(mail_handler)
        app.logger.addHandler(file_handler)

def register_extensions(app):
    db.init_app(app)
    csrf.init_app(app)
    bootstrap.init_app(app)
    ckeditor.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

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
    def init(username, password):

        click.echo('Initializing...')
        

        admin = Admin.query.first()
        if admin is not None:
            admin.username = username
            admin.set_password(password)
        
        else:
            admin = Admin(username=username, 
                          name='Admin', 
                          site_title="Jason's site", about="")
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

    register_logging(app)

    return app

def register_errors(app):

    @app.errorhandler(CSRFError)
    def handle_csrf_error(e):
        return render_template('error/400.html', description=e.description), 400
    
    @app.errorhandler(400)
    def bad_request(e):
        return render_template('error/400.html'), 400
    
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('error/404.html'), 404
    
    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('error/500.html'), 500

