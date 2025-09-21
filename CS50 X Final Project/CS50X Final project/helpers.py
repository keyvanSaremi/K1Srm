from functools import wraps
from flask import session, redirect
from werkzeug.security import generate_password_hash, check_password_hash

# Decorator برای صفحات نیازمند ورود
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

# رمزگذاری و بررسی رمز
def hash_password(password):
    return generate_password_hash(password)

def check_password(hash, password):
    return check_password_hash(hash, password)
