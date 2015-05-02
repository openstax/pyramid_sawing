# -*- coding: utf-8 -*-
# ###
# Copyright (c) 2015, Rice University
# This software is subject to the provisions of the GNU Affero General
# Public License version 3 (AGPLv3).
# See LICENCE.txt for details.
# ###
import logging
import socket
from wsgiref.util import request_uri

from pyramid.threadlocal import get_current_request


__all__ = ('ContextFilter', 'EnvironFilter')


class ContextFilter(logging.Filter):
    """Provides context specific filter values.
    See also https://docs.python.org/3/library/logging.html#filter-objects
    """
    hostname = socket.gethostname()

    def filter(self, record):
        record.hostname = ContextFilter.hostname
        return True


class EnvironFilter(logging.Filter):
    """Exposes the request ``environ`` to the logger."""

    def _get_defaults(self, environ):
        if environ.get('HTTP_X_FORWARDED_FOR'):
            remote_addr = environ['HTTP_X_FORWARDED_FOR']
        elif environ.get('REMOTE_ADDR'):
            remote_addr = environ['REMOTE_ADDR']
        uri = environ.get('REQUEST_URI', None)
        if uri is None:
            uri = request_uri(environ)
        defaults = {
            'REMOTE_ADDR': remote_addr,
            'REMOTE_USER': environ.get('REMOTE_USER') or '-',
            'REQUEST_URI': uri,
            'HTTP_VERSION': environ.get('SERVER_PROTOCOL'),
            'HTTP_REFERER': environ.get('HTTP_REFERER', '-'),
            'HTTP_USER_AGENT': environ.get('HTTP_USER_AGENT', '-'),
            }
        return defaults

    def filter(self, record):
        request = get_current_request()
        # Apply a set of default values to the record.
        for key, value in self._get_defaults(request.environ).items():
            setattr(record, key, value)
        # Apply actual values to the record.
        for key, value in request.environ.items():
            setattr(record, key, value)

        # Set the status and byte length to the record.
        response = request.response
        bytes = '-'
        for name, value in response.headers.items():
            if name.lower() == 'content-length':
                bytes = value
                break
        record.bytes = bytes
        record.status = response.status

        return True
