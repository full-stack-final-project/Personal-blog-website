from flask import Blueprint

authorization_buleprint = Blueprint('authorization', __name__)

@authorization_buleprint.route('/login', methods=['GET', 'POST'])
def login():
    return 'This should be a login webpage!!!'


@authorization_buleprint.route('/logout')
def logout():
    return 'Logout webpage'


