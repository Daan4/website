from .views import mod_projects
from app import register_module


@register_module()
def setup_module(app, nav, nav_bar):
    # Register blueprint
    app.register_blueprint(mod_projects)
    # Setup main menu bar items
    nav_bar.items.append(nav.Item('Projects', 'projects.index'))
