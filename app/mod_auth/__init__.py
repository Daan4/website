from flask_login import LoginManager
from flask import Blueprint

mod_auth = None
lm = None


def setup_module(app, nav_bar):
    # Register blueprint
    global mod_auth
    mod_auth = Blueprint('auth', __name__, url_prefix='/user', template_folder='templates')
    app.register_blueprint(mod_auth)
    # Setup main menu bar items
    nav_bar.items.append(app.nav.Item('Log in', 'auth.login', constraints=[app.nav.Item.REQUIRELOGOUT]))
    nav_bar.items.append(app.nav.Item('Log out', 'auth.logout', constraints=[app.nav.Item.REQUIRELOGIN]))
    # Setup login manager
    global lm
    lm = LoginManager()
    lm.init_app(app)
    lm.login_view = 'auth.login'
