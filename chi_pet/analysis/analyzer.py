#!/usr/bin/env python
# In case of poor (Sh***y) commenting contact adam.lamson@colorado.edu
# Basic
import sys
import os
from os import path as pth
# Testing
import pandas as pd
from .base_funcs import *
import _pickle as pickle
import h5py
# sys.path.append(os.path.join(os.path.dirname(__file__), '[PATH]'))


"""@package docstring
File: analyzer.pyAuthor: Adam Lamson
Email: adam.lamson@colorado.edu
Description:
"""


class Analyzer(object):

    """!Base object for analysis composite tree """

    def __init__(self, path, param_dir='params', data_dir='data',
                 subnodeType=None, **kwargs):
        """!Initialize analyzer object with necessary information.

        @param path: TODO
        @param nodeType: TODO

        """
        self._path = self.CheckPath(path)
        self._data_dir = create_datadir(self._path, data_dir)
        # self._param_dir = self.CheckPath(pth.join(self._path, param_dir))
        self._pfile_lst = []
        # self._pfile_lst = [
        # f for f in os.listdir(
        # self._param_dir) if f.endswith('.yaml')]
        self._subnodeType = subnodeType
        self._params = {}

        self._name = self._path.split('/')[-1]

        self._subnodes = []
        self._data_dict = {}
        self._h5_data = None

    def CheckPath(self, path):
        """!Make sure path to directory exists
        @param path: TODO
        @return: TODO

        """
        if path == 'cur_dir':
            return pth.abspath(os.getcwd())
        elif not pth.isdir(path):
            raise FileNotFoundError("Directory [{}] does not exist."
                                    "Try again.".format(path))
        else:
            return pth.abspath(path)

    def ParseParams(self):
        """! Make a param dictionary
        @return: void, creates params dictionary

        """
        for pf in self._pfile_lst:
            with open(pf, 'r') as f:
                param_d = yaml.safe_load(f)
                self._params[pf] = param_d

    def Analyze(self, filelist, overwrite=False):
        """!Analyze data in the file provided

        @param filelist: TODO
        @return: TODO

        """
        pass

    def Write(self):
        """!Write out analyzed data into an excel file.

        @return: TODO

        """
        pass

    def Collect(self):
        """!Collect all subnodes
        @return: TODO

        """
        pass

    def Graph(self):
        """!TODO: Docstring for Graph.
        @return: TODO

        """

    def GraphSubnodes(self, level=-2):
        """!TODO: Docstring for GraphSubnodes.
        @return: TODO

        """
        if level == -1 or self._subnodeType is None:
            return
        for sn in self._subnodes:
            print("--- Graphing {} ---".format(sn._name))
            sn.Graph()
            sn.GraphSubnodes(level - 1)
        return

    def Save(self):
        """!Save state of analyzer object
        @return: void

        """
        self._h5_data.flush()
        self._h5_data.close()
        # # Make pickle filename
        # filename = pth.join(self._data_dir, "{}.pickle".format(self._name))
        # # Dump data into pickle file
        # with open(filename, 'wb') as f:
        #     pickle.dump(self._data_dict, f)
        # print("        - {} saved - ".format(self._path))

    def Load(self):
        """!Load saved state of analyzer
        @return: boolean on whether load was successful or not

        """
        # TODO Make sure this works correctly
        self._h5_data = h5py.File(pth.join(self._data_dir,
                                           "{}.h5".format(self._name)), 'r')
        # filename = pth.join(self._data_dir, "{}.pickle".format(self._name))
        # if pth.exists(filename):
        #     with open(filename, 'rb') as f:
        #         try:
        #             self._data_dict = pickle.load(f)
        #         except BaseException:
        #             return false
        #     return True
        # else:
        #     print(("    Could not find file '{}'.").format(filename))
        #     return False

    def Read(self):
        """!TODO: Docstring for Read.
        @return: TODO
        """
        pass

    def ReadSubnodes(self, level=-2):
        if level == -1 or self._subnodeType is None:
            return
        else:
            for sn in self._subnodes:
                sn.ReadSubnodes(level - 1)


##########################################
if __name__ == "__main__":
    print("Not implemented yet")
