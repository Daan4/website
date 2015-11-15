import json
import threading
import urllib.request
from urllib.error import URLError

from app import app, db
from app.mod_streams.models import Stream
# todo: stream api shouldnt import website_config directly
# todo: get api stream url from config
from config import website_config as c

TWITCH_API_CLIENT_ID = c.TWITCH_API_CLIENT_ID
TWITCH_API_CLIENT_SECRET = c.TWITCH_API_CLIENT_SECRET
TWITCH_API_STREAM_URL = 'https://api.twitch.tv/kraken/streams/?channel='


def get_twitch_stream_object(channels):
    response = None
    channels_string = ','.join(channels)
    url = TWITCH_API_STREAM_URL + channels_string
    try:
        response = urllib.request.urlopen(url)
    except URLError as e:
        if hasattr(e, 'reason'):
            app.logger.exception('We failed to reach a server. Reason: {}'.format(e.reason))
        elif hasattr(e, 'code'):
            app.logger.exception('The server couldn\'t fulfill the request. Error code: {}'.format(e.code))

    return json.loads(response.read().decode('utf8'))


def update_stream_info(auto_update=True):
    app.logger.info("Updating stream info.")
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
