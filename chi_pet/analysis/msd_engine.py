#!/usr/bin/env python
# In case of poor (Sh***y) commenting contact adam.lamson@colorado.edu
# YOLO edelmaie@colorado.edu (too)
# Basic
import sys, os, pdb
import gc
## Analysis
import numpy as np
import yaml

from operator import attrgetter

from scipy import special
import scipy.misc
from scipy.optimize import curve_fit

from .read_posit_chromosomes import ReadPositChromosomes

# import pandas as pd
# import matplotlib.pyplot as plt
# import matplotlib as mpl
# from math import *

'''
Name: msd_engine.py
Description: Generates the mean squared displacement for things
Input:
Output:
'''

def LinearFitCheat(x, a, b):
    return a*x + b

#Class definition
class MSDEngine(object):
    def __init__(self, ndim, nframes, nposit, delta, uc):
        self.nframes = nframes
        self.ndim = ndim
        self.uc = uc
        self.nposit = nposit
        self.delta = delta

    ### Initializations
    def InitChromosomes(self, chromosomes):
        self.nkcs = chromosomes.nkc
        self.rkc0 = chromosomes.r
        self.ukc0 = chromosomes.u
        self.radiuskc = chromosomes.radiuskc
        self.kc_trans_msd = np.zeros(self.nframes)
        self.kc_trans_msd_err = np.zeros(self.nframes)
        self.kc_rot_msd = np.zeros(self.nframes)
        self.kc_rot_msd_err = np.zeros(self.nframes)

    ### Calculations
    def CalcMSDChromo(self, frame, chromosomes):
        trans_msd = np.zeros(self.nkcs)
        rot_msd = np.zeros(self.nkcs)
        rkc = chromosomes.r
        ukc = chromosomes.u
        for ikc in range(self.nkcs):
            i = 3*ikc
            j = i+3
            dr = rkc[i:j:1] - self.rkc0[i:j:1]
            costheta = np.dot(ukc[i:j:1],self.ukc0[i:j:1])
            costheta = costheta/np.linalg.norm(ukc[i:j:1])
            costheta = costheta/np.linalg.norm(self.ukc0[i:j:1])
            dtheta = np.arccos(np.clip(costheta, -1.0, 1.0))
            trans_msd[ikc] = np.dot(dr,dr)
            rot_msd[ikc] = dtheta*dtheta

        trans_msd_avg = np.mean(trans_msd)
        trans_msd_stddev = np.std(trans_msd, ddof=1)
        trans_msd_stddevmean = trans_msd_stddev/np.sqrt(self.nkcs)
        self.kc_trans_msd[frame] = trans_msd_avg
        self.kc_trans_msd_err[frame] = trans_msd_stddevmean
        
        rot_msd_avg = np.mean(rot_msd)
        rot_msd_stddev = np.std(rot_msd, ddof=1)
        rot_msd_stddevmean = rot_msd_stddev/np.sqrt(self.nkcs)
        self.kc_rot_msd[frame] = rot_msd_avg
        self.kc_rot_msd_err[frame] = rot_msd_stddevmean

    ### Graphs/Plots
    def GraphMSD_Chromosomes_Trans(self, ax, label, color='b', me=1, xlabel=True):
        ax.set_title("Kinetochore Translation MSD")
        ax.set_ylabel(r'MSD ($\mu$m$^{2}$)')
        if xlabel:
            ax.set_xlabel(r'Time (s)')

        xvals = np.zeros(self.nframes)
        # Do unit conversions
        for frame in range(self.nframes):
            xvals[frame] = frame * self.nposit * self.delta * self.uc['sec'][1]
        self.kc_trans_msd = self.kc_trans_msd * self.uc['um'][1] * self.uc['um'][1]
        self.kc_trans_msd_err = self.kc_trans_msd_err * self.uc['um'][1] * self.uc['um'][1]

        ax.errorbar(xvals, self.kc_trans_msd, yerr=self.kc_trans_msd_err, fmt='o')

        # Run a fit on this
        xvalfit = xvals[1:]
        yvalfit = self.kc_trans_msd[1:]
        yvalerr = self.kc_trans_msd_err[1:]
        popt, pcov = curve_fit(LinearFitCheat, xvalfit, yvalfit, sigma=yvalerr)
        print(popt)
        print(pcov)
        pfit = np.poly1d(popt)
        print(pfit)
        ax.plot(xvalfit, pfit(xvalfit), 'r--')
        diffsphere = pfit[1]/6. #hardoded for 3d
        print("D_kc: {:.4e} um2/s".format(diffsphere))

