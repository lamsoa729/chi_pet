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

Introduction
------------
The philosophy behind Chi-Pet is to allow you to generate a heirarchy of directories by minimally modifying viable configuration and input files of your choice of simulation framework. These variations could be simple paramter scans or iterative optimizations schemes that require the output of one simulation to be the input of another. Chi-Pet will allow you to create a directory of nodes that can be submitted to a computing cluster. Chi-Pet will also allow you to analyze the output of your simulations and create a heirarchy of directories of those results. Chi-Pet is designed to be modular and extensible so that you can easily add your own simulation framework and analysis tools.

The key lies in the `ChiParam` object that you substitute into yaml or toml files of your simulation. Every ChiParam will be varied in the generated node structure until no all ChiParams have been realized and a viable simulation run is created. 


Chi (non-leaf) node structure
-----------------------------

.. code::

    - ChiNode(Level i)_(param j_val n)
    - metadata.txt
    - args.yaml
    - current_state.dat (node_run.sh generated)
    - subnodes
        - ChiNode(Level i+1)_(param j+1)_(val m)
        - ChiNode(Level i+1)_(param j+1)_(val m+1)
        - …
    - analysis
        - node_postprocess1.h5
        - node_postprocess2.h5
        - …
    - scripts
        - tree_generate.sh (chi generated)
        - node_run.sh (chi generated)
        - step1.sh
        - step2.sh
        - …
    - node_params1.yaml (not fully realized)
    - node_params2.yaml (not fully realized)
    - …



Leaf node structure
-------------------

.. code::

    - ChiNode(Level L)_(param j_val n)
        - metadata.txt
        - args.yaml
        - data
            - raw_data1.dat
            - raw_data2.dat
            - …
        - analysis
            - postprocess1.h5
            - postprocess2.h5
            - video1.mov
            - …
        - scripts
            - step1.sh
            - step2.sh
            - …
        - log.out (chi generated)
        - log.err (chi generated)
        - params1.yaml (fully realized)
        - params2.yaml (fully realized)
        - …


Features
--------
* Create a directory heirarchy of nodes
* Create variations of simulations, optimizing for a given cost function

Developing Task
---------------
|uncheck| Add subnode generating function to ChiNode

|uncheck| Add edge case handling to tests (one for each test)

|uncheck| Create tests for functions in chi_lib.py

|uncheck| Create tests for multi-node generation

|uncheck| Create tests for main Chi and parser

|uncheck| Create a pattern option to pattern

|uncheck| Get commandline arguments working

|uncheck| Create ChiRun class

|uncheck| Make tutorial and quickstart for using Chi-Pet

|uncheck| Create a safe chiparam parser so we don't need to use eval

|check| Create a subparser for creation algorithms

|check| Create ChiNode class

|check| Create ChiDict class

|check| Have ChiDict read in a list of yaml files

|check| Add ChiParam finding to ChiDict class

|check| Create ChiParam class

|check| Add better leaf node finding

|check| Add object references to chi params

|check| Change out all os.path to pathlib.Path objects




Credits
-------

This package was created with Cookiecutter_ and the `pyOpenSci/cookiecutter-pyopensci`_ project template, based off `audreyr/cookiecutter-pypackage`_.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`pyOpenSci/cookiecutter-pyopensci`: https://github.com/pyOpenSci/cookiecutter-pyopensci
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
