Installation
============

Package requires at least Python 3.5.

::

  pip install -U git+https://github.com/eea/emrt.necd.test.git


Usage
=====

::

  seleniumtesting http://localhost/Plone/2018/ emrt.necd.test.review_folder \
    -ea roles sectorexpert user_for_sectorexpert \
    -ea users "user_for_sectorexpert" "pwd_for_user"



Docker build and run tests
==========================

::

Go to the docker directory: ::

	cd docker

Edit the environment file containing the command that runs the tests.
Modify the credentials accordingly for the LDAP Manager DN, Zope user, and EMRT-NECD users and roles.
Run the *setup_tests* to prepare a Plone site for the tests, enter the desired tests and then remove the Plone site by running the *remove_test_site* test.

Build the selenium test service and see the running tests: ::

	docker-compose up -d; docker-compose logs -f selenium


Please also check the ``edw.seleniumtesting`` `usage page <https://github.com/eaudeweb/edw.seleniumtesting#usage>`_ for additional information.

