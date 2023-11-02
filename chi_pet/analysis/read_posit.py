#!/usr/bin/env python
# In case of poor (Sh***y) commenting contact alamson@flatironinstitute.org
# YOLO edelmaie@colorado.edu (too)
# Basic
import sys
import os
import pdb
import gc
# Analysis
import numpy as np
import yaml

from operator import attrgetter

from scipy import special
import scipy.misc

# import pandas as pd
# import matplotlib.pyplot as plt
# import matplotlib as mpl
# from math import *

"""@package docstring
File: read_posit_base.py
Author: Adam Lamson
Email: alamson@flatironinstitute.org
Description: Base class for all ReadPosit classes which take in a binary
file (position or posit files) and interprets bits as objects to be analyzed.
"""


class ReadPositBase(object):

    """!Base class for ReadPosit objects"""

    def __init__(self, seed_path, posit_name,
                 default_file='default.yaml', equil_file='equil.yaml'):
        """!Initialize posit class with necessary binary and parameter files.

        @param seed_path: Path to seed directory containing posit file.
        @param posit_name: Posit file name
        @param default_file: Default global parameters for simulation
        @param equil_file: Adjusted global parameters for simulation

        """
        self.seed_path = os.path.abspath(seed_path)
        self.posit_path = os.path.join(self.seed_path, posit_name)

        self.default_yaml = self.GetYamlDict(default_file)
        self.equil_yaml = self.GetYamlDict(equil_file)
        self.configsize = None

    def GetYamlDict(self, file_name):
        """!Read in yaml dictionary of parameters

        @param file_name: name of yaml file containing parameters
        @return: Dictionary of files

        """
        file_path = os.path.join(self.seed_path, file_name)
        file_dict = ''
        with open(file_path, 'r') as stream:
            file_dict = yaml.safe_load(stream)
        return file_dict

    def CheckDefaultThenEquil(self, key, val=None):
        """!Check to see if a parameter key is in the default file and then the equil file

        @param key: name of parameter in yaml files
        @param val: default value of parameter if not found in default or equil yaml files
        @return: Return value of parameter checked if it exists

        """
        if key in self.default_yaml:
            val = self.default_yaml[key]
        if key in self.equil_yaml:
            val = self.equil_yaml[key]
        if not val and val != 0:
            print('{} not in default or equil files.'.format(key))
            val = None
        return val

    def LoadPosit(self):
        """!Load in posit file into object and initialize with header
        @return: void, changes self.f_posit

        """
        self.f_posit = open(self.posit_path)
        # pdb.set_trace()
        self.ReadPosHeader()
        self.CountFrames()

    def UnloadPosit(self):
        """!Unload posit file by closing self.f_posit
        @return: void, closes self.f_posit

        """
        self.f_posit.close()

    def ReadPosHeader(self, headerdt):
        """!Read in meta data for the rest of posit file

        @param headerdt: dictionary of data types in header file to be read in
        @return: dictionary of header parameters, changes self.f_data_start and self.cur_Frame

        """
        header = np.fromfile(self.f_posit, dtype=headerdt, count=1)[0]
        self.f_data_start = self.f_posit.tell()
        self.cur_frame = -1
        return header

    def CountFrames(self):
        """!Counts the number of frames in the posit file
        @return: void, sets self.framezie and self.nframes
        """
        assert (self.configsize is not None)
        self.data_file_position = self.f_posit.tell()
        self.f_posit.seek(0, os.SEEK_END)
        final_file_position = self.f_posit.tell()
        self.f_posit.seek(self.data_file_position, os.SEEK_SET)
        self.framesize = final_file_position - self.data_file_position
        self.nframes = int(self.framesize / self.configsize)

    def FindFramePosit(self, frame_num):
        """!Find a specific frame in the posit file and set position to this frame.

        @param frame_num: Frame number of frame you wish to read
        @return: void, changes self.cur_frame

        """
        self.f_posit.seek(self.data_file_position +
                          (frame_num - 1) * self.configsize, os.SEEK_SET)
        self.cur_frame = frame_num - 1
        self.ReadFrame()
        return

    def ReadFrame(self):
        """!Read the current frame in the posit file
        @return: current frame in the data type that corresponds to self.framedt

        """
        return np.fromfile(self.f_posit, dtype=self.framedt, count=1)[0]


##########################################
if __name__ == "__main__":
    p = ReadPosit(sys.args[1], sys.args[2], sys.args[3], sys.args[4])
