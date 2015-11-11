import time
from app import app, lm, db, nav
from flask import render_template, redirect, session, url_for, request, g, flash
from flask_login import login_user, logout_user, current_user, login_required,\
    user_logged_in, user_logged_out
from .forms import LoginForm
from .models import User


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated:
        flash('User {} is already logged in.'.format(g.user.username))
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remember_me = form.remember_me.data
        session['remember_me'] = remember_me
        user = User.query.filter_by(username=username).first()
        if user is not None and password == user.password:
            login_user(user, remember=remember_me)
            flash('User {} logged in.'.format(username))
            next_view = request.args.get('next')
            if not next_view or next_view == '/logout':
                return redirect(url_for('index'))
            else:
                return redirect(next_view)
        flash('Login failed: incorrect username or password entered.')
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
@login_required
def logout():
    if g.user is not None and g.user.is_authenticated:
        flash('User {} logged out.'.format(g.user.username))
        logout_user()
    else:
        flash('Logout failed: no user was logged in.')
    return redirect(url_for('index'))


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
    g.user = current_user
    g.start_time = time.time()


@app.after_request
def after_request(response):
    """ Replace the string __EXECUTION_TIME__ in the reponse with the actual
    execution time. """
    diff = round((time.time() - g.start_time) * 1000)
    execution_time_string = "1 millisecond" if diff == 1 else "{} milliseconds".format(diff)
    if response.response:
        try:
            response.response[0] = response.response[0].replace('__EXECUTION_TIME__'.encode('utf-8'), execution_time_string.encode('utf-8'))
            response.headers["content-length"] = len(response.response[0])
        except TypeError:
            # Response doesn't contain the text __EXECUTION_TIME__
            pass
    return response


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))
