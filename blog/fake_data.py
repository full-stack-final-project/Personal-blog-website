from faker import Faker 
from blog.extensions import db
from blog.models import Admin, Category, Comment, Article
from sqlalchemy.exc import IntegrityError

import random

fake = Faker()

# fake admin data
def fake_admin():
    admin = Admin(
        username = 'admin',
        name = fake.name(),
        about = 'This is my first personal blog which is created by Junhao and Yihua. \
                    I will share my stories and some articles in this blog.',
        site_title = name + "'s Personal blog"
    )
    admin.set_password('webdev')
    db.session.add(admin)
    db.session.commit()

# fake categories data
def fake_categories(count = 10):
    category = Category(name='Default') 
    db.session.add(category) 
    for i in range(count):
        category = Category(name = fake.work())
        db.session.add(category)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()

# fake articles data
def fake_articles(count = 100):
    for i in range(count):
        article = Article(
            title = fake.sentence(),
            body = fake.text(3000),
            category = Category.query.get(random.randint(1, Category.query.count())),
            timestamp = fake.data_time_this_year()
        )
        db.session.add(article)
    db.session.commit()

# fake comments data
def fake_comments(count = 300):
    # for reviewed comments
    for i in range(count):
        comment = Comment(
            person_post = fake.name(),
            body = fake.sentence(),
            reviewed = True,
            timestamp = fake.data_time_this_year(),
            email = fake.email(),
            site = fake.url(),
            article = Article.query.get(random.randint(1, Article.query.count()))
        )
        db.session.add(comment)

    # for unreviewed comments
    number = count * 0.2
    for i in range(number):
        comment = Comment(
            person_post = fake.name(),
            body = fake.sentence(),
            reviewed = False,
            timestamp = fake.data_time_this_year(),
            email = fake.email(),
            site = fake.url(),
            article = Article.query.get(random.randint(1, Article.query.count()))
        )
        db.session.add(comment)

        # for admin's comments
        comment = Comment(
            person_post = fake.name(),
            body = fake.sentence(),
            from_admin = True,
            reviewed = False,
            timestamp = fake.data_time_this_year(),
            email = fake.email(),
            site = fake.url(),
            article = Article.query.get(random.randint(1, Article.query.count()))
        )
        db.session.add(comment)
    db.session.commit()

    # for replied comments
    for i in range(number):
        comment = Comment(
            person_post = fake.name(),
            body = fake.sentence(),
            reviewed = True,
            timestamp = fake.data_time_this_year(),
            email = fake.email(),
            site = fake.url(),
            article = Article.query.get(random.randint(1, Article.query.count())),
            replied = Comment.query.get(random.randint(1, Comment.query.count()))
        )
        db.session.add(comment)
    db.session.commit()

    