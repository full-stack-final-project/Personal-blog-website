from flask import Blueprint
from flask_login import login_user, logout_user
from flask_login import login_requried, current_user
from forms import login_form
from models import Admin

authorization_buleprint = Blueprint('authorization', __name__)

@authorization_buleprint.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('blog.index'))

    form = login_form()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remember = form.remember.data

        administrator = Admin.query.first()
        if administrator:
            if username == administrator.username and administrator.validate_password(password):
                login_user(administrator, remember) 
                flash('This is your home!', 'success') 
                return redirect(url_for('blog.index'))
            flash('username or/and password is/are wrong!', 'warning')
        else:
            flash('No administrator now', 'warning')
    return render_template('authorization/login.html', form=form)

@authorization_buleprint.route('/logout')
def logout():
    logout_user()
    flash('Signed out', 'success')
    return redirect('blog.index')


