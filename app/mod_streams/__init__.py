from flask import Blueprint

mod_streams = None


def setup_module(app, nav, nav_bar):
    # Register blueprint
    global mod_streams
    mod_streams = Blueprint('streams', __name__, url_prefix='/streams', template_folder='templates')
    app.register_blueprint(mod_streams)
    # Setup main menu bar items
    nav_bar.items.append(nav.Item('Streams', 'streams.index'))
