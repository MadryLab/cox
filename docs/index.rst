cox package
===========

Cox is a lightweight, serverless framework for designing and managing
experiments. Inspired by our own struggles with ad-hoc filesystem-based
experiment collection, and our inability to use heavy-duty frameworks, Cox aims
to be a minimal burden while inducing more organization. Created by `Logan
Engstrom <https://twitter.com/logan_engstrom>`_ and `Andrew
Ilyas <https://twitter.com/andrew_ilyas>`_. 

Cox works by helping you easily `log`, `collect`, and
`analyze` experimental results. 

`Why "Cox"? (Aside)`: The name Cox draws both from
`Coxswain <https://en.wikipedia.org/wiki/Coxswain>`_, the person in charge of
steering the boat in a rowing crew, and from the name of `Gertrude
Cox <https://en.wikipedia.org/wiki/Gertrude_Mary_Cox>`_, a pioneer of experimental
design.

Quick Logging Overview 
""""""""""""""""""""""
The cox logging system is designed for dealing with repeated experiments. The
user defines schemas for `Pandas dataframes <https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html>`_
that contain all the data necessary for each experiment instance. Each
experiment ran corresponds to a `data store`, and each specified dataframe
from above corresponds to a table within this store. The experiment stores are
organized within the same directory. Cox has a number of utilities for running
and collecting data from experiments of this nature.


Walkthroughs
------------

.. toctree::
   
   examples/1
   examples/2

Submodules
----------

.. toctree::

   cox.readers
   cox.store
   cox.tensorboard_view
   cox.utils

