from time import time
from app import db
from flask import render_template, g, request, session, url_for, Blueprint

mod_root = Blueprint('root', __name__, url_prefix='/')


@mod_root.route('/')
def index():
    return render_template('index.html')


@mod_root.before_request
def before_request():
    # Save current time to be used after the request to display the time the request took to complete.
    g.start_time = time()


# todo: error page back button always goes to base.index
@mod_root.after_request
def after_request(response):
    """ Replace the string __EXECUTION_TIME__ in the reponse with the actual
    execution time. """
    session['previous_page'] = request.url
    diff = round((time() - g.start_time) * 1000)
    execution_time_string = "1 millisecond" if diff == 1 else "{} milliseconds".format(diff)
    if response.response:
        try:
            response.response[0] = response.response[0].replace('__EXECUTION_TIME__'.encode('utf-8'), execution_time_string.encode('utf-8'))
            response.headers["content-length"] = len(response.response[0])
        except TypeError:
            # Response doesn't contain the text __EXECUTION_TIME__
            pass
    return response


def setup_error_handlers(app):
    @app.errorhandler(404)
    def not_found_error(error):
        try:
            redirect_url = session['previous_page']
        except KeyError:
            redirect_url = url_for('index')
        return render_template('404.html', title='404', redirect_url=redirect_url), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        try:
            redirect_url = session['previous_page']
        except KeyError:
            redirect_url = url_for('index')
        return render_template('500.html', title='500', redirect_url=redirect_url), 500
