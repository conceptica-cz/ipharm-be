Getting started
===============

Requirements
------------

You need ``docker`` and ``docker-compose`` to run the app.


Installation and configuration
------------------------------

Clone the repository
^^^^^^^^^^^^^^^^^^^^
::

    $ git clone https://github.com/conceptica-cz/ipharm-be.git

Add environment variable files
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Create a environment variable files for:

- ``./.envs/.development/.ipharm_app``
- ``./.envs/.development/.ipharm_postgres``
- ``./.envs/.development/.ipharm_redis``

In the files, set environment variables, mainly those that do not have default values.

:ref:`Environment variables description.<envars>`

Run the app
^^^^^^^^^^^
::

    $ cd ipharm-be
    $ docker-compose up -d

Create superuser
^^^^^^^^^^^^^^^^
::

    $ docker-compose exec ipharm-app python manage.py createsuperuser

Now you can login to the app's admin on localhost:8000/admin/

Populate database with fake data (optional, development only)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

    $ docker-compose exec ipharm-app python manage.py populate


Documentation
-------------
The documentation is available in the source code in the ``/docs/build`` directory

.. _envars:

Environment variables
=====================

iPharm variables
----------------

File: ``./.envs/.development/.ipharm_app``

Django application variables. Used by ``ipharm-app``, ``ipharm-worker``, ``ipharm-beat``  docker services.

ALLOWED_HOSTS
^^^^^^^^^^^^^

No default value (must be set).

Django ``ALLOWED_HOSTS`` - list of hosts separated by comma (or just ``*``).

BASE_IPHARM_REFERENCES_URL
^^^^^^^^^^^^^^^^^^^^^^^^^^

Default: ``http://iciselniky-app:8000/api/v1``

Base references API (iciselniky app) url.

BASE_REFERENCES_URL
^^^^^^^^^^^^^^^^^^^

No default value (must be set).

External API (patient) url.

DEBUG
^^^^^

Default: ``False``

ENVIRONMENT
^^^^^^^^^^^

Default: ``production``

App's environment.

IPHARM_REFERENCES_TOKEN
^^^^^^^^^^^^^^^^^^^^^^^

No default value (must be set).

References API (iciselniky app) token.

LOG_LEVEL
^^^^^^^^^

Default: ``INFO``

Logging level.

REFERENCES_TOKEN
^^^^^^^^^^^^^^^^

No default value (must be set).

External API (patient) token.

SECRET_KEY
^^^^^^^^^^

No default value (must be set).

Django secret key.


Postgres variables
------------------

File: ``./.envs/.development/.ipharm_postgres``

Postgres variables. Used by ``ipharm-postgres`` and also by ``ipharm-app``, ``ipharm-worker``, ``ipharm-beat`` docker services.

POSTGRES_DB
^^^^^^^^^^^

No default value (must be set).

Postgres database name.

POSTGRES_PASSWORD
^^^^^^^^^^^^^^^^^

No default value (must be set).

Postgres database password.

POSTGRES_HOST
^^^^^^^^^^^^^

No default value (must be set).

Postgres database host.

POSTGRES_PORT
^^^^^^^^^^^^^

No default value (must be set).

Postgres database port.

POSTGRES_USER
^^^^^^^^^^^^^

No default value (must be set).

Postrgres database user.


Redis variables
---------------

Redis variables. Used by ``ipharm-redis`` and also by ``ipharm-app``, ``ipharm-worker``, ``ipharm-beat``, ``ipharm-flower`` docker services.

CELERY_BROKER_URL
^^^^^^^^^^^^^^^^^

No default value (must be set).

Celery broker url. Used by flower worker.

REDIS_HOST
^^^^^^^^^^

No default value (must be set).

Redis host.

REDIS_PORT
^^^^^^^^^^

No default value (must be set).

Redis port.


