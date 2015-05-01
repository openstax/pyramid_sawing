# -*- coding: utf-8 -*-
# ###
# Copyright (c) 2015, Rice University
# This software is subject to the provisions of the GNU Affero General
# Public License version 3 (AGPLv3).
# See LICENCE.txt for details.
# ###
import logging
import socket


__all__ = ('ContextFilter')


class ContextFilter(logging.Filter):
    """Provides context specific filter values.
    See also https://docs.python.org/3/library/logging.html#filter-objects
    """
    hostname = socket.gethostname()

    def filter(self, record):
        record.hostname = ContextFilter.hostname
        return True
