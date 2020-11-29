from datetime import datetime
from flask_login import UserMixin
from blog.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash

class Admin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(30))
    name = db.Column(db.String(30))
    about = db.Column(db.Text)
    password = db.Column(db.String(128))
    site_title = db.Column(db.String(50))

    def set_password(self, password):
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password, password)

class Bio(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(30))
    intro = db.Column(db.Text)
    current_job = db.Column(db.String(30))
    #skills = db.relationship('Skill', back_populates = 'bio')
    # projects = db.relationship('Project', back_populates = 'bio')

class Skill(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.String(60), unique = True)
    is_techical = db.Column(db.Boolean, default = True)
    #bio_id = db.Column(db.Integer, db.ForeignKey('bio.id'))
    #bio = db.relationship('Bio', back_populates = 'skills')

class Project(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(50))
    abstract = db.Column(db.Text)
    #bio_id = db.Column(db.Integer, db.ForeignKey('bio.id'))
    #bio = db.relationship('Bio', back_populates = 'projects')
    role = db.Column(db.String(30))

class Work_(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(50))
    abstract =db.Column(db.Text)
    time  = db.Column(db.String(20))
    
    company = db.Column(db.String(30))

class Article(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(50))
    body = db.Column(db.Text)
    category = db.relationship('Category', back_populates = 'articles')
    timestamp = db.Column(db.DateTime, default = datetime.utcnow, index = True)
    comment_open = db.Column(db.Boolean, default = True)
    count_read = db.Column(db.Integer)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    comments = db.relationship('Comment', back_populates = 'article', cascade = 'all, delete-orphan')
    

class Category(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(30), unique = True)
    articles = db.relationship('Article', back_populates = 'category')

    def delete(self):
        default = Category.query.get(1)
        articles = self.articles[:]
        for a in articles:
            a.category = default
        db.session.delete(self)
        db.session.commit()

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    person_post = db.Column(db.String(30))
    body = db.Column(db.Text)
    from_admin = db.Column(db.Boolean, default = False)
    reviewed = db.Column(db.Boolean, default = False)
    timestamp = db.Column(db.DateTime, default = datetime.utcnow, index = True)
    email = db.Column(db.String(255))
    site = db.Column(db.String(255))
    reply_id = db.Column(db.Integer, db.ForeignKey('comment.id'))
    article_id = db.Column(db.Integer, db.ForeignKey('article.id'))
    
    # to support comments to reply comments
    article = db.relationship('Article', back_populates = 'comments')
    replies = db.relationship('Comment', back_populates = 'replied', cascade = 'all, delete-orphan')
    replied = db.relationship('Comment', back_populates = 'replies', remote_side = [id])