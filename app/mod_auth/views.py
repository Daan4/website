from flask import g, flash, redirect, url_for, request, render_template, Blueprint
from .forms import *
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

mod_auth = Blueprint('auth', __name__, url_prefix='/user', template_folder='templates',
                     static_folder='static')


@mod_auth.route('/login', methods=['GET', 'POST'])
def login():
    if user_is_logged_in():
        flash('User {} is already logged in'.format(g.user.username))
        return redirect(url_for('root.index'))
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remember_me = form.remember_me.data
        user = User.query.filter_by(username=username).first()
        if user is not None and check_password_hash(user.password, password):
            login_user(user, remember=remember_me)
            flash('User {} logged in'.format(username))
            next_view = request.args.get('next')
            if not next_view or next_view == '{}/logout'.format(mod_auth.url_prefix):
                return redirect(url_for('root.index'))
            else:
                return redirect(next_view)
        flash('Login failed: incorrect username or password entered')
    return render_template('login.html', title='Sign In', form=form)


@mod_auth.route('/logout')
@login_required
def logout():
    if user_is_logged_in():
        flash('User {} logged out.'.format(g.user.username))
        logout_user()
    else:
        flash('Logout failed: no user was logged in.')
    return redirect(url_for('root.index'))


@mod_auth.route('/signup', methods=['GET', 'POST'])
@login_required  # Don't allow new signups by default
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        User.create(username=form.username.data, password=generate_password_hash(form.password.data))
        return redirect(url_for('auth.login'))
    return render_template('signup.html', title='Sign Up', form=form)


@mod_auth.before_app_request
def before_request():
    g.user = current_user


def user_is_logged_in():
    return g.user is not None and g.user.is_authenticated
