# -*- coding: utf-8 -*-
# ###
# Copyright (c) 2015, Rice University
# This software is subject to the provisions of the GNU Affero General
# Public License version 3 (AGPLv3).
# See LICENCE.txt for details.
# ###
import logging
from logging.config import dictConfig

import yaml
from pyramid.settings import asbool

from .filters import EnvironFilter
from .utils import local_settings

__all__ = (
    'includeme',
    )

PROJECT = 'pyramid_sawing'
PREFIX = PROJECT


class TransitLogger:
    """A Pyramid tween that logs in transit requests."""
    settings_prefix = '.'.join([PREFIX, 'transit_logging'])

    def __init__(self, handler, registry):
        self.handler = handler
        global_settings = registry.settings
        settings = local_settings(global_settings, self.settings_prefix)
        logger_name = settings.get('logger_name', 'transit_logger')
        self.logger = logging.getLogger(logger_name)
        # Ensure the logger has the EnvironFilter added.
        self.logger.addFilter(EnvironFilter())

    def __call__(self, request):
        response = self.handler(request)
        self.logger.info(' ')
        return response


def includeme(config):
    """Pyramid pluggable and discoverable function."""
    global_settings = config.registry.settings
    settings = local_settings(global_settings, PREFIX)

    try:
        file = settings['file']
    except KeyError:
        raise KeyError("Must supply '{}.file' configuration value "
                       "in order to configure logging via '{}'."
                       .format(PREFIX, PROJECT))

    with open(file, 'r') as f:
        logging_config = yaml.load(f)

    dictConfig(logging_config)

    # Enable transit logging?
    if asbool(settings.get('transit_logging.enabled?', False)):
        config.add_tween('pyramid_sawing.main.TransitLogger')
