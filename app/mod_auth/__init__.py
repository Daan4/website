from .views import mod_auth
from flask_login import LoginManager


def setup_module(app, nav_bar):
    # Register blueprint
    app.register_blueprint(mod_auth)
    # Setup main menu bar items
    nav_bar.items.append(app.nav.Item('Log in', 'auth.login', constraints=[app.nav.Item.REQUIRELOGOUT]))
    nav_bar.items.append(app.nav.Item('Log out', 'auth.logout', constraints=[app.nav.Item.REQUIRELOGIN]))
    # Setup login manager
    lm = LoginManager()
    lm.init_app(app)
    lm.login_view = 'auth.login'
