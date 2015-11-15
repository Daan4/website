from flask_login import LoginManager
from .views import mod_auth

lm = None


def setup_module(app, nav, nav_bar):
    # Register blueprint
    app.register_blueprint(mod_auth)
    # Setup main menu bar items
    nav_bar.items.append(nav.Item('Log in', 'auth.login', constraints=[nav.Item.REQUIRELOGOUT]))
    nav_bar.items.append(nav.Item('Log out', 'auth.logout', constraints=[nav.Item.REQUIRELOGIN]))
    # Setup login manager
    global lm
    lm = LoginManager()
    lm.init_app(app)
    lm.login_view = 'auth.login'
