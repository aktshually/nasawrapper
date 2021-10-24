.. nasawrapper documentation master file, created by
   sphinx-quickstart on Fri Oct 22 21:35:26 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. currentmodule:: nasawrapper

Welcome to nasawrapper!
=======================================

This is a easy to use wrapper for some of the open APIs provided by NASA, with support to sync/async syntax.

.. caution::
   This is an **alpha release** yet, so maybe there are some bugs. Please, report them to `Issues page <https://github.com/End313234/nasawrapper/issues>`_

Features
=======================================
* Easy to use;
* Supports ``sync``/``async`` syntax;
* Provides a better type hinting;

Getting Started
=======================================
To get started, you only have to install ``nasawrapper`` package. You can do this using `PYPI <https://www.pypi.org/>`_:

.. code-block:: batch

   pip install nasawrapper

Once you done that, you're ready to start coding!

Getting An API Key
========================================
In documentation examples, I use ``DEMO_KEY``  API key. Acording to the `Portal <https://api.nasa.gov/>`_, use this API
key is a good way to start exploring the APIs, however, this special API key has much lower 
rate limits (hourly limit: 30 requests per IP address per hour; daily limit: 50 requests per IP address per day) so I also
encourage you to sign up and get an API key. You can sign up in the `NASA API Portal <https://api.nasa.gov/>`_.

After getting an API key, it's good to know that rate limits of the different APIs may vary, but, again, acording to the Portal,
the default rate limit is 1.000 requests per hour (hourly limit) and exceeding these limits will lead to your API key being
temporarily blocked from making requests. More information can be found in the Portal.

Linting
========================================
For a better linting, it's highly recommended to use `Visual Studio Code <https://code.visualstudio.com/>`_ or 
`Pycharm <https://www.jetbrains.com/pycharm/>`_ and `Pyright <https://github.com/Microsoft/pyright>`_

Summary
========================================
* :doc:`APOD </extensions/apod>`
    * :py:class:`SyncApod <apod.SyncApod>`
    * :py:class:`AsyncApod <apod.AsyncApod>`
    * :py:class:`ApodQueryBuilder <apod.ApodQueryBuilder>`

* :doc:`NeoWs </extensions/neows>`
    * :py:class:`SyncNeoWs <neows.SyncNeoWs>`
    * :py:class:`AsyncNeoWs <neows.AsyncNeoWs>`
    * :py:class:`NeoWsQueryBuilder <neows.NeoWsQueryBuilder>`

Getting Help
========================================
* If you're looking for something, try the search box on the top of this page;
* You can report bugs/issues/make suggestions at `Issues page <https://github.com/End313234/nasawrapper/issues>`_
  

.. toctree::
   :maxdepth: 2
   :hidden:
   :caption: Supported APIs

   extensions/apod
   extensions/neows

.. toctree::
   :maxdepth: 2
   :hidden:
   :caption: utils

   extensions/utils