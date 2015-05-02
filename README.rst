Pyramid Sawing
==============

.. image:: https://travis-ci.org/Connexions/pyramid_sawing.svg
   :target: https://travis-ci.org/Connexions/pyramid_sawing

.. image:: https://badge.fury.io/py/pyramid_sawing.svg
    :target: http://badge.fury.io/py/pyramid_sawing

A Pyramid framework plugin for configurating logging
via `YAML <http://yaml.org>`_.
This uses the Python standard-library's logging
(initialized using ``logging.config.dictConfig``).

.. contents:: Table of Contents

Usage
-----

Include the package in your project, either by adding to the INI configuration::

    pyramid.includes = pyramid_sawing
    pyramid_sawing.file = my-logging-config.yaml

Or declarative via the configuration object::

    config.include('pyramid_sawing')
    assert 'pyramid_sawing.file' in config.registry.settings

You'll be required to specify a logging configuration file
at ``pyramid_sawing.file``, which points to the file that contains your
YAML logging configuration.

YAML Configuration
------------------

This configuration follows the standard-library's
`logging.config dictionary schema <https://docs.python.org/3/library/logging.config.html#configuration-dictionary-schema>`_

An example configuration might look like this::

    ###
    # logging configuration
    ###
    version: 1

    formatters:
      generic:
        format    : '%(asctime)s %(levelname)-5.5s [%(name)s][%(threadName)s] %(message)s'
      papertrail:
        format    : '%(asctime)s %(hostname)s my_project %(message)s'
        datefmt   : '%Y-%m-%dT%H:%M:%S'
    filters:
      context:
        ()        : pyramid_sawing.filters.ContextFilter
    handlers:
      console:
        class     : logging.StreamHandler
        level     : NOTSET
        formatter : generic
        stream    : 'ext://sys.stdout'
      syslog:
        class     : logging.handlers.SysLogHandler
        level     : DEBUG
        formatter : papertrail
        filters   : [context]
        address   : ['<host>.papertrailapp.com', 11111]
    loggers:
      my_project:
        level     : INFO
        handlers  : [console, syslog]
        propagate : 0
    root:
      level       : NOTSET
      handlers    : []

A typical *gotcha* in configuring this is to forget the 'version'. Please
make sure you include ``version: 1`` in your configuration.

Additional Features
-------------------

Transit Logging
~~~~~~~~~~~~~~~

This resembles the functionality you would find in ``pyramid_translogger``
except that this implementation is more configurable.

To enable this feature, add the following line to your configuraton/settings.

::

    pyramid_sawing.transit_logging.enabled? = yes
    # Optional...
    # The default logger_name is `transit_logger`
    pyramid_sawing.transit_logging.logger_name = lumberjack

A template for configuring the transit logger would be something like::

    formatters:
      apache_style:
        # filters : [environ]
        format    : '%(REMOTE_ADDR)s - %(REMOTE_USER)s [%(asctime)s] "%(REQUEST_METHOD)s %(REQUEST_URI)s %(HTTP_VERSION)s" %(status)s %(bytes)s "%(HTTP_REFERER)s" "%(HTTP_USER_AGENT)s"'
        datefmt   : '%d/%b/%Y:%H:%M:%S'
    filters:
      environ:
        ()        : pyramid_sawing.filters.EnvironFilter
    handlers:
      console:
        class     : logging.StreamHandler
        formatter : apache_style
        filters   : [environ]
        stream    : 'ext://sys.stdout'
    loggers:
      transit_logger:
        handlers  : [console]
        propagate : 0

This should give you the exact same output as ``pyramid_translogger``.

License
-------

This software is subject to the provisions of the GNU Affero General
Public License Version 3.0 (AGPL). See LICENSE.txt for details.
Copyright (c) 2015 Rice University
