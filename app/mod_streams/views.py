from flask import Blueprint, request, render_template, flash,\
    g, session, redirect, url_for
from app import db
from app.mod_streams.models import Stream
from app.mod_streams import stream_api

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
