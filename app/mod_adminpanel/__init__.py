from .views import registered_adminpanels


def setup_module(app, nav, nav_bar):
    # Set up navigation bar in adminpanel
    setup_navigation(app, nav)
    # Add navigation bar item to the main navigation bar
    nav_bar.items.append(nav.Item('Admin Panel', 'adminpanel.index', constraints=[nav.Item.REQUIRELOGIN]))


# Sets up a navigation menu item for each module with mod_adminpanel integration.
def setup_navigation(app, nav):
    items = [nav.Item(x, 'adminpanel.configure_module', {'bp_name': x}) for x in registered_adminpanels]
    nav.Bar('adminpanel', items)
