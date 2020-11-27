from flask import Blueprint
from flask_login import login_user, logout_user
from flask_login import login_required, current_user
from blog.forms import login_form
from blog.models import Admin
from flask import render_template
from flask import flash, redirect, url_for
from blog.views.management import redirect_to_last_page

authorization_buleprint = Blueprint('authorization', __name__)

@authorization_buleprint.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect_to_last_page()
    form = login_form()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remember = form.remember.data

        administrator = Admin.query.first()
        if administrator:
            if username == administrator.username and administrator.check_password(password):
                login_user(administrator, remember) 
                flash('This is your home!', 'success') 
                return redirect_to_last_page()
            flash('username or/and password is/are wrong!', 'warning')
        else:
            flash('No administrator now', 'warning')
    return render_template('authorization/login.html', form=form)

@authorization_buleprint.route('/logout')
def logout():
    logout_user()
    flash('Signed out', 'success')
    return redirect(url_for('blog.index'))


