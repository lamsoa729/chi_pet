#!/usr/bin/env python


"""@package docstring
File: chi_param
Author: Adam Lamson
Email: alamson@flatironinstitute.org
Description:
"""

from typing import Optional, List


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


##########################################
if __name__ == "__main__":
    print("Not implemented yet")
