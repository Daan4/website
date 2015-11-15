import json
import urllib.request
from urllib.error import URLError
from flask import current_app
from .models import *
# todo: stream api shouldnt import website_config directly
# todo: get api stream url from config

get_twitch_api_client_id = lambda: current_app.config['TWITCH_API_CLIENT_ID']
get_twitch_api_client_secret = lambda: current_app.config['TWITCH_API_CLIENT_SECRET']
get_twitch_api_stream_url = lambda: current_app.config['TWITCH_API_STREAM_URL']


def get_twitch_stream_object(channels):
    response = None
    channels_string = ','.join(channels)
    url = get_twitch_api_stream_url() + channels_string
    try:
        response = urllib.request.urlopen(url)
    except URLError as e:
        if hasattr(e, 'reason'):
            current_app.logger.exception('We failed to reach a server. Reason: {}'.format(e.reason))
        elif hasattr(e, 'code'):
            current_app.logger.exception('The server couldn\'t fulfill the request. Error code: {}'.format(e.code))

    return json.loads(response.read().decode('utf8'))


def update_stream_info():
    current_app.logger.info("Updating stream info.")
    stream_object = get_twitch_stream_object([x.channel for x in Stream.query.all()])
    online_streams_found = list()
    for stream in stream_object['streams']:
        online_streams_found.append(stream['channel']['name'])
    q = db.session.query(Stream).all()
    for record in q:
        if record.channel.lower() not in online_streams_found:
            record.is_online = False
        else:
            record.is_online = True
            for stream in stream_object['streams']:
                if stream['channel']['name'] == record.channel.lower():
                    record.game = stream['game']
                    record.viewers = stream['viewers']
                    break
    db.session.commit()
