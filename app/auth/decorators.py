"""
Decorators for authentication and authorization
"""
from flask import session, redirect, url_for
from functools import wraps

# authentication decorators
def login_required(f):
    """ Decorator for functions that require a logged in user """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session :
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def logout_required(f):
    """ Decorator for functions that require no user to be logged in """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' in session :
            return redirect(url_for('main.home'))
        return f(*args, **kwargs)
    return decorated_function

