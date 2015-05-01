# -*- coding: utf-8 -*-
# ###
# Copyright (c) 2015, Rice University
# This software is subject to the provisions of the GNU Affero General
# Public License version 3 (AGPLv3).
# See LICENCE.txt for details.
# ###
import unittest


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
