.. InstAL documentation master file, created by
   sphinx-quickstart on Thu Apr  7 20:13:16 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

InstAL : The Institutional Action Language
================================


Introduction
------------

Institutions!::

   institution basic

   type Alpha

   exogenous event ex_blue(Alpha)
   exogenous event ex_green(Alpha)
   exogenous event ex_red(Alpha)

   inst event in_blue(Alpha)
   inst event in_green(Alpha)
   inst event in_red(Alpha)

   fluent in_fact(Alpha)
   fluent in_fact_a(Alpha)
   fluent in_fact_b(Alpha)

   obligation fluent obl(ex_red(Alpha),ex_blue(Alpha),ex_green(Alpha), achievement)
   obligation fluent obl(in_fact_a(Alpha),in_fact_b(Alpha),ex_green(Alpha), achievement)

   transient fluent ni_fact(Alpha)

   ni_fact(Alpha) when in_fact(Alpha)
   %% perm(ex_green(Alpha)) when in_fact(Alpha)

   ex_red(Alpha) generates in_red(Alpha)
   in_red(Alpha) initiates
      in_fact(Alpha),
      perm(in_blue(Alpha)),
      pow(in_blue(Alpha)),
      obl(ex_red(Alpha),ex_blue(Alpha),ex_green(Alpha))

   %% in_red(Alpha) terminates perm(in_red(Alpha)), pow(in_red(Alpha))

   ex_blue(Alpha) generates in_blue(Alpha)
   in_blue(Alpha) initiates
      %% in_fact(Alpha),
      perm(in_green(Alpha)),
      pow(in_green(Alpha))

   in_blue(Alpha) terminates in_fact(Alpha)

Documentation Contents
----------------------

.. toctree::
   :maxdepth: 1

   concepts.rst
   system_structure.rst
   repo_structure.rst
   installation.rst
   cli.rst
   examples.rst


API Reference
-------------

.. autosummary::
   :recursive:
   :toctree: _generated_instal

   instal.interfaces



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
