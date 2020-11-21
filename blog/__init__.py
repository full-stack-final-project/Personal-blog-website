import os
from blog.views.admin import admin_blueprint
from blog.views.authorization import authorization_buleprint
from blog.views.blogs import blogs_blueprint
from config import config

from flask import Flask

app = Flask('A blog website by Yihua and Junhao')
app.config.from_pyfile('config.py')

def register_blueprints(app):
    app.register_blueprint(blogs_blueprint)
    app.register_blueprint(authorization_buleprint, url_prefix='/authorization')
    app.register_blueprint(admin_blueprint, url_prefix='admin')

def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    app = Flask('Personal-blog-website')
    app.config.from_object(config[config_name])

    register_blueprints(app)

    return app
