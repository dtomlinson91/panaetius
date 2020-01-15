panaetius
==========

.. image:: https://img.shields.io/readthedocs/panaetius?style=for-the-badge   :target: https://panaetius.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status

.. image:: https://img.shields.io/github/v/tag/dtomlinson91/panaetius?style=for-the-badge   :alt: GitHub tag (latest by date)

.. image:: https://img.shields.io/github/commit-activity/m/dtomlinson91/panaetius?style=for-the-badge   :alt: GitHub commit activity

.. image:: https://img.shields.io/github/issues/dtomlinson91/panaetius?style=for-the-badge   :alt: GitHub issues

.. image:: https://img.shields.io/github/license/dtomlinson91/panaetius?style=for-the-badge   :alt: GitHubtbc

Python module to gracefully handle a .config file/environment variables for scripts, with built in masking for sensitive options. Provides a Splunk friendly formatted logger instance.

Usage
------

Setting a config file
~~~~~~~~~~~~~~~~~~~~~~

The main functionality of ``panaetius`` is using a config file to store variables.

Your ``config.toml`` can be created and found in ~/.config/__header__/config.toml where __header__ is equal to the variable configured/set. `See how to configure`_ this variable in the configuration section of panaetius.

.. _See how to configure: https://panaetius.readthedocs.io/en/latest/configuration.html#header-py

Setting values in a config.toml/environment variables
#######################################################

A ``config.toml`` can be created in the default folder for the module. In this example this would be found in ``~/.config/example_module/config.toml``. 

An example ``config.toml`` could look like:

.. code-block:: toml

    [example_module]
    test = "a6cbf36649b029f3618a0cc1"

    [example_module.logging]
    path = "~/.config/example_module"
    level = "DEBUG"

    [example_module.foo]
    bar = "6b3b96815218960ceaf7cceb"

These are equivalent to the environment variables:

.. code-block:: bash

    EXAMPLE_MODULE_TEST
    EXAMPLE_MODULE_LOGGING_PATH
    EXAMPLE_MODULE_LOGGING_LEVEL
    EXAMPLE_MODULE_FOO_BAR


.. Attention:: 
    Environment variables take precedent over the ``config.toml``. If both are set then the environment variable will be used.

You can overwrite the ``config.toml`` location by setting the environment variable:

.. code-block:: bash

    DEFAULT_CONFIG_PATH = "~/path/to/config"


Setting values in your code
############################

Values in a ``config.toml`` or from an environment variable need to be set in your work in order for you to use them. You can do this easily by

- importing panaetius.
- using the :func:`~panaetius.library.set_config` function.
  
E.g your script could contain:

.. code-block:: python

    import panaetius
    panaetius.set_config(panaetius.CONFIG, 'logging.path')

.. Note::

    The ``key`` attribute in :func:`~panaetius.library.set_config` is specified as a string, with the hirearchy in the config file split with a ``.``

.. Important::

    The default value for a variable defined using :func:`~panaetius.library.set_config` is ``None``. See the documentation of this function to see all the options available.


Accessing values
#################

You can then access the result of this variable later in your code:

.. code-block:: python

    panaetius.CONFIG.logging_path


Logging
~~~~~~~~

In order to save to disk, you need to specify a path for the log file in the config file/environment variable. There is no need to register this with :func:`~panaetius.library.set_config` as ``panaetius`` will do this automatically.

There are other options available for you to configure a logger. These are (including the default values which can be overwritten):

.. code-block:: toml

    [example_module.logging]
    backup_count = 3
    format = "{\n\t"time": "%(asctime)s",\n\t"file_name": "%(filename)s",'
    '\n\t"module": "%(module)s",\n\t"function":"%(funcName)s",\n\t'
    '"line_number": "%(lineno)s",\n\t"logging_level":'
    '"%(levelname)s",\n\t"message": "%(message)s"\n}"
    level = "INFO" # Level should be in CAPS
    rotate_bytes = 512000

You can use the logger in your code by:

.. code-block:: python

    panaetius.logger.info('some log message')

which gives an output of:

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


Importing and using the api
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

See `panaetius api page`_ on how to use and import the module.

.. _panaetius api page: https://panaetius.readthedocs.io/en/latest/modules/panaetius.html


Configuration
---------------

See `configuration page`_ on how to configure ``panaetius``.

.. _configuration page: https://panaetius.readthedocs.io/en/latest/configuration.html
