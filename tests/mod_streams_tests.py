from tests.app_tests import BaseTestCase
from app.mod_streams.models import *
from flask import url_for

CHANNEL = 'channel'
CHANNELS = ['channel1', 'channel2', 'channel3']


class TestStreams(BaseTestCase):
    @classmethod
    def setUpClass(cls):
        cls.disable_login = True
        super().setUpClass()
        cls.url = url_for('adminpanel.configure_module', bp_name='streams')

    def add_streams(self, channels):
        if isinstance(channels, list):
            channels = ','.join(channels)
        return self.client.post(self.url, data=dict(
            channel=channels,
            add='Add'
        ))

    def remove_streams(self, channels):
        if isinstance(channels, list):
            channels = ','.join(channels)
        return self.client.post(self.url, data=dict(
            channel=channels,
            remove='Remove'
        ))

    def load_streams(self, channels):
        if isinstance(channels, list):
            channels = ','.join(channels)
        return self.client.post(self.url, data=dict(
            all_channels=channels,
            load='Load'
        ))

    def test_add(self):
        with self.client:
            # Test adding a single stream
            self.add_streams(CHANNEL)
            stream = Stream.query.filter_by(channel=CHANNEL).first()
            self.assertIsInstance(stream, Stream)
            self.assertEquals(stream.channel, CHANNEL)
            # Test adding an existing stream
            self.add_streams(CHANNEL)
            # Test adding multiple streams
            self.add_streams(CHANNELS)
            streams = Stream.query.filter(Stream.channel.in_(CHANNELS)).all()
            stream_names = []
            for stream in streams:
                stream_names.append(stream.channel)
                self.assertIsInstance(stream, Stream)
            self.assertEquals(set(stream_names), set(CHANNELS))
            # Test adding multiple existing streams
            self.add_streams(CHANNELS)
            # Test stream name requirement
            self.add_streams('')
            stream = Stream.query.filter_by(channel='').first()
            self.assertIsNone(stream)

    def test_remove(self):
        with self.client:
            # Test removing a stream
            self.add_streams(CHANNEL)
            self.remove_streams(CHANNEL)
            stream = Stream.query.filter_by(channel=CHANNEL).first()
            self.assertIsNone(stream)
            # Test removing multiple streams
            self.add_streams(CHANNELS)
            self.remove_streams(CHANNELS)
            streams = Stream.query.filter(Stream.channel.in_(CHANNELS)).all()
            self.assertEquals(streams, [])
            # Test removing non-existing stream
            self.remove_streams('kappa')
            # Test removing empty stream
            self.remove_streams('')

    def test_load(self):
        with self.client:
            # Test loading a stream
            self.add_streams(CHANNEL)
            rv = self.load_streams(CHANNEL)
            self.assertIn(CHANNEL.encode(), rv.data)
            # Test loading multiple streams
            self.add_streams(CHANNELS)
            rv = self.load_streams(CHANNELS)
            for channel in CHANNELS:
                self.assertIn(channel.encode(), rv.data)
