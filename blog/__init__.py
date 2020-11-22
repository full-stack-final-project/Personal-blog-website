import os
from blog.views.admin import admin_blueprint
from blog.views.authorization import authorization_buleprint
from blog.views.blogs import blogs_blueprint
from config import config
from extensions import db, csrf
from blog.models import Admin, Article, Category, Comment, Link
from flask_wtf.csrf import CSRFError

from flask import Flask

app = Flask('A blog website by Yihua and Junhao')
app.config.from_pyfile('config.py')

def register_blueprints(app):
    app.register_blueprint(blogs_blueprint)
    app.register_blueprint(authorization_buleprint, url_prefix='/authorization')
    app.register_blueprint(admin_blueprint, url_prefix='admin')
    

def register_extensions(app):
    db.init_app(app)
    csrf.init_app(app)

def register_commands(app):
    @app.cli.command()
    @click.option('--username', prompt=True)
    @click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True)
    @click.option('--site_title', prompt=True)

    def init(username, password):

        click.echo('Initializing...')
        db.crete_all()

        admin = Admin.query.first()
        if admin is not None:
            admin.username = username
            admin.set_password(password)
        
        else:
            admin = Admin(username=username, name='Admin', site_title=site_title, about="")
            admin.set_password(password)
            db.session.add(admin)

        if Category.query.first() is None:
            category = Category(name='Default')
            db.session.add(category)
        
        db.session.commit()


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    app = Flask('Personal-blog-website')
    app.config.from_object(config[config_name])

    register_blueprints(app)
    register_extensions(app)
    register_commands(app)

    return app

@app.errorhandler(CSRFError)
def handle_csrf_error(e):
    return 
