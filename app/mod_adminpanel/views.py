from flask import Blueprint, render_template, abort, redirect, url_for, flash
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
    module = None
    for name, blueprint in app.blueprints.items():
        if name == bp_name:
            module = importlib.import_module(blueprint.import_name)
            break
    else:
        abort(404)
    try:
        render_template_kwargs = module.do_config_logic()
        return render_template('{}_config.html'.format(bp_name), **render_template_kwargs)
        # form = module.ConfigForm()
        # if form.validate_on_submit():
        #     render_template_kwargs = module.do_config_form_logic(form)
        # return render_template('{}_config.html'.format(bp_name), form=form)
    except AttributeError as e:
        # The module has no ConfigForm form or do_config_form_logic function
        abort(404)
