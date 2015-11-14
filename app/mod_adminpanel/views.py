from flask import Blueprint, render_template, abort, redirect, url_for, flash
from app import app
from flask_login import login_required
import importlib

mod_adminpanel = Blueprint('adminpanel', __name__, url_prefix='/adminpanel', template_folder='templates')
registered_blueprints = {}


@mod_adminpanel.route('/')
@login_required
def index():
    return render_template('adminpanel.html', title='Admin Panel', form=None)


@mod_adminpanel.route('/<bp_name>', methods=['GET', 'POST'])
@login_required
def configure_module(bp_name):
    render_template_kwargs = {}
    try:
        render_template_kwargs = registered_blueprints[bp_name]()
        return render_template('{}_config.html'.format(bp_name), **render_template_kwargs)
    except KeyError:
        abort(404)


def register_adminpanel(blueprint_name):
    """ Decorator used to register a function as the function to be
        called to generate the kwargs for its blueprint's mod_config.html page.
    """
    def decorator(f):
        registered_blueprints[blueprint_name] = f
        return f
    return decorator
