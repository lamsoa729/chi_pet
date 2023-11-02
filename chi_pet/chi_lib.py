#!/usr/bin/env python
import os
from pathlib import Path
import re
import yaml
from collections import OrderedDict

"""@package docstring
File: chi_lib.py
Author: Adam Lamson
Email: alamson@flatironinstitute.org
Description: Library of common functions for chi_pet
"""


def create_yaml_files_from_dict(dir_path, yml_file_dict):
    for f, d in yml_file_dict.items():
        fpath = dir_path / f
        with open(fpath, 'w') as of:
            dump_yaml_in_order(d, of, default_flow_style=False)


def create_dict_from_yaml_file(path):
    with open(path, 'r') as f:
        ydict = load_yaml_in_order(f)
        return ydict


def load_yaml_in_order(stream,
                       Loader=yaml.Loader,
                       object_pairs_hook=OrderedDict):
    """ Taken from http://stackoverflow.com/questions/5121931/in-python-how-can-you-load-yaml-mappings-as-ordereddicts/21048064#21048064
    Usage: yaml_dict = OrderedYamlLoad(istream)
    """
    class OrderedLoader(Loader):
        pass

    def construct_mapping(loader, node):
        loader.flatten_mapping(node)
        return object_pairs_hook(loader.construct_pairs(node))
    OrderedLoader.add_constructor(
        yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
        construct_mapping)
    return yaml.safe_load(stream, OrderedLoader)


def dump_yaml_in_order(data, stream=None, Dumper=yaml.Dumper, **kwds):
    ''' Taken from http://stackoverflow.com/questions/5121931/in-python-how-can-you-load-yaml-mappings-as-ordereddicts/21048064#21048064
    Usage: OrderedYamlDump(yaml_dictionary, ostream)
    '''
    class OrderedDumper(Dumper):
        pass

    def _dict_representer(dumper, data):
        return dumper.represent_mapping(
            yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
            list(data.items()))
    OrderedDumper.add_representer(OrderedDict, _dict_representer)
    return yaml.dump(data, stream, OrderedDumper, **kwds)


def ind_recurse(pi_list, p_index=0):
    '''Function that creates a list of list of all possible parameter indices'''
    l = []  # return list
    # Cycle through possible value indices for parameter with param index,
    # p_index
    for i in range(pi_list[p_index]):
        if p_index == len(pi_list) - 1:
            # If at the last index (end of recursion) start constructing index
            # list
            l += [[i]]
        else:
            # Prepend i value to front of sublists using recursion
            lst = ind_recurse(pi_list, p_index + 1)
            for x in lst:
                l += [[i] + x]
    return l


def find_str_values(obj, pattern=r'^ChiParam\(.*\)'):
    '''Recursive function to find ChiParams in program and returns a list of
    references to those objects.
    '''
    # Look through list with the index being the key of the object
    if isinstance(obj, list):
        for k, v in enumerate(obj):
            # If you find a match to pattern, create and yeild object
            # reference.
            if re.match(pattern, str(v)):
                yield ObjRef(obj, k)
            # If another list or dictionary is encountered, recurse into it.
            # Yeild any patterns you find
            elif isinstance(v, (dict, list)):
                for result in find_str_values(v, pattern):
                    yield result
    # Look through dictionary with the key being the key to the object
    # reference
    elif isinstance(obj, dict):
        for k, v in obj.items():
            if re.match(pattern, str(v)):
                yield ObjRef(obj, k)
            elif isinstance(v, (dict, list)):
                for result in find_str_values(v, pattern):
                    yield result
    else:
        return


class ObjRef(object):
    ''' A 'reference' to an object. This allows you to make changes to strings
    or other objects in place of a dictionary or list like structure.
    '''

    def __init__(self, obj, key):
        self.obj = obj
        self.key = key

    def Set(self, value):
        self.obj[self.key] = value

    def GetValue(self):
        return self.obj[self.key]

    def __repr__(self):
        return self.obj[self.key]


# TODO turn into node dir. Might not need this any more.
# def find_seed_dirs(path):
#     is_seed = re.compile(r's\d+$')
#     for current, dirnames, filenames in os.walk(path):
#         if is_seed.search(current):
#             yield os.path.abspath(current)


def touch(fname, times=None):
    """ Replicates the UNIX touch command """
    with open(fname, 'a'):
        os.utime(fname, times)


def find_dirs(path):
    """ Find all the child directories one level deep and return a list
        of the absolute paths.
    """
    return [os.path.abspath(x) for x in (next(os.walk(path))[1])]


##########################################
if __name__ == "__main__":
    print("Not implemented. This is strictly a library.")
