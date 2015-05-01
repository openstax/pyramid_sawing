# -*- coding: utf-8 -*-
# ###
# Copyright (c) 2015, Rice University
# This software is subject to the provisions of the GNU Affero General
# Public License version 3 (AGPLv3).
# See LICENCE.txt for details.
# ###
from logging.config import dictConfig

import yaml

from .utils import local_settings

__all__ = (
    'includeme',
    )

PROJECT = 'pyramid_sawing'
PREFIX = PROJECT


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
