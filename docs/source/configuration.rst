Configuration
=============

panaetius is fairly easy to configure. There are just a couple of options to be aware of.

Manual configuration of ``Config`` instance
--------------------------------------------

Configuring with a ``__header__.py`` is deprecated. Manually set this value.

Use the following snippet to configure (in ``__init__.py``):

.. code-block:: python

    import panaetius
    from panaetius.config import Config

    CONFIG = Config(path="~/.config/island-code-extractor", header="island-code-extractor")

    panaetius.set_config(CONFIG, "reddit.secret")

Access this in your code by importing the ``CONFIG`` instance from your module:

.. code-block:: python

    from island_code_extractor import CONFIG
    from island_code_extractor import panaetius

    CONFIG.reddit_output_path
    panaetius.logger.info("Using logger")

__header__.py
-------------

You should set a ``__header__.py`` next to your script or module.

This ``__header__.py`` should contain a ``__header__`` variable that sets the name of your project/script.

E.g a ``__header__.py`` for the module ``plex_posters`` would look like:

.. code-block:: python

    __header__ = 'plex_posters' 

Your config file can then be created at ``~/.config/__header__/config.toml``. 

Your environment variables can be created with:

.. code-block:: bash

    HEADER_FOO = "bar"
    HEADER_SUBSECTION_FOO = "bar"

The headers of the toml file would look like:

.. code-block:: toml

    [__header__]
    foo = bar

    [__header__.subsection]
    foo = bar

If you are writing a script, simply place this ``__header__.py`` along side your script. Panaetius will pick this up when the script is ran.

If you are writing a module, you can either place the ``__header__.py`` alongside the script that uses your module. If this is not possible, panaetius will set the default ``__header__`` variable to the name of the virtualenv that the script is activated from.

If neither of the above aren't possible (say your script is running in a lambda on AWS), then ``__header__`` will be set to the default of ``panaetius``.
