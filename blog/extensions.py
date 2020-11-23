from flask_sqlalchemy import SQLAlchemy 
from flask_wtf import CSRFProtect 
from flask_bootstrap import Bootstrap 


db = SQLAlchemy()
bootstrap = Bootstrap()
csrf = CSRFProtect()

