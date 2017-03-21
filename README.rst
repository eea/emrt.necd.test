Installation
============

Package requires at least Python 3.5.

::

  pip install -U https://github.com/eea/emrt.necd.test.git


Usage
=====

::

  seleniumtesting http://localhost/Plone/2015/ emrt.necd.test.review_folder \
    -ea roles sectorexpert user_for_sectorexpert \
    -ea users "user_for_sectorexpert" "pwd_for_user"

Please also check the ``edw.seleniumtesting`` `usage page <https://github.com/eaudeweb/edw.seleniumtesting#usage>`_ for additional information.

