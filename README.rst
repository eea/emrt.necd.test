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

To build the Docker image: ::

  docker build -t <tag_name> .

Now, run the tests: ::

  docker run --rm -it --cap-add=SYS_ADMIN <tag_name> -A='--headless' http://<host_ip>:<port>/Plone/2018/ emrt.necd.test.review_folder
    -ea roles sectorexpert user_for_sectorexpert
    -ea users "user_for_sectorexpert" "pwd_for_user"

Please also check the ``edw.seleniumtesting`` `usage page <https://github.com/eaudeweb/edw.seleniumtesting#usage>`_ for additional information.

