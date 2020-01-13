.. include:: ../global.rst

panaetius :modname:`panaetius`
-------------------------------------


API
===

The following is availble by importing the module:

.. code-block:: python

    import panaetius


panaetius.CONFIG
----------------

``panaetius.CONFIG`` provides an instance of :class:`panaetius,config.Config`


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

    panaetius.CONFIG.aws_secret_key


panaetius.logger
-----------------

``panaetius.logger`` provides a logger instance already formatted with a nice json output.
