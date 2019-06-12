import os
import re


def get_params_from_path(path_name):
    param_list = path_name.split("_")
    params = {}

    for param in param_list:
        m = re.match("([a-zA-Z]+)(.*)", param)
        params[m.group(1)] = [float(p) for p in m.group(2).split(',')]

    return params


def get_dir_names(dir_path):
    """Create a list that contains the parameter directories names"""
    dir_names = next(os.walk(dir_path))[1]
    return dir_names
