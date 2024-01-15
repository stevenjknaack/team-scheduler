from flask import session, redirect, url_for
from functools import wraps

def login_required(f):
    """ Decorator for functions that require a logged in user """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session :
            return redirect(url_for('auth.login'))
        #', next=request.url' removed from example
        return f(*args, **kwargs)
    return decorated_function

def logout_required(f):
    """ Decorator for functions that require no user to be logged in """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' in session :
            return redirect(url_for('main.home'))
        #', next=request.url' removed from example
        return f(*args, **kwargs)
    return decorated_function

