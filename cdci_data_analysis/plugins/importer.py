"""
Overview
--------
   
general info about this module


Classes and Inheritance Structure
----------------------------------------------
.. inheritance-diagram:: 

Summary
---------
.. autosummary::
   list of the module you want
    
Module API
----------
"""

from __future__ import absolute_import, division, print_function

from builtins import (bytes, str, open, super, range,
                      zip, round, input, int, pow, object, map, zip)

__author__ = "Andrea Tramacere"

# Standard library
# eg copy
# absolute import rg:from copy import deepcopy

# Dependencies
# eg numpy 
# absolute import eg: import numpy as np

# Project
# relative import eg: from .mod import f
import  importlib

plugin_list=['cdci_osa_plugin']


instrument_facotry_list=[]
for plugin_name in plugin_list:
    e=importlib.import_module(plugin_name+'.exposer')
    instrument_facotry_list.extend(e.instr_factory_list)
    #for p in plugin.instr_factory_list:
    #    print ('p',p)

