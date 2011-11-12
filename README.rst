Openstack Common
================
Provides components which are re-used across multiple OpenStack projects. Each
component provided by openstack-common should be generic enough to stand on it's
own and should ideally already be in use by one or more OpenStack projects.

Good examples of generic components which should be transitioned to
openstack-common include:

 * Logging
 * Configuration
 * i18n Translation
 * Common database logic
 * WSGI server/application/middleware
 * AMQP/RPC
 * Performance metrics

OpenStack projects are not required to use the code provided by openstack-common,
but it is highly recommended. 


Common Developer Tasks
----------------------
Run PEP8 compliance task:
    ``$ tools/pep8``

Run pylint code compliance task:
    ``$ tools/pylint``

Run tests and show test coverage report (in a virtual environment):
    ``$ tools/run_tests``

Run tests and show test coverage report:
    ``$ nosetests``

Install this checkout locally, not overriding system libraries:
    ``$ python setup.py develop``

Install this checkout locally, overriding system libraries:
    ``$ python setup.py install``
