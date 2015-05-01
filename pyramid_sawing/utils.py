# -*- coding: utf-8 -*-
# ###
# Copyright (c) 2015, Rice University
# This software is subject to the provisions of the GNU Affero General
# Public License version 3 (AGPLv3).
# See LICENCE.txt for details.
# ###


__all__ = ('local_settings')


def local_settings(settings, prefix):
    """Localizes the settings for the dotted prefix.
    For example, if the prefix where 'xyz'::

        {'xyz.foo': 'bar', 'other': 'something'}

    Would become::

        {'foo': 'bar'}

    Note, that non-prefixed items are left out and the prefix is dropped.
    """
    prefix = "{}.".format(prefix)
    new_settings = {k[len(prefix):]:v for k, v in settings.items()
                    if k.startswith(prefix)}
    return new_settings
