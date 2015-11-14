from importlib import import_module


def setup_module(app, nav, nav_bar):
    # Set up navigation bar in adminpanel
    setup_navigation(app, nav)
    # Add navigation bar item to the main navigation bar
    nav_bar.items.append(nav.Item('Admin Panel', 'adminpanel.index', constraints=[nav.Item.REQUIRELOGIN]))


# Sets up a navigation menu item for each module with mod_adminpanel integration.
def setup_navigation(app, nav):
    items_to_add = []
    for name, blueprint in app.blueprints.items():
        module = import_module(blueprint.import_name)
        # Check if blueprint has a form named ConfigForm.
        # Check if blueprint has a function named do_config_form_logic.
        # If both of those are implemented then the module should have an adminpanel page.
        try:
            module.do_config_logic
        except AttributeError as e:
            continue
        items_to_add.append(name)

    # Create navigation bar
    items = [nav.Item(x, 'adminpanel.configure_module', {'bp_name': x}) for x in items_to_add]
    nav.Bar('adminpanel', items)
