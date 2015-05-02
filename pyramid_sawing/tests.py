# -*- coding: utf-8 -*-
# ###
# Copyright (c) 2015, Rice University
# This software is subject to the provisions of the GNU Affero General
# Public License version 3 (AGPLv3).
# See LICENCE.txt for details.
# ###
import os
import io
import logging
import socket
import unittest
from tempfile import mkstemp
from wsgiref.util import request_uri
try:
    from unittest import mock
except ImportError:
    import mock

from pyramid import testing
from pyramid.request import Request


class UtilsTests(unittest.TestCase):

    def test_local_settings(self):
        prefix = 'xyz'
        settings = {
            '{}.foo'.format(prefix): 'bar',
            '{}.bar'.format(prefix): 'foo',
            'oof': 'arb',
            }
        expected = {
            'foo': 'bar',
            'bar': 'foo',
            }
        # Test the utility...
        from .utils import local_settings
        self.assertEqual(expected, local_settings(settings, prefix))


CONFIG = """\
version: 1

formatters:
  generic:
    format    : '%(levelname)-5.5s;.;%(message)s'
  contextualized:
    # filters : [context]
    format    : '%(levelname)-5.5s;.;%(hostname)s;.;%(message)s'
  apache_style:
    # filters : [environ]
    format    : '%(REMOTE_ADDR)s - %(REMOTE_USER)s [asctime] "%(REQUEST_METHOD)s %(REQUEST_URI)s %(HTTP_VERSION)s" %(status)s %(bytes)s "%(HTTP_REFERER)s" "%(HTTP_USER_AGENT)s"'
    datefmt   : '%d/%b/%Y:%H:%M:%S'
filters:
  context:
    ()        : pyramid_sawing.filters.ContextFilter
  environ:
    ()        : pyramid_sawing.filters.EnvironFilter
handlers:
  logio:
    class     : logging.StreamHandler
    level     : INFO
    formatter : generic
    stream    : 'ext://pyramid_sawing.tests.logio'
  logio_with_context:
    class     : logging.StreamHandler
    level     : INFO
    formatter : contextualized
    filters   : [context]
    stream    : 'ext://pyramid_sawing.tests.logio'
  logio_for_transit:
    class     : logging.StreamHandler
    formatter : apache_style
    stream    : 'ext://pyramid_sawing.tests.logio'
  console:
    class     : logging.StreamHandler
    formatter : apache_style
    filters   : [context, environ]
    stream    : 'ext://sys.stdout'
loggers:
  pyramid_sawing.tests:
    level     : INFO
    handlers  : [logio_with_context]
    propagate : 0
  my_transit_logger:
    handlers  : [logio_for_transit]
    propagate : 0
root:
  level       : NOTSET
  handlers    : [logio]
"""
logio = io.BytesIO()


class IncludePluginTestCase(unittest.TestCase):

    def setUp(self):
        # Put the config somewhere.
        self.logging_config_filepath = mkstemp()[1]
        with open(self.logging_config_filepath, 'w') as f:
            f.write(CONFIG)
        # Settings...
        self.settings = {
            'pyramid_sawing.file': self.logging_config_filepath,
            }
        self.addCleanup(os.remove, self.logging_config_filepath)

        global logio
        self.logio_position = logio.tell()

    def test_logging(self):
        """Test that the includeme function loads the logging config."""
        from .main import includeme
        with testing.testConfig(settings=self.settings) as config:
            includeme(config)

        # Set up the loggers
        root = logging.getLogger()
        local = logging.getLogger('pyramid_sawing.tests')

        # Try logging...
        root_log_msg = 'O.o'
        root.error(root_log_msg)
        local_log_msg = '>,<'
        local.info(local_log_msg)

        global logio
        logio.seek(self.logio_position)
        log_lines = logio.read().split('\n')
        self.assertEqual(len(log_lines), 3)

        # Check the root message...
        parsed_root_msg = log_lines[0].split(';.;')
        self.assertEqual(parsed_root_msg, ['ERROR', root_log_msg])
        parsed_local_msg = log_lines[1].split(';.;')
        self.assertEqual(parsed_local_msg,
                         ['INFO ', socket.gethostname(), local_log_msg])


class TransitLoggingTestCase(unittest.TestCase):

    def setUp(self):
        # Put the config somewhere.
        self.logging_config_filepath = mkstemp()[1]
        with open(self.logging_config_filepath, 'w') as f:
            f.write(CONFIG)
        # Settings...
        self.settings = {
            'pyramid_sawing.file': self.logging_config_filepath,
            'pyramid_sawing.transit_logging.logger_name': 'my_transit_logger',
            }
        self.addCleanup(os.remove, self.logging_config_filepath)

        global logio
        self.logio_position = logio.tell()

    @property
    def target(self):
        from .main import TransitLogger
        return TransitLogger

    def make_one(self, handler=None, registry=None):
        if handler is None:
            handler = mock.Mock()
        if registry is None:
            registry = mock.Mock()
            registry.settings = self.settings
        return self.target(handler, registry)

    def test_logging_a_request(self):
        request = Request.blank('/foo')
        request.environ.update({
            'HTTP_VERSION': '1.1',
            'REMOTE_ADDR': '127.0.0.1',
            })
        config_kwargs = {'request': request, 'settings': self.settings}
        with testing.testConfig(**config_kwargs) as config:
            request.registry = config.registry
            tween = self.make_one(registry=config.registry)
            tween(request)

        global logio
        logio.seek(self.logio_position)
        log_lines = logio.read().split('\n')
        self.assertEqual(len(log_lines), 2)

        log_line = log_lines[0]
        self.assertEqual(
            log_line,
            '127.0.0.1 - - [asctime] "GET http://localhost:80/foo 1.1" 200 OK 0 "-" "-"')
