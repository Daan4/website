from flask import Blueprint, request, render_template, flash, session
from app import db
from sqlalchemy.exc import IntegrityError, InvalidRequestError
from sqlalchemy.orm.exc import UnmappedInstanceError
from app.mod_streams.models import Stream
from app.mod_streams import stream_api
from .forms import ConfigForm

mod_streams = Blueprint('streams', __name__, url_prefix='/streams', template_folder='templates')


@mod_streams.route('/', methods=['GET', 'POST'])
def index():
    all_streams = Stream.query.order_by(Stream.is_online.desc(),
                                        Stream.viewers.desc()).all()
    active_stream = None
    if request.method == 'POST':
        active_stream = request.form['submit']
        session['chat_enabled'] = request.form.getlist('enable_chat')
        if active_stream == 'Refresh':
            active_stream = None
            stream_api.update_stream_info(auto_update=False)
            flash("Stream info refreshed!")
    return render_template('streams.html',
                           title='Streams',
                           streams=all_streams,
                           active_stream=active_stream)


# Used by mod_adminpanel module to do configuration form logic.
def do_config_form_logic(form):
    channels = []
    if form.channel.data:
        channels = form.channel.data.split(',')
    if form.add.data:
        for channel in channels:
            stream = Stream(channel=channel)
            try:
                db.session.add(stream)
                db.session.commit()
                flash('Channel {} added'.format(channel))
            except (IntegrityError, InvalidRequestError):
                flash('Channel {} already exists in the database'.format(channel))
    elif form.remove.data:
        for channel in channels:
            stream = Stream.query.filter_by(channel=channel).first()
            try:
                db.session.delete(stream)
                db.session.commit()
                flash('Channel {} removed.'.format(channel))
            except UnmappedInstanceError:
                flash('Channel {} doesn\'t exist in the database'.format(channel))
