from flask import Blueprint, request, render_template, flash,\
    g, session, redirect, url_for
from flask_login import login_required

mod_adminpanel = Blueprint('adminpanel', __name__, url_prefix='/adminpanel', template_folder='templates')


@mod_adminpanel.route('/')
@login_required
def index():
    return render_template('adminpanel.html', title='Admin Panel')


@mod_adminpanel.route('/<config_name>', methods=['GET', 'POST'])
@login_required
def configure_module(config_name):
    return redirect(url_for('{}.adminpanel'.format(config_name)))
