=======
Chi-Pet
=======

.. |check| raw:: html

    <input checked=""  type="checkbox">

.. |check_| raw:: html

    <input checked=""  disabled="" type="checkbox">

.. |uncheck| raw:: html

    <input type="checkbox">

.. |uncheck_| raw:: html

    <input disabled="" type="checkbox">


.. image:: https://img.shields.io/pypi/v/chi_pet.svg
        :target: https://pypi.python.org/pypi/chi_pet

.. image:: https://img.shields.io/travis/lamsoa729/chi_pet.svg
        :target: https://travis-ci.org/lamsoa729/chi_pet

.. image:: https://codecov.io/gh/lamsoa729/chi_pet/branch/master/graph/badge.svg
        :target: https://codecov.io/gh/lamsoa729/chi_pet

.. image:: https://readthedocs.org/projects/chi-pet/badge/?version=latest
        :target: https://chi-pet.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status


Python module to create, schedule, and analyze simulations on computing clusters.


* Free software: MIT license
* Documentation: https://chi-pet.readthedocs.io.


Features
--------
*  Create a directory of nodes

Developing Task
---------------
|check| Create ChiNode class

|check| Create ChiDict class

|uncheck| Have ChiDict read in a list of yaml files

|uncheck| Add ChiParam finding to ChiDict class

|uncheck| Create ChiParam class

|uncheck| Add better leaf node finding

|uncheck| Add object references to chi params

|uncheck| Create tests for functions in chi_lib.py

|uncheck| Change out all os.path to pathlib.Path objects

Credits
-------

This package was created with Cookiecutter_ and the `pyOpenSci/cookiecutter-pyopensci`_ project template, based off `audreyr/cookiecutter-pypackage`_.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`pyOpenSci/cookiecutter-pyopensci`: https://github.com/pyOpenSci/cookiecutter-pyopensci
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
