from flask import Blueprint, request, render_template, flash,\
    g, session, redirect, url_for

mod_adminpanel = Blueprint('adminpanel', __name__, url_prefix='/adminpanel', template_folder='templates')


@mod_adminpanel.route('/', methods=['GET', 'POST'])
def index():
    return render_template('adminpanel.html')
