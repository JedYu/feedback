from functools import wraps
from flask import g, request, redirect, url_for
import hashlib
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user is None:
            print 'g.user', g.user
            return redirect(url_for('manage.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user is None:
            return "You are not login, man."
        if not g.user.is_admin :
            return "You are not admin, man."
        return f(*args, **kwargs)
    return decorated_function


def get_encrypt_passwd(p):
    md5 = hashlib.md5()
    md5.update(p)
    e1 = md5.hexdigest()
    md5.update("/")
    md5.update(e1)
    return md5.hexdigest()


