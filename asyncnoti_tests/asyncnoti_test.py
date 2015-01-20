import unittest
import mock
from nose.tools import *

import sys

sys.path.append("../")
from asyncnoti import Asyncnoti
from asyncnoti.util import AsyncnotiException


class PropertiesTest(unittest.TestCase):
    def test_instance_app_id(self):
        eq_(obj().app_id, '123')

    def test_instance_key(self):
        eq_(obj().app_key, 'key123')

    def test_instance_secret(self):
        eq_(obj().app_secret, 'secret123')


class InstanceParamsTest(unittest.TestCase):
    @raises(TypeError)
    def test_with_bad_key(self):
        Asyncnoti(123)

    @raises(TypeError)
    def test_with_bad_secret(self):
        Asyncnoti(u'key', 5134)

    @raises(TypeError)
    def test_with_bad_app_id(self):
        Asyncnoti(u'key', u'secret', 123)

    @raises(TypeError)
    def test_with_bad_hostname(self):
        Asyncnoti(u'key', u'secret', '1156', 4532)

    @raises(TypeError)
    def test_with_bad_port(self):
        Asyncnoti(u'key', u'secret', '1156', 'http://hostname', 'port')


class RequestTest(unittest.TestCase):
    @mock.patch('asyncnoti.Asyncnoti._request')
    def test_trigger_method(self, _request):
        _request.return_value = 200, {}
        trigger()
        _request.assert_called_once_with('/api/v1/apps/123/events', 'POST', {'channels': ('channel1',), 'data': '{}',
                                                                             'data_hash': '44136fa355b3678a1146ad16f7e8649e94fb4fc21fe77e8310c060f61caaff8a',
                                                                             'name': 'event1'})

    @mock.patch('time.time')
    @mock.patch('asyncnoti.Asyncnoti._http_request')
    def test_request_method(self, http_request_mock, time_mock):
        time_mock.return_value = 1421420862
        http_request_mock.return_value = 200, {}
        response = trigger()

        http_request_mock.assert_called_once_with('POST', '/api/v1/apps/123/events', {
        'data_hash': '44136fa355b3678a1146ad16f7e8649e94fb4fc21fe77e8310c060f61caaff8a',
        'auth_signature': u'6a5f929fb5a80ba7f7e7f19664b7ba1a5a02adf245bf0f79cef767d8c0c1ed34', 'name': 'event1',
        'auth_key': u'key123', 'channels': ('channel1',), 'data': '{}', 'auth_timestamp': '1421420862'})

        eq_(response, {})

    @raises(Exception)
    @mock.patch('asyncnoti.Asyncnoti._http_request')
    def t1est_request_error(self, http_request_mock):
        http_request_mock.return_value = 405, {}
        trigger()

    @mock.patch('asyncnoti.Asyncnoti._http_request')
    def test_request_error2(self, http_request_mock):
        http_request_mock.return_value = 405, {}

        try:
            trigger()
            assert False
        except AsyncnotiException as e:
            assert e.code is 405

    @raises(Exception)
    @mock.patch('six.moves.http_client.HTTPConnection.request')
    def test_http_request_error(self, http_connection_request_mock):
        http_connection_request_mock.return_value = 'dd'
        trigger()


class ResponsesTest(unittest.TestCase):
    def test_trigger_method_with_404_error(self):
        # TODO
        pass

    def test_trigger_method_with_401_error(self):
        # TODO
        pass

    def test_trigger_method_with_400_error(self):
        # TODO
        pass


def obj():
    return Asyncnoti(app_key=u'key123', app_id=u'123', app_secret=u'secret123')


def trigger():
    return obj().trigger(u'channel1', u'event1')