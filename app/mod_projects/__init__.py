from flask import Blueprint

mod_projects = None


def setup_module(app, nav_bar):
    # Register blueprint
    global mod_projects
    mod_projects = Blueprint('projects', __name__, url_prefix='/projects', template_folder='templates')
    app.register_blueprint(mod_projects)
    # Setup main menu bar items
    nav_bar.items.append(app.nav.Item('Projects', 'projects.index'))
