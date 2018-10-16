Installation
============

Package requires at least Python 3.5.

::

  pip install -U git+https://github.com/eea/emrt.necd.test.git


Usage
=====

::

  seleniumtesting -v -B <browser_name> -P /path/to/browser/driver <url_for_testing> <test_name(s)> \
    -ea ldap_credentials ldap_user ldap_password \
    -ea roles sectorexpert user_for_sectorexpert \
    -ea users "user_for_sectorexpert" "pwd_for_user" \
    -ea roles leadreviewer user_for_leadreviewer \
    -ea users "user_for_leadreviewer" "pwd_for_user" \
    -ea roles msauthority user_for_msauthority \
    -ea users "user_for_msauthority" "pwd_for_user"

For multiple tests, the test names will be separated by whitespace.


Docker build and run tests
==========================

::

Go to the docker directory: ::

	cd docker

Edit the environment file (selenium.env) containing a template for storing the usernames and passwords.
Modify the credentials accordingly for the LDAP Manager DN and EMRT-NECD users and roles.

Build the selenium test service and see the running tests: ::

	docker-compose up -d plone memcached; docker-compose run selenium


Please also check the ``edw.seleniumtesting`` `usage page <https://github.com/eaudeweb/edw.seleniumtesting#usage>`_ for additional information.

