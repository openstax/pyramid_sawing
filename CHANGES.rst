
.. Use the following to start a new version entry:

   |version|
   ----------------------

   - feature message [author]

1.1.2
-----

- Fix the transit logging tween to return the response coming from
  the handler rather than the one attached to the request object. [pumazi]

1.1.1
-----

- Fix the transit logging tween by returning the response,
  which caused secondary tweens and event subscribers to fail. [pumazi]

1.1.0
-----

- Add a transit (request) logging feature that mimics functionality
  found in ``pyramid_translogger``. [pumazi]

1.0.0
-----

- Add a logging filter that allows for ``%(hostname)s`` be be used
  within log lines. [pumazi]
- Logging from a YAML file. [pumazi]
