from time import time
from app import db
from flask import render_template, g, request, session, url_for, Blueprint, redirect, current_app

mod_root = Blueprint('root', __name__, url_prefix='/')


@mod_root.route('/')
def index():
    return render_template('index.html')


@mod_root.before_app_request
def before_request():
    # Save current time to be used after the request to display the time the request took to complete.
    g.start_time = time()
    # Redirect to https when not running in debug mode
    if not current_app.debug and not request.is_secure:
        url = request.url.replace('http://', 'https://')
        code = 301
        return redirect(url, code=code)


@mod_root.after_app_request
def after_request(response):
    # Track previously visited url
    session['previous_url'] = request.referrer
    # Replace __EXECUTION_TIME__ string in the response with the actual execution time.
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
            redirect_url = session['previous_url']
        except KeyError:
            redirect_url = url_for('root.index')
        return render_template('404.html', title='404', redirect_url=redirect_url), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        try:
            redirect_url = session['previous_url']
        except KeyError:
            redirect_url = url_for('root.index')
        return render_template('500.html', title='500', redirect_url=redirect_url), 500
