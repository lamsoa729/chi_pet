#!/usr/bin/env python


"""@package docstring
File: chi_param
Author: Adam Lamson
Email: alamson@flatironinstitute.org
Description:
"""

import re
from typing import Optional, Union, List, Dict


class ObjRef(object):
    """ A 'reference' to an object that stores ChiParam strings and locations. This allows you to make changes to strings
    or other objects in  a dictionary or list like structure.
    """

    def __init__(self, obj: Union[Dict, List], key: Union[str, int]):
        self.obj = obj
        self.key = key

    def set_value(self, value):
        self.obj[self.key] = value

    def get_value(self):
        return self.obj[self.key]

    def __repr__(self):
        return self.get_value()


def find_chi_param_str(obj: Union[Dict, List],
                       pattern: str = r'^ChiParam\(.*\)'):
    """Recursive function to find ChiParams in a heirarchical parameter dictionary and returns a list of references to the objects that store these strings.
    """
    # Look through list with the index being the key of the object
    if isinstance(obj, list):
        for k, v in enumerate(obj):
            # If a ChiParam is found, yield it
            if re.match(pattern, str(v)):
                yield ObjRef(obj, k)

            # If another list or dictionary is encountered, recurse into it.
            elif isinstance(v, (dict, list)):
                for result in find_chi_param_str(v, pattern):
                    yield result

    # Walk dictionary recursing into any lists or dictionaries
    elif isinstance(obj, dict):
        for k, v in obj.items():
            # If a ChiParam is found, yield it
            if re.match(pattern, str(v)):
                yield ObjRef(obj, k)
            # If another list or dictionary is encountered, recurse into it.
            elif isinstance(v, (dict, list)):
                for result in find_chi_param_str(v, pattern):
                    yield result
    else:
        return


class ChiParam(object):

    """!Class that holds all the values of a changing parameter."""

    def __init__(self, name: str,
                 format_str: Optional[str] = None,
                 exec_str: Optional[str] = None,
                 values: Optional[List] = None,
                 level: int = 0,
                 **kwargs):
        """Initialize a Chi parameter object.

        Parameters
        ----------
        name : str
            _description_
        format_str : Optional[str], optional
            _description_, by default None
        exec_str : Optional[str], optional
            _description_, by default None
        vals : Optional[List], optional
            _description_, by default None
        level : int, optional
            _description_, by default 0
        """
        self._name = name
        self._format_str = format_str
        self._exec_str = exec_str
        self._values = values
        self._level = level
        self._kwargs = kwargs

        # Object reference class will be set here
        self._obj_r = None

    def set_obj_ref(self, obj_r):
        self._obj_r = obj_r

    def get_number_of_values(self):
        return len(self._values)

    def gen_param_values(self):
        # Values already exist so new parameters will not be generated
        if self._values:
            return

        if self._exec_str is None:
            raise RuntimeError(
                "Must provide a command to execute if values are not explicitly given or a list of values.")

        # XXX This is really dangerous and we should figure out a better way to do this. Maybe parsing it first so you can see if it is safe.
        self._values = eval(self._exec_str)

    def set_value(self, index: int):
        self._obj_r.set_value(self._values[index])

    def get_value(self):
        return self._obj_r.get_value()

    def get_dir_str(self):
        return self._format_str.format(self.get_value())

    def __str__(self):
        chi_str = f'ChiParam(name={self._name}, format_str={self._format_str}, exec_str={self._exec_str}, values={self._values}, level={self._level}'
        for k, v in self._kwargs.items():
            chi_str += f', {k}={v}'
        chi_str += ')'
        return chi_str


##########################################
if __name__ == "__main__":
    print("Not implemented yet")
