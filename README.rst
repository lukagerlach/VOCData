========
VOCData
========

Welcome to VOCData, the VOC Dataset Management System! This project is designed to facilitate the management and retrieval of datasets containing data about Volatile Organic Compounds (VOCs) and their subclasses. It aims to become a central source of information about worldwide VOC data, subsequently aiming to answer interesting questions related to VOC data, e.g.:

* Geographical over or under representations of areas
* Analysis of specific VOCs for datasets
* Quick retrieval of contact info for datasets
* and many more...

Our system offers a comprehensive API to handle various operations related to datasets, VOCs, VOC subclasses, research sites, and associated contacts and publications.

Key Features
============

**Dataset Management**

* Create Datasets: Add new datasets to the system.
* Retrieve Datasets: Fetch all datasets or filter datasets by specific criteria such as site, country, VOC subclass, or geographic area.
* Dataset Association: Link datasets to VOC subclasses and sites, allowing for hierarchical data organization and retrieval.

**VOC and VOC Subclass Management**

* Create VOCs: Add new VOCs to the system.
* Retrieve VOCs: Fetch all VOCs or filter VOCs by subclass name.
* Add Relationships: add relationships between VOCs and VOC subclasses, or hierarchical relationships between subclasses.
* VOC Subclasses: Manage and retrieve VOC subclasses, including retrieving all subclasses associated with a specific VOC and hierarchical VOC Subclass relationships.

**Site Management**

* Create Sites: Add new research sites where data is collected.
* Retrieve Sites: Fetch all research sites or filter sites within a specific geographic area.

**Contact Management**

* Create Contacts: Add new contacts associated with datasets.
* Retrieve Contacts: Fetch all contacts or retrieve contacts associated with a specific dataset.

**Publication Management**

* Create Publications: Add new publications referencing datasets.
* Retrieve Publications: Fetch all publications in the system, retrieve publications for a specific dataset.

Quickstart
==========
The easiest way to get started with VOCData is via docker-compose. This will start 2 containers, one for the database and one for the backend providing the API. Swagger UI automatically generates API docs that are available under :code:`<your_host>:<your_port>/docs` (:code:`localhost:80/docs`) as soon as the app started.
It is suggested to checkout the API docs to get familiar with the project and its functions.  To get a better understanding of the underlying datastructure, check out `this model <https://miro.com/welcomeonboard/MDlDZVExalgzcnNwRjc4Z0ZiRlN2SDc2QmhxSVNzQm1vR0JqY0dwcWxrOXd2VmRLT2tmS3M2Y1NzTFo4QXhicHwzNDU4NzY0NTU1Nzg0OTI4Mjk1fDI=?share_link_id=185847563129>`_.

.. code-block:: shell-session

        $ docker compose up --build

Development Environment
=======================
There are two approaches to develop this project locally, either the "classic" way by developing on your local machine, or directly inside a container using dev containers.

Devcontainers
-------------

Developing from within a `dev container <https://code.visualstudio.com/docs/devcontainers/containers>`_ eliminates discrepancies between your development environment (usually your local machine) and the container environment,
therefore eliminating related issues (e.g. non matching python versions). It fully relies on Docker and an IDE that supports development from inside a container (e.g. VSC or PyCharm).
Dev containers rely on Microsofts `dev container specification <https://containers.dev/implementors/spec/>`_. The dev container configuration can be found in :code:`.devcontainer/backend/devcontainer.json`.
While this is the fastest way to set up a local dev environment, it misses some functionality in comparison to the regular approach (e.g. ease of debugging).

Local Development
-----------------

**Prerequisites:**

* Python @3.10 and pip

.. code-block:: shell-session

        $ python --version              3.10.x
        $ pip --version

* pre-commit (`docs <https://pre-commit.com>`_)

.. code-block:: shell-session

        $ pip install pre-commit
        $ cd VOCData
        $ pre-commit install

**Setup the repository:**

.. code-block:: shell-session

    # Clone the repo
    $ git clone https://github.com/lukagerlach/VOCData.git
    # navigate to backend folder
    # cd backend
    # Create virtual environment named venv
    $ python -m venv venv
    # Active environment
    $ \venv\Scripts\activate            Windows
    $ source venv/bin/activate          Unix based OS
    # Install dependencies
    $ pip install -r requirements.txt

**Startup application:**

To startup the database, it is suggested to make use of docker compose, but only start the database container. Therefore, just run:

.. code-block:: shell-session

    $ docker compose up db --build

Your database is now exposed to your local machine on the port specified in the `compose.yaml`.
The database is built from a postgis image, to be able to natively handle geo-spatial data.

Before starting up the FastAPI backend app, it is necessary to configure the database connection.
While this is automatically handled by docker if we run the backend in a container, running it locally requires some extra setup.
Therefore, create a `database.env` file and put in the following variable:

.. code-block::

    POSTGRES_SERVER=localhost

This way, your backend will now try to find the database on your local machine, not inside the docker network.
Since this is a FastAPI App, just run the following command to start your backend:

.. code-block:: shell-session

    $ fastapi run app/main.py --port 80 --reload

Your backend now runs on port 80 of your local machine. to check the API docs call `http://localhost:80/docs`

Useful Resources
================

This project builds upon a lot of libraries, tools and technologies.
To get a better understanding of how it works, these resources might be helpful:

`Docker Docs <https://docs.docker.com>`_

`Docker Compose Docs <https://docs.docker.com/compose/>`_

`FastApi Docs <https://fastapi.tiangolo.com>`_

`OpenApi Spec <https://swagger.io/specification/>`_

`Pydantic <https://docs.pydantic.dev/latest/>`_

`Sqlmodel <https://sqlmodel.tiangolo.com>`_

`SqlAlchemy <https://www.sqlalchemy.org>`_

`Postgis <https://postgis.net>`_

`Pre-commit <https://pre-commit.com>`_

`Sphinx <https://www.sphinx-doc.org/en/master/>`_

asdasd
