from faker import Faker 
from blog.extensions import db
from blog.models import Admin, Category, Comment, Article, Bio, Skill, Project, Work_
from sqlalchemy.exc import IntegrityError


import random

fake = Faker()

# fake admin data
def fake_admin():
    admin = Admin(
        username = 'admin',
        name = 'Jason',
        about = 'This is my first personal blog which is created by Junhao and Yihua. \
                    I will share my stories and some articles in this blog.',
        site_title = "Jason's Personal blog"
    )
    admin.set_password('fullstack')
    db.session.add(admin)
    db.session.commit()

    bio = Bio(
        name = 'Jason Gale',
        intro = 'Donec quam felis, ultricies nec, pellentesque eu. \
             Lorem ipsum dolor sit amet, consectetuer adipiscing elit. \
                  Aenean commodo ligula eget dolor. Aenean massa. \
                      Cum sociis natoque penatibus et magnis dis parturient montes, \
                          nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem.\
                               Maecenas nec odio et ante tincidunt tempus.\
                           Donec vitae sapien ut libero venenatis faucibus.\
                                Nullam quis ante. Etiam sit amet orci eget eros faucibus tincidunt. Duis leo. Sed fringilla mauris sit amet nibh.',
        current_job = 'Software Engineer'


    )

    db.session.add(bio)
    db.session.commit()

    work = Work_(
        title = 'Senior Software Engineer',
        abstract = 'Role description goes here ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa.\
             Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Donec pede justo,\
             fringilla vel. Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. \
                 Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis.',
        time = '2018-present',
        company = 'Google'
    )
    db.session.add(work)
    db.session.commit()

    project = Project(
        title = 'Senior Software Engineer',
        abstract = 'Role description goes here ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa.\
             Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Donec pede justo,\
             fringilla vel. Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. \
                 Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis.',
        
        role = 'Leader'
    )
    db.session.add(project)
    db.session.commit()

    skill_1 = Skill(
        content = 'JavaScript/Angular/React/Vue',
        is_techical = True
    )
    skill_2 = Skill(
        content = 'Python/Ruby/PHP',
        is_techical = True
    )
    skill_3 = Skill(
        content = 'Effective communication',
        is_techical = False
    )

    db.session.add(skill_1)
    db.session.add(skill_2)
    db.session.add(skill_3)
    db.session.commit()


    

    



# fake categories data
def fake_categories(count = 10):
    category = Category(name='Default') 
    db.session.add(category) 
    for i in range(count):
        category = Category(name = fake.word())
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
            timestamp = fake.date_time_this_year(),
            count_read = random.randint(1,10000)
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
            timestamp = fake.date_time_this_year(),
            email = fake.email(),
            site = fake.url(),
            article = Article.query.get(random.randint(1, Article.query.count()))
        )
        db.session.add(comment)

    # for unreviewed comments
    number = int(count * 0.2)
    for i in range(number):
        comment = Comment(
            person_post = fake.name(),
            body = fake.sentence(),
            reviewed = False,
            timestamp = fake.date_time_this_year(),
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
            reviewed = True,
            timestamp = fake.date_time_this_year(),
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
            timestamp = fake.date_time_this_year(),
            email = fake.email(),
            site = fake.url(),
            article = Article.query.get(random.randint(1, Article.query.count())),
            replied = Comment.query.get(random.randint(1, Comment.query.count()))
        )
        db.session.add(comment)
    db.session.commit()

    