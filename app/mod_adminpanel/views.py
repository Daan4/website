from flask import Blueprint, request, render_template, flash,\
    g, session, redirect, url_for, abort
from app import app
from flask_login import login_required
import importlib

mod_adminpanel = Blueprint('adminpanel', __name__, url_prefix='/adminpanel', template_folder='templates')


@mod_adminpanel.route('/')
@login_required
def index():
    return render_template('adminpanel.html', title='Admin Panel', form=None)


@mod_adminpanel.route('/<bp_name>', methods=['GET', 'POST'])
@login_required
def configure_module(bp_name):
    # Check if a blueprint with the given name exists before continuing
    if bp_name not in app.blueprints.keys():
        abort(404)
    module_forms = importlib.import_module('app.mod_{}.forms'.format(bp_name))
    module_views = importlib.import_module('app.mod_{}.views'.format(bp_name))
    form = module_forms.ConfigForm()
    if form.validate_on_submit():
        module_views.do_config_logic(form)
    return render_template('{}_config.html'.format(bp_name), form=form)
