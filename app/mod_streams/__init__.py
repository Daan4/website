from .views import mod_streams


def setup_module(app, nav, nav_bar):
    # Register blueprint
    app.register_blueprint(mod_streams)
    # Setup main menu bar items
    nav_bar.items.append(nav.Item('Streams', 'streams.index'))
