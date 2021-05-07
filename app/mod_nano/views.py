from flask import render_template, Blueprint, current_app, redirect
import urllib.request


mod_nano = Blueprint('nano', __name__, url_prefix='/nano', template_folder='templates', static_folder='static')


@mod_nano.route('/overview')
def overview():
    return render_template('overview.html')


@mod_nano.route('/donate')
def donate():
    return render_template('donate.html')


@mod_nano.route('/monitor')
def monitor():
    return redirect('http://' + current_app.config['NANO_NODE_IP'])
