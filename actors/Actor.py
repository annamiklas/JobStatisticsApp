from functools import wraps

from flask import redirect, session


class Actor:
    sess_key = ""
    route_url = "/"

    def login_required(self, f, path="login"):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if self.sess_key not in session or session[self.sess_key] is None:
                print(path)
                return redirect(self.route_url + path)
            return f(*args, **kwargs)

        return decorated_function

    def redirect_if_login(self, f, path="dashboard"):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if self.sess_key in session and session[self.sess_key] is not None:
                return redirect(self.route_url + path)
            return f(*args, **kwargs)

        return decorated_function

    def logout(self):
        session[self.sess_key] = None
