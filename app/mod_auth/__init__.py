from flask_login import LoginManager
from flask import Blueprint
from .models import User

mod_auth = None
lm = None


def setup_module(app, nav, nav_bar):
    # Register blueprint
    global mod_auth
    mod_auth = Blueprint('auth', __name__, url_prefix='/user', template_folder='templates')
    app.register_blueprint(mod_auth)
    # Setup main menu bar items
    nav_bar.items.append(nav.Item('Log in', 'auth.login', constraints=[nav.Item.REQUIRELOGOUT]))
    nav_bar.items.append(nav.Item('Log out', 'auth.logout', constraints=[nav.Item.REQUIRELOGIN]))
    # Setup login manager
    global lm
    lm = LoginManager()
    lm.init_app(app)
    lm.login_view = 'auth.login'

    @lm.user_loader
    def load_user(id_):
        return User.query.get(int(id_))
