#!/usr/bin/env python
# Basic
import sys, os, pdb
# Analysis
import pandas as pd
import numpy as np
from math import *

'''
Name: bin_functions.py
Description: Functions that deal with binning and then graphing data
'''

# From http://stackoverflow.com/questions/26248654/numpy-return-0-with-divide-by-zero
def div0( a, b ):
    """ Function to divide arrays by zero and not have an error/warning thrown """
    with np.errstate(divide='ignore', invalid='ignore'):
        c = np.true_divide( a, b )
        c[ ~ np.isfinite( c )] = 0  # -inf inf NaN
    return c

def BarArray(pvalues, x_ar, use_zeros=True):
    """
        Inputs:  
        Outputs: 
    """
    p_ar = np.unique(pvalues)
    pmax = np.amax(p_ar)
    pmin = np.amin(p_ar)
    bar_num = len(p_ar)
    bar_width = (pmax-pmin)/float(2*bar_num) # make the width of the bars half the
                                           # width of the separation between bars
    bar_mean = np.zeros(bar_num)
    bar_error = np.zeros(bar_num)
    bar_edges = p_ar - .5*bar_width
    bar_n = np.zeros(bar_num)
    # if bar_width == 0: 
    #     bar_width = 1.0
    #     bar_edges = p_ar 
    # else: bar_edges = p_ar - .5*bar_width

    for p, x in zip(pvalues, x_ar):
        if (not use_zeros and x == 0):
            continue

        for j in range(bar_num-1):
            if p == p_ar[j]:
                bar_mean[j] += x # Weight by the inverse varience
                bar_n[j] += 1
                break
            elif j == bar_num - 2:
                bar_mean[j+1] += x 
                bar_n[j+1] += 1

    bar_mean = np.nan_to_num(np.divide(bar_mean, bar_n))

    for p, x in zip(pvalues, x_ar):
        if (not use_zeros and x == 0):
            continue
        for j in range(bar_num-1):
            if p == p_ar[j]:
                bar_error[j] += (bar_mean[j]-x)**2 # Weight by the inverse varience
                break
            elif j == bar_num - 2:
                bar_error[j+1] += (bar_mean[j+1]-x)**2 
    bar_error = div0(np.sqrt(bar_error), bar_n)
    bar_max = np.max(bar_n)

    return (bar_mean, bar_error, bar_edges, bar_n, bar_width, bar_max) 

def BinomialBarArray(pvalues, x_ar, use_zeros=True):
    """
        Inputs:  
        Outputs: 
    """
    # pdb.set_trace()
    p_ar = np.unique(pvalues)
    pmax = np.amax(p_ar)
    pmin = np.amin(p_ar)
    bar_num = len(p_ar)
    bar_width = (pmax-pmin)/float(2*bar_num) # make the width of the bars half the
                                           # width of the separation between bars
    bar_edges = p_ar - .5*bar_width
    if bar_width == 0: bar_width = 1
    bar_mean = np.zeros(bar_num)
    bar_error = np.zeros(bar_num)
    bar_n = np.zeros(bar_num)
    # Get statistics
    if bar_num == 1: # If there is only one p_value given
        bar_n[0] = pvalues.shape[0]
        bar_max = bar_n[0]
        bar_mean[0] = x_ar.sum()
    else:
        for p, x in zip(pvalues, x_ar):
            #Find which bar it belongs too
            if (not use_zeros and x == 0):
                continue
            for j in range(bar_num-1):
                if p == p_ar[j]:
                    bar_mean[j] += x 
                    bar_n[j] += 1
                    break
                elif j == bar_num - 2:
                    bar_mean[j+1] += x 
                    bar_n[j+1] += 1

        bar_max = np.max(bar_n)
    for i in range(bar_num):
        bar_error[i] = BinomialError(bar_mean[i], bar_n[i])

    bar_mean = np.nan_to_num(np.divide(bar_mean, bar_n))

    return (bar_mean, bar_error, bar_edges, bar_n, bar_width, bar_max) 

def WeightedBinArray(pvalues, x_ar, error_ar, bin_num, use_zeros = True):
    """
        Inputs:  
        Outputs: 
    """
    l = x_ar.size
    pmax = np.amax(pvalues)
    pmin = np.amin(pvalues)
    bin_width = (pmax-pmin)/float(bin_num)
    w_ar = np.zeros(l)
    w_ar = 1.0/(error_ar**2)
    bin_w = np.zeros(bin_num)
    bin_n = np.zeros(bin_num, dtype=float)
    bin_mean = np.zeros(bin_num)
    bin_error = np.zeros(bin_num)
    bin_edges = np.linspace(pmin, pmax, bin_num)

    for p, x, i in zip(pvalues, x_ar, list(range(l))):
        #Find which bin it belongs too
        if ((not use_zeros and x == 0) or error_ar[i] == 0):
            continue
        for j in range(bin_num-1):
            if p >= bin_edges[j] and p < bin_edges[j+1]:
                bin_w[j] += w_ar[i]
                bin_mean[j] += w_ar[i]*x # Weight by the inverse varience
                bin_n[j] += 1
                break
            elif j == bin_num - 2:
                bin_mean[j+1] += x*w_ar[i]

    for m, w in zip(bin_mean, bin_w): 
        if w == 0: m = 0
        else: m /= w

    for p, x, i in zip(pvalues, x_ar, list(range(l))): 
        if (not use_zeros and (x == 0 or w_ar[i] == 0)):
            continue
        for j in range(bin_num-1):
            if p >= bin_edges[j] and p < bin_edges[j+1]:
                bin_error[j] += (x - bin_mean[j])**2 * w_ar[i]
                break
            elif j == bin_num -1:
                bin_error[j+1] += (x - bin_mean[j+1])**2 * w_ar[i]

    for s, w, n in zip(bin_error, bin_w, bin_n):
        if w == 0 or n == 1: s = 0
        else: s *= float(n)/(float(n-1)*w)

    return (bin_mean, bin_error, bin_edges, bin_width, bin_n) 

def BinArray(pvalues, x_ar, bin_num, use_zeros = True):
    """
        Inputs:  
        Outputs: 
    """
    pmax = np.amax(pvalues)
    pmin = np.amin(pvalues)
    bin_width = (pmax-pmin)/float(bin_num)
    bin_n = np.zeros(bin_num, dtype=float)
    bin_mean = np.zeros(bin_num)
    bin_error = np.zeros(bin_num)
    bin_edges = np.linspace(pmin, pmax, bin_num, endpoint=False)

    for p, x in zip(pvalues, x_ar):
        #Find which bin it belongs too
        if (not use_zeros and x == 0):
            continue
        for j in range(bin_num-1):
            if p >= bin_edges[j] and p <= bin_edges[j+1]:
                bin_mean[j] += x # Weight by the inverse varience
                bin_n[j] += 1
                break
            elif j == bin_num - 2:
                bin_mean[j+1] += x 
                bin_n[j+1] += 1

    # bin_mean = np.nan_to_num(np.divide(bin_mean, bin_n))
    bin_mean = div0(bin_mean, bin_n)

    for p, x in zip(pvalues, x_ar):
        if (not use_zeros and x == 0):
            continue
        for j in range(bin_num-1):
            if p >= bin_edges[j] and p < bin_edges[j+1]:
                bin_error[j] += (bin_mean[j]-x)**2 # Weight by the inverse varience
                break
            elif j == bin_num - 2:
                bin_error[j+1] += (bin_mean[j+1]-x)**2 

    # bin_error = np.nan_to_num(np.divide(np.sqrt(np.divide(bin_error, bin_n)), np.sqrt(bin_n-1.0)))
    bin_error = div0(np.sqrt(bin_error), bin_n)
    # bin_error = np.nan_to_num(np.divide(np.sqrt(bin_error), bin_n)) 
    bin_max = np.max(bin_n)

    return (bin_mean, bin_error, bin_edges, bin_n, bin_width, bin_max) 

def BinomialBinArray(pvalues, x_ar, bin_num, use_zeros = True):
    """
        Inputs:  
        Outputs: 
    """
    pmax = np.amax(pvalues)
    pmin = np.amin(pvalues)
    bin_width = (pmax-pmin)/float(bin_num)
    bin_n = np.zeros(bin_num, dtype=float)
    bin_mean = np.zeros(bin_num)
    bin_error = np.zeros(bin_num)
    bin_edges = np.linspace(pmin, pmax, bin_num, endpoint=False)

    for p, x in zip(pvalues, x_ar):
        #Find which bin it belongs too
        if (not use_zeros and x == 0):
            continue
        for j in range(bin_num-1):
            if p >= bin_edges[j] and p <= bin_edges[j+1]:
                bin_mean[j] += x # Weight by the inverse varience
                bin_n[j] += 1
                break
            elif j == bin_num - 2:
                bin_mean[j+1] += x 
                bin_n[j+1] += 1

    bin_max = np.max(bin_n)
    for i in range(bin_num):
        bin_error[i] = BinomialError(bin_mean[i], bin_n[i])

    bin_mean = div0(bin_mean, bin_n) 

    return (bin_mean, bin_error, bin_edges, bin_n, bin_width, bin_max) 

def BinomialError(x, n):
    """ Get the standard error of the mean for a binomial variable given number 
        of success and total observations.
        Inputs:  x = number of successes observed
                 n = number of total possible successes
        Outputs: Calculated standard error of the mean
    """
    x = float(x) # Total number of successes
    n = float(n) # Total number of possible successes
    if n == 0:
        return 0
    if x == 0 or n == x:
        return sqrt((x+.5)/(n+1.0)*(1.0-(x+.5)/(n+1.0))/(n+1.0))
    else:
        return sqrt((x*n-x**2)/(n**3))

def WeightedMeanError(x, xerr):
    """ Return the weighted average and error on the inputs
    """
    n = len(x)
    if n != len(xerr):
        print("ERROR in WeightedMeanError, don't have equal length arrays")
        return [0, 0]
    yi = 0.0
    sigma2 = 0.0
    for i in range(n):
        yi += x[i]/(xerr[i]*xerr[i])
        sigma2 += 1.0/(xerr[i]*xerr[i])
    sigma2 = 1.0/sigma2
    sigma = np.sqrt(sigma2)
    mu = yi*sigma2
    return [mu, sigma]


##########################################
# if __name__ == "__main__":
    # print "Not implemented yet"




