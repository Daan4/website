from flask import render_template, Blueprint

mod_nano = Blueprint('nano', __name__, url_prefix='/nano', template_folder='templates', static_folder='static')


@mod_nano.route('/overview')
def overview():
    return render_template('overview.html')

@mod_nano.route('/donate')
def donate():
    return render_template('donate.html')
