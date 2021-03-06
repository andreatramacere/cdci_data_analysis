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

import  simple_logger
import  logging
from cdci_data_analysis.analysis.job_manager import  Job



class AysnchExcept(Exception):
    pass

class DataServerQuery(object):

    def __init__(self):
        pass




    def test_connection(self):
        pass

    def test_has_input_products(self):
        pass


    def run_query(self, job, prompt_delegate=True):
        res = None
        try:
            # redirect_out('./')
            # with silence_stdout():
            #simple_logger.logger.setLevel(logging.ERROR)

            if isinstance(job, Job):
                pass
            else:
                raise RuntimeError('job object not passed')

            print('--osa disp--')
            print('call_back_url', job.get_call_back_url())
            print('*** prompt_delegate', prompt_delegate)

            #call to dataserver to get products

            print('--> url for call_back', job.get_call_back_url())
            print("--> cached object in", res, res.ddcache_root_local)
            job.set_done()
        except Exception as e:

            job.set_failed()
            print("ERROR->")
            print(type(e), e)
            print("e", e)
            e.display()
            raise RuntimeWarning('ddosa connection or processing failed', e)

        except AysnchExcept as e:

            if isinstance(job, Job):
                print('--> url for call_back', job.get_call_back_url())
            else:
                raise RuntimeError('job object not passed')

            return res




