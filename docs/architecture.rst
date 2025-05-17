Architecture
============

This document gives a high-level overview of the main components that make up a typical Froide deployment.

Components
----------

* **Django backend** – provides the web application, REST API and administrative interface.
* **Celery worker with RabbitMQ** – executes asynchronous tasks outside of the request cycle.
* **PostgreSQL/PostGIS** – stores application data and geographic information.
* **Elasticsearch** – powers the search features.
* **Vue frontend** – single-page application that interacts with the backend API.

Diagram
-------

The following diagram illustrates the interaction between these components:

.. code-block:: text

       +-------------------+
       |    Vue frontend   |
       +---------+---------+
                 |
                 v
       +---------+---------+
       |   Django backend  |
       +----+---------+----+
            |         |
            |         v
            |   +-----+-----+
            |   |  Celery   |
            |   | (RabbitMQ)|
            |   +-----+-----+
            |         |
            v         v
     +------------+  +--------------+
     | PostgreSQL |  | Elasticsearch|
     +------------+  +--------------+

