Development
===========

Run tests
---------

Froide has a test suite. You have to install the test dependencies first::

    pip install -r requirements-test.txt

The default test configuration requires a running elasticsearch instance.
You either have to install elasticsearch or change the configuration to
another search engine.

Then you can run the tests::

    make test

For end-to-end UI tests, you need the Playwright browser installed::

    playwright install --with-deps chromium

Run the UI tests with::

    make testui

Make sure your database, Elasticsearch and RabbitMQ services are running
when executing UI tests.

This also does test coverage analysis. You can generate an HTML report with::

  coverage html --omit="*/migrations/*"

You can then find the test HTML coverage report at `htmlcov/index.html`.

If you want to run tests for modules, classes or methods your can run them like this::

  # Run everything
  python manage.py test froide --settings=froide.settings_test
  # Run only app tests
  python manage.py test froide.foirequest --settings=froide.settings_test
  # run only one test module in app
  python manage.py test froide.foirequest.tests.test_admin.AdminActionTest --settings=froide.settings_test
  # run only one method
  python manage.py test froide.foirequest.tests.test_admin.AdminActionTest.test_approve --settings=froide.settings_test



Build translation
-----------------

Make .po files like this::

    python manage.py makemessages -a -i docs --settings=your_settings


Build docs
----------

The docs can be build with Sphinx but first you must install the theme.
Excecute these commands from the top level of the froide directory::

  git submodule init
  git submodule update

Then change into the `docs` directory and type::

  make html

The documentation will be build and you can find the resulting html in `docs/_build/html`.

Frontend development
--------------------

The frontend requires `Node.js` 22 or higher. Install Node.js and then install
the dependencies with ``pnpm``::

    pnpm install

Start the development server with::

    pnpm run dev

To build the production assets, run::

    pnpm run build

For UI tests you also need to install the Playwright browser::

    playwright install --with-deps chromium
