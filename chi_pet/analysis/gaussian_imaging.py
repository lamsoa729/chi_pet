#!/usr/bin/env python

import sys, os, pdb
import numpy as np
from scipy import special

def GaussianSpot2D(x, y, A, sigma, x0, y0):
    term0 = np.square(y - y0) + np.square(x-x0)
    z = A*np.exp(-term0/(2*sigma*sigma))

    return z

def GaussianLine2D(x, y, A, sigma, x0, y0, L, theta):
    term0 = (y-y0)*np.cos(theta)+(x0-x)*np.sin(-theta)
    expterm = A*np.exp(-term0*term0/(2*sigma*sigma))
    erfterm = (special.erf((L+(x0-x)*np.cos(theta)+(y0-y)*np.sin(-theta))/(np.sqrt(2)*sigma)) \
             - special.erf(((x0-x)*np.cos(theta)+(y0-y)*np.sin(-theta))/(np.sqrt(2)*sigma)))

    z = expterm*erfterm
    return z

def GaussianLine3D(A,sigmaxy,sigmaz,x,y,z,x0,y0,z0,x1,y1,z1):
    # Define lengths
    Lx = x1 - x0
    Ly = y1 - y0
    Lz = z1 - z0

    # Define shifts in coordinates
    xeff = x - x0
    yeff = y - y0
    zeff = z - z0

    # Gaussian terms
    expterm1 = Lz**2 * (xeff**2 + yeff**2) * sigmaxy**2
    expterm2 = -2*Lz * (Lx*xeff + Ly*yeff)*zeff * sigmaxy**2
    expterm3 = (Lx**2 + Ly**2)*(zeff**2)*sigmaxy**2
    expterm4 = (Ly*xeff - Lx*yeff)**2*sigmaz**2
    expdenom = 2*Lz**2*sigmaxy**4 + 2*(Lx**2 + Ly**2)*sigmaxy**2*sigmaz**2
    
    expterm = np.exp(-(expterm1+expterm2+expterm3+expterm4)/expdenom)

    # Erf terms
    erfdenom = sigmaxy * sigmaz * np.sqrt(2*Lz**2*sigmaxy**2 + 2*(Lx**2 + Ly**2)*sigmaz**2)
    erf1top = -Lz*zeff*sigmaxy**2 + (-Lx*xeff - Ly*yeff)*sigmaz**2
    erf2top = Lz*(Lz - zeff)*sigmaxy**2 + (Lx*(Lx - xeff) + Ly*(Ly - yeff))*sigmaz**2
    erf1 = special.erf(erf1top/erfdenom)
    erf2 = special.erf(erf2top/erfdenom)

    # Normalization term
    L = np.sqrt(Lx**2 + Ly**2 + Lz**2)
    normterm = A * L / (4 * np.pi * sigmaxy * np.sqrt(Lz**2 * sigmaxy**2 + Lx**2 * sigmaz**2 + Ly**2 * sigmaz**2))

    zret = normterm * expterm *(-erf1 + erf2)

    return zret
