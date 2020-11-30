import os

root = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

class BaseConfig(object):
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev_key')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    CKEDITOR_ENABLE_CSRF = True
    CKEDITOR_FILE_UPLOADER = 'management.upload_image'
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USE_TLS = False
    MAIL_USERNAME = 'fullblogtest@gmail.com'
    MAIL_PASSWORD = 'fullstack'
    MAIL_DEFAULT_SENDER = ('fullblogtest@gmail.com', MAIL_USERNAME)

    ARTICLE_PER_PAGE = 9
    MANAGE_ARTICLE_PER_PAGE = 10
    MANAGE_COMMENT_PER_PAGE = 20

    ELIGIBLE_IMAGE = ['jpg', 'jpeg', 'png', 'gif']
    ELIGIBLE_FILE = ['pdf']

    UPLOAD_PATH = os.path.join(root, 'blog/static/uploads')

class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'sqlite:////' + os.path.join(root, 'dev.db')

class TestConfig(BaseConfig):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    
class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.getenv('DB_URI', 'sqlite:////' + os.path.join(root, 'dev.db'))
    
config = {
    'development': DevelopmentConfig,
    'testing': TestConfig,
    'production': ProductionConfig
}