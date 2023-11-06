#!/usr/bin/env python


"""@package docstring
File: chi_param
Author: Adam Lamson
Email: alamson@flatironinstitute.org
Description:
"""

import re
from typing import Optional, List


class ObjRef(object):
    """ A 'reference' to an object. This allows you to make changes to strings
    or other objects in place of a dictionary or list like structure.
    """

    def __init__(self, obj, key):
        self.obj = obj
        self.key = key

    def set_value(self, value):
        self.obj[self.key] = value

    def get_value(self):
        return self.obj[self.key]

    def __repr__(self):
        return self.obj[self.key]


class ChiParam(object):

    """!Class that holds all the values of a changing parameter."""

    def __init__(self, name: str, format_str: Optional[str] = None,
                 exec_str: Optional[str] = None,
                 vals: Optional[List] = None,
                 level: int = 0,
                 **kwargs):
        """Initialize ChiParam with name, format string, execution string,

        Parameters
        ----------
        name : _type_
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
        self._vals = vals
        self._level = level


# TODO: Make this a class method of ChiParam
def find_chi_param_values(obj, pattern=r'^ChiParam\(.*\)'):
    """Recursive function to find ChiParams in program and returns a list of
    references to those objects.
    """
    # Look through list with the index being the key of the object
    if isinstance(obj, list):
        for k, v in enumerate(obj):
            # If a ChiParam is found, yield it
            if re.match(pattern, str(v)):
                yield ObjRef(obj, k)

            # If another list or dictionary is encountered, recurse into it.
            elif isinstance(v, (dict, list)):
                for result in find_chi_param_values(v, pattern):
                    yield result

    # Walk dictionary recursing into any lists or dictionaries
    elif isinstance(obj, dict):
        for k, v in obj.items():
            # If a ChiParam is found, yield it
            if re.match(pattern, str(v)):
                yield ObjRef(obj, k)
            # If another list or dictionary is encountered, recurse into it.
            elif isinstance(v, (dict, list)):
                for result in find_chi_param_values(v, pattern):
                    yield result
    else:
        return


##########################################
if __name__ == "__main__":
    print("Not implemented yet")
