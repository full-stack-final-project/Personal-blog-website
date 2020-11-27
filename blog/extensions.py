from flask_sqlalchemy import SQLAlchemy 
from flask_wtf import CSRFProtect 
from flask_bootstrap import Bootstrap 
from flask_ckeditor import CKEditor 
from flask_login import LoginManager
from flask_moment import Moment 
from flask_mail import Mail



ckeditor = CKEditor()
db = SQLAlchemy()
bootstrap = Bootstrap()
csrf = CSRFProtect()
mail = Mail()
moment = Moment()
login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    from blog.models import Admin
    user = Admin.query.get(int(user_id))
    return user