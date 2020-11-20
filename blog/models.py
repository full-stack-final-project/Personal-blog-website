from datetime import datetime
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Admin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(30))
    name = db.Column(db.String(30))
    about = db.Column(db.Text)
    password = db.Column(db.String(128))
    blog_title = db.Column(db.String(50))
    
class Article(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(50))
    body = db.Column(db.Text)
    category = db.relationship('Category', back_populates = 'articles')
    timestamp = db.Column(db.Datetime, default = datetime.utcnow, index = True)
    comment_open = db.Column(db.Boolean, default = True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    comments = db.relationship('Comment', back_populates = 'article', cascade = 'all, delete-orphan')

class Category(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(30), unique = True)
    articles = db.relationship('Article', back_populates = 'category')

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    person_post = db.Column(db.String(30))
    body = db.Column(db.Text)
    from_admin = db.Column(db.Boolean, default = False)
    reviewed = db.Column(db.Boolean, default = False)
    timestamp = db.Column(db.Datetime, default = datetime.utcnow, index = True)
    email = db.Column(db.String(255))
    site = db.Column(db.String(255))
    reply_id = db.Column(db.Integer, db.ForeignKey('comment.id'))
    article_id = db.Column(db.Integer, db.ForeignKey('article.id'))
    # to support comments to reply comments
    article = db.relationship('Article', back_populates = 'comments')
    replies = db.relationship('Comment', back_populates = 'replied', cascade = 'all, delete-orphan')
    replied = db.relationship('Comment', back_populates = 'replies', remote_side = [id])