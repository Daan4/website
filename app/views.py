from time import time
from app import app, db
from flask import render_template, g


@app.route('/')
def index():
    return render_template('index.html')


@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html', title='404'), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html', title='500'), 500


@app.before_request
def before_request():
    # Save current time to be used after the request to display the time the request took to complete.
    g.start_time = time()


@app.after_request
def after_request(response):
    """ Replace the string __EXECUTION_TIME__ in the reponse with the actual
    execution time. """
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
