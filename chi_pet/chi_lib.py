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
    return yaml.load(stream, OrderedLoader)


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


def find_leaf_dirs(path, ignore=['result', 'analysis', 'scripts']):
    # Assume this is a leaf to start
    is_leaf = True
    # See if directories exist in cureent path (besides ignored directories)
    # If so, this is not a leaf and interate into next leaf yielding paths
    for p in path.iterdir():
        if p.is_dir() and p.name not in ignore:
            yield from find_leaf_dirs(p, ignore)
            is_leaf = False
    # This is a leaf directory so yeald this current path
    if is_leaf:
        yield path


def touch(fname, times=None):
    """ Replicates the UNIX touch command """
    with open(fname, 'a'):
        os.utime(fname, times)


def find_dirs(path):
    """ Find all the child directories one level deep and return a list
        of the absolute paths.
    """
    return [Path(dir_path).absolute() for dir_path in (next(os.walk(path))[1])]


##########################################
if __name__ == "__main__":
    print("Not implemented. This is strictly a library.")
