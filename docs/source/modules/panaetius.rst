.. include:: ../global.rst

*********
panaetius
*********

API
===

The following is availble by importing the module:

.. code-block:: python

    import panaetius


panaetius.CONFIG
----------------

:obj:`panaetius.CONFIG` provides an instance of :class:`panaetius.config.Config`


panaetius.set_config()
-----------------------

Conveniently provides :func:`panaetius.library.set_config` 

Use in your module/script with:

.. code-block:: python

    panaetius.set_config(panaetius.CONFIG, 'aws.secret_key', str, mask=True)    


panaetius.CONFIG.aws_secret_key
-------------------------------

Conveniently provides access to all attributes that have been declared with :func:`panaetius.library.set_config`:

.. code-block:: python

    my_secret_key = panaetius.CONFIG.aws_secret_key


panaetius.logger
-----------------

:obj:`panaetius.logger` provides a logger instance already formatted with a nice json output.

.. code-block:: python

    panaetius.logger.info('some logging message')

This gives a logger output of:

.. code-block:: json

    {
        "time": "2020-01-13 23:07:17,913",
        "file_name": "test.py",
        "module": "test",
        "function":"<module>",
        "line_number": "33",
        "logging_level":"INFO",
        "message": "some logging message"
    }
