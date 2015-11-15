from flask import render_template, abort, Blueprint
from flask_login import login_required

mod_adminpanel = Blueprint('adminpanel', __name__, url_prefix='/adminpanel', template_folder='templates')
registered_adminpanels = {}


@mod_adminpanel.route('/')
@login_required
def index():
    return render_template('adminpanel.html', title='Admin Panel', form=None)


@mod_adminpanel.route('/<bp_name>', methods=['GET', 'POST'])
@login_required
def configure_module(bp_name):
    try:
        return registered_adminpanels[bp_name]()
    except KeyError:
        abort(404)


def register_adminpanel(bp_name):
    """ Decorator used to register a function as the function to be
        called to render the blueprint's adminpanel page.
    """
    def decorator(f):
        registered_adminpanels[bp_name] = f
        return f
    return decorator
