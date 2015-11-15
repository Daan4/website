from flask import Blueprint, request, render_template, flash, session
from app import db
from sqlalchemy.exc import IntegrityError, InvalidRequestError
from sqlalchemy.orm.exc import UnmappedInstanceError
from app.mod_streams.models import Stream
from app.mod_streams import stream_api
from .forms import ConfigForm
from app.mod_adminpanel.views import register_adminpanel

mod_streams = Blueprint('streams', __name__, url_prefix='/streams', template_folder='templates',
                        static_folder='static')


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


@register_adminpanel(mod_streams.name)
def do_adminpanel_logic():
    config_form = ConfigForm()
    # Drop down list shows all channels.
    all_streams = Stream.query.all()
    config_form.all_channels.choices = [(s.channel, s.channel) for s in all_streams]
    if config_form.validate_on_submit():
        channels = []
        selected_channels = config_form.all_channels.data
        if config_form.channel.data:
            channels = config_form.channel.data.split(',')
        if config_form.add.data:
            add_streams(channels, config_form)
        elif config_form.remove.data:
            delete_streams(channels, config_form)
        elif config_form.load.data:
            if selected_channels:
                load_stream(selected_channels, config_form)
    return render_template('streams_config.html', config_form=config_form, title='Admin Panel - Streams')


def add_streams(channels, form):
    for channel in channels:
        stream = Stream(channel=channel)
        try:
            db.session.add(stream)
            db.session.commit()
            # Add newly added channel to the drop-down selection list.
            form.all_channels.choices.append((stream.channel, stream.channel))
            flash('Channel {} added'.format(channel))
        except (IntegrityError, InvalidRequestError):
            flash('Channel {} already exists in the database'.format(channel))


def delete_streams(channels, form):
    for channel in channels:
        stream = Stream.query.filter_by(channel=channel).first()
        try:
            db.session.delete(stream)
            db.session.commit()
            form.all_channels.choices.remove((stream.channel, stream.channel))
            flash('Channel {} removed'.format(channel))
        except UnmappedInstanceError:
            flash('Channel {} doesn\'t exist in the database'.format(channel))


def load_stream(channels, form):
    streams = Stream.query.filter(Stream.channel.in_(channels)).all()
    form.channel.data = ','.join([s.channel for s in streams])
    for stream in streams:
        flash('Stream {} loaded'.format(stream.channel))