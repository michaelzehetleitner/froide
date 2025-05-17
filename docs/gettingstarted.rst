===============
Getting Started
===============

This is a guide that will get you started with Froide.
If you plan to setup a site based on Froide, you should not run Froide directly, but instead use Froide as a dependency in your own project.


Set up the development environment
----------------------------------

Froide requires Python 3.5+. You should be using a Python 3 virtual environment or similar setup.
Setup a virtual environment for development with `venv`like so::

    # Create virtualenv
    python -m venv venv
    # Activate it
    source venv/bin/activate

Get the source code with Git from the GitHub repository::

    git clone git://github.com/okfde/froide.git
    cd froide

Install the `libmagic` library, which is a system requirement. See `https://github.com/ahupp/python-magic#dependencies <https://github.com/ahupp/python-magic#dependencies>`_ for details.

Install the requirements inside the virtual env with `pip`::

    pip install -r requirements.txt

This installs the Python dependencies into the virtual environment.

Frontend development
--------------------

The frontend requires `Node.js` 22 or higher. After installing Node.js,
install the frontend dependencies with ``pnpm``::

    pnpm install

Run the development server with::

    pnpm run dev

To create a production build, use::

    pnpm run build

For UI tests the Playwright browser must be installed::

    playwright install --with-deps chromium

Froide requires one of Django's geospatial database backends. `<https://docs.djangoproject.com/en/1.11/ref/contrib/gis/install/#spatial-database>`_.

Froide is designed to run with the PostgreSQL database with PostGIS extension. You may be able to use a different Django-supported geospatial database, but it is not recommended. Elasticsearch is used as a search engine.

You can install these services as you wish. There is a `docker-compose.yml` that provides a set of these services for use with Docker.

You need to configure these services in your Django settings or via environment variables. There's a `local_settings.py.example` that can be used to locally override settings.

After configuring database and search engine, run database migrations::

    python manage.py migrate

Now you can already start the web server::

    python manage.py runserver

Visit `http://localhost:8000 <http://localhost:8000>`_ and there is your running Froide instance!

You can quit the server (Ctrl+C) and create a superuser account::

    python manage.py createsuperuser


.. _add-basic-database-objects:


Custom settings
--------------------

By default the Django Web server uses the `settings.py` file in the ``froide`` directory (the `froide.settings` Python module). This will be fine for your first experiments but if you want to customize your froide instance you will want your own settings file.

Go into the ``froide`` directory and copy the `local_settings.py.example` to `local_settings.py`::

    cd froide
    cp local_settings.py.example local_settings.py

Now you can customize that settings file to your liking.


Search with Elasticsearch
--------------------

An example configuration for Elasticsearch would look like this::

    ELASTICSEARCH_INDEX_PREFIX = 'froide'
    ELASTICSEARCH_DSL = {
        'default': {
            'hosts': 'localhost:9200'
        },
    }

.. _background-tasks-with-celery:

Background Tasks with Celery
----------------------------

From the standard settings file everything is already setup for background tasks except that they are not running in the background.

You need to change the `CELERY_TASK_ALWAYS_EAGER` setting to `False` in your custom settings::

    CELERY_TASK_ALWAYS_EAGER = False

You need a broker for Celery. Find out more at the `Celery Docs <http://docs.celeryproject.org/en/latest/getting-started/first-steps-with-celery.html#choosing-a-broker>`_.

We recommend `RabbitMQ <http://www.rabbitmq.com/>`_ as broker. Install it and then start it in a different terminal like this::

    rabbitmq-server

After you started the broker open yet another terminal, activate your virtual environment and run the celery worker like this::

    python manage.py celeryd -l INFO -B

Now your server will send background tasks to Celery. Lots of common tasks are designed as background tasks so that an ongoing HTTP request can send a response more quickly. The following things are designed as background tasks:

- Search Indexing: Updates to database objects are indexed in the background
- Email Sending: When an action triggers an email, it's sent in the background
- Denormalized counts on database objects

Celery also takes the role of `cron` and handles periodic tasks. These are setup in the `CELERYBEAT_SCHEDULE` setting.
