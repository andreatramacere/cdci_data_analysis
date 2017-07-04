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

import  ast
from datetime import datetime, date, time

import  numpy as np

class ParameterGroup(object):

    def __init__(self,par_list,name,exclusive=True,def_selected=None,selected=None):
        self.name=name
        self._par_list=par_list
        self._check_pars(par_list)
        self.exclusive=True

        self.msk = np.ones(len(par_list), dtype=np.bool)

        if exclusive==True:
            self.msk[::]=False

            if def_selected is None:
                self.msk[0]==True

        if  def_selected is not None:
            self.select(def_selected)

        if selected is not None:
            self.select(selected)



    @property
    def par_list(self):
        return self._par_list

    @property
    def names(self):
        return [p.name for p in self._par_list]


    def select(self,name):
        if isinstance(name,Parameter):
            name=Parameter.value
        for ID,p in enumerate(self._par_list):
            if p.name==name:
                self.msk[ID]=True
                self._selected=self._par_list[ID].name

        if self.msk.sum()>1 and self.exclusive==True:
            raise RuntimeError('only one paramter can be selected in mutually exclusive groups')


    def _check_pars(self, par_list):
        for p in par_list:
            if isinstance(p,Parameter):
               pass
            elif isinstance(p,ParameterRange):
                pass
            else:
                raise RuntimeError('you can group Paramters or ParamtersRanges found',type(p))


    def to_list(self):
        _l=[]
        for p in self._par_list:
            if isinstance(p,Parameter):
               _l.append(p)
            elif isinstance(p,ParameterRange):
                _l.extend(p.to_list())
        return _l


    def add_par(self,par):
        self.par_list.append(par)
        self.msk=np.append(self.msk,False)


    def build_selector(self,name):
        return  Parameter(name, allowed_values=self.names)


class ParameterRange(object):

    def __init__(self,p1,p2,name):
        self._check_pars(p1,p2)
        self.name=name
        self.p1=p1
        self.p2=p2



    def _check_pars(self,p1,p2):
        if type(p1)!=type(p2):
            raise RuntimeError('pars must be of the same time')

        for p in (p1,p2):
            try:
                assert (isinstance(p,Parameter))
            except:
                raise RuntimeError('both p1 and p2 must be Parameters objects, found',type(p))

    def to_list(self):
        return [self.p1,self.p2]


class Parameter(object):
    def __init__(self,name='par',units=None,allowed_units=[],check_value=None,value=None,allowed_values=None):
        self.check_value=check_value

        self._allowed_units = allowed_units
        self._allowed_values = allowed_values
        self.name = name
        self.units=units
        self.value = value
        #self._wtform_dict=wtform_dict




    @property
    def value(self):
        return self._value



    @value.setter
    def value(self,v):
        print ('set',self.name,v,self._allowed_values)
        if v is not None:
            if self.check_value is not None:
                self.check_value(v, units=self.units,name=self.name)
            if self._allowed_values is not None:
                if v not in self._allowed_values:
                    raise RuntimeError('value',v,'not allowed, allowed=',self._allowed_values)
            self._value=v
        else:
            self._value=None


    @property
    def units(self):
        return self._units

    @units.setter
    def units(self,units):

        if self._allowed_units !=[] and self._allowed_units is not None:

            self.chekc_units(units,self._allowed_units,self.name)

        self._units=units

    def set_from_form(self,form):
        if self.name in form.keys:
            self.value=form[self.name]
        else:
            print('par %s not present in form'%self.name)

    def get_form(self,wtform_cls,key,validators,defaults):
         return   wtform_cls('key', validators=validators, default=defaults)

    @staticmethod
    def chekc_units(units,allowed,name):

        if units not in allowed:
            raise RuntimeError('wrong units for par: %s'%name, ' found: ',units,' allowed:', allowed)

    @staticmethod
    def check_value(val,units,par_name):
        pass

    # def get_form_field(self,key=None,default=None,validators=None,wtform_dict=None,wtform=None):
    #     if key is None:
    #        key=self.name
    #
    #     if wtform is  None and wtform_dict is  None:
    #
    #         wtform_dict=self._wtform_dict
    #
    #     if default is not None:
    #         self.check_value(default,self.units)
    #     else:
    #         default=self.value
    #
    #
    #     if wtform is not None and wtform_dict is not None:
    #         raise RuntimeError('either you provide wtform or wtform_dict or you pass a wtform_dict to the constructor')
    #
    #     elif wtform_dict is not None:
    #         wtform=wtform_dict[self.units]
    #
    #     else:
    #         raise RuntimeError('yuo must provide wtform or wtform_dict')
    #
    #     return wtform(label=key, validators=validators, default=default)

    def reprJSON(self):
        return dict(name=self.name, units=self.first, value=self.value)


#class Instrument(Parameter):
#    def __init__(self,T_format,name,value=None):
        #wtform_dict = {'iso': SelectField}


class Time(Parameter):

    def __init__(self,T_format,name,value=None):

        _allowed_units = ['iso', 'mjd', 'prod_list']

        #wtform_dict = {'iso': StringField}
        #wtform_dict['mjd'] = FloatField
        #wtform_dict['prod_list'] = TextAreaField

        super(Time,self).__init__(value=value,
                                  units=T_format,
                                  check_value=self.check_time_value,
                                  name=name,
                                  allowed_units=_allowed_units)
                                  #wtform_dict=wtform_dict)


    @staticmethod
    def check_time_value(value,units,name='par'):
        if units == 'iso':
            try:
                c = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f")
            except:
                raise RuntimeError(name,'value is not iso format YYYY-MM-DDThh:mm:ss.sssss','it is',type(value),value)
        elif units == 'mjd':
            try:
                assert (type(value) == int or type(value) == float)
            except:
                raise RuntimeError(name,'value is not MJD format : int or float', 'it is ','it is',type(value),value)

        elif units=='prod_list':
            try:
                print(type(value))
                assert (type(value) == list or type(value) == str  or type(str(value))== str)
            except:
                raise RuntimeError(name,'value is not product list format : list of strings','it is',type(value),value)

        else:
            raise  RuntimeError(name,'units not valid',units)




class AngularPosition(Parameter):
    def __init__(self, angular_units, reference_system,name, value=None):
        _allowed_units = ['deg']
        super(AngularPosition, self).__init__(value=value,
                                     units=angular_units,
                                     check_value=self.check_angle_value,
                                     name=name,
                                     allowed_units=_allowed_units)

        self.reference_system=reference_system
        #to improve

    @staticmethod
    def check_angle_value(value, units=None, name=None):
        print('check type of ', name, 'value', value, 'type', type(value))
        pass



class AngularDistance(Parameter):
    def __init__(self, angular_units,name, value=None):
        _allowed_units = ['deg']
        super(AngularDistance, self).__init__(value=value,
                                     units=angular_units,
                                     check_value=self.check_angle_value,
                                     name=name,
                                     allowed_units=_allowed_units)



    @staticmethod
    def check_angle_value(value, units=None, name=None):
        print('check type of ', name, 'value', value, 'type', type(value))
        pass




class Energy(Parameter):
    def __init__(self,E_units,name,value=None):

        _allowed_units = ['keV']

        #wtform_dict = {'keV': FloatField}

        super(Energy, self).__init__(value=value,
                                   units=E_units,
                                   check_value=self.check_energy_value,
                                   name=name,
                                   allowed_units=_allowed_units)
                                   #wtform_dict=wtform_dict)




    @staticmethod
    def check_energy_value(value, units=None,name=None):
        print('check type of ',name,'value', value, 'type',type(value))


        try:
            value=ast.literal_eval(value)
        except:
            pass

        if type(value)==int:
            pass
        if type(value)==float:
            pass
        else:
            raise RuntimeError('type of ',name,'not valid',type(value))

