from flask import Blueprint

mod_adminpanel = None
registered_adminpanels = {}


def setup_module(app, nav_bar):
    # Register blueprint
    global mod_adminpanel
    mod_adminpanel = Blueprint('adminpanel', __name__, url_prefix='/adminpanel', template_folder='templates')
    app.register_blueprint(mod_adminpanel)
    # Set up navigation bar in adminpanel
    setup_navigation(app, app.nav)
    # Setup main menu bar items
    nav_bar.items.append(app.nav.Item('Admin Panel', 'adminpanel.index', constraints=[app.nav.Item.REQUIRELOGIN]))


# Sets up a navigation menu item for each module with mod_adminpanel integration.
def setup_navigation(app, nav):
    items = [nav.Item(x, 'adminpanel.configure_module', {'bp_name': x}) for x in registered_adminpanels]
    nav.Bar('adminpanel', items)
