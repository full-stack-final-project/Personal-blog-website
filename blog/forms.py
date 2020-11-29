from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, TextAreaField, ValidationError, HiddenField
from wtforms.validators import DataRequired, Length, Email, Optional, URL
from flask_ckeditor import CKEditorField
from blog.models import Category

class login_form(FlaskForm):
    username = StringField('Username', validators = [DataRequired(), Length(1, 30)])
    password = PasswordField('Password', validators = [DataRequired(), Length(8, 128)])
    remember = BooleanField('Remember me')
    submit = SubmitField('Log in')

class article_form(FlaskForm):
    title = StringField('Title', validators = [DataRequired(), Length(1, 50)])
    category = SelectField('Category', coerce = int, default = 1)
    body = CKEditorField('Body', validators = [DataRequired()])
    submit = SubmitField()

    def __init__(self, *args, **kwargs):
        super(article_form, self).__init__(*args, **kwargs)
        self.category.choices = [(category.id, category.name) 
                                for category in Category.query.order_by(Category.name).all()]

class category_form(FlaskForm):
    name = StringField('Name', validators = [DataRequired(), Length(1, 30)])
    submit = SubmitField()

    # In category database model, name is unique
    def validate_name(self, field):
        if Category.query.filter_by(name = field.data).first():
            raise ValidationError('This name has been used!!!')

class comment_form(FlaskForm):
    person_post = StringField('Name', validators = [DataRequired(), Length(1, 30)])
    email = StringField('Email', validators = [DataRequired(), Email(), Length(1, 255)])
    site = StringField('Site', validators = [Optional(), URL(), Length(0, 255)])
    body = TextAreaField('Comment', validators = [DataRequired()])
    submit = SubmitField()

class admin_comment_form(comment_form):
    author = HiddenField()
    email = HiddenField()
    site = HiddenField()

class bio_form(FlaskForm):
    name = StringField('Name', validators = [DataRequired(), Length(1, 30)])
    current_job = StringField('Current Job Title', validators = [DataRequired(), Length(1, 30)])
    body = CKEditorField('Introduction', validators = [DataRequired()])
    submit = SubmitField()

class work_form(FlaskForm):
    title = StringField('Job Title', validators = [DataRequired(), Length(1,30)])
    company = StringField('Company', validators = [DataRequired(), Length(1,30)])
    time = StringField('yyyy - yyyy', validators=[DataRequired(), Length(1,30)])
    body = CKEditorField('Abstract', validators = [DataRequired()])
    submit = SubmitField()

class project_form(FlaskForm):
    title = StringField('Project Name', validators = [DataRequired(), Length(1,30)])
    role = StringField('Role', validators = [DataRequired(), Length(1,30)])
    body = CKEditorField('Abstract', validators = [DataRequired()])
    submit = SubmitField()

class skill_form(FlaskForm):
    content = StringField('Your Skill', validators = [DataRequired(), Length(1,50)])
    techical = BooleanField('Is techical skill?')
    submit = SubmitField()


