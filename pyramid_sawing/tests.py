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

from pyramid import testing


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
    format    : '%(levelname)-5.5s;.;%(hostname)s;.;%(message)s'

filters:
  context:
    ()        : pyramid_sawing.filters.ContextFilter

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

loggers:
  pyramid_sawing.tests:
    level     : INFO
    handlers  : [logio_with_context]
    propagate : 0

root:
  level       : NOTSET
  handlers    : [logio]
"""
logio = None


class IncludePluginTestCase(unittest.TestCase):

    def setUp(self):
        global logio
        logio = io.BytesIO()

        # Put the config somewhere.
        self.logging_config_filepath = mkstemp()[1]
        with open(self.logging_config_filepath, 'w') as f:
            f.write(CONFIG)
        # Settings...
        self.settings = {
            'pyramid_sawing.file': self.logging_config_filepath,
            }
        self.addCleanup(os.remove, self.logging_config_filepath)

    def tearDown(self):
        global logio
        logio = None

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
        logio.seek(0)
        log_lines = logio.read().split('\n')
        self.assertEqual(len(log_lines), 3)

        # Check the root message...
        parsed_root_msg = log_lines[0].split(';.;')
        self.assertEqual(parsed_root_msg, ['ERROR', root_log_msg])
        parsed_local_msg = log_lines[1].split(';.;')
        self.assertEqual(parsed_local_msg,
                         ['INFO ', socket.gethostname(), local_log_msg])
