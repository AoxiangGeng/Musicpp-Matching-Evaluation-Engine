#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 15:47:13 2019

@author: alex
"""

import sys
import numpy as np
import py_sonicvisualiser 

wavfname = 'sp_cut.wav'
outsvenvfname = 'sp.test.wav'

# init a sonic visualiser environment file corresponding
# to the analysis of media wavfname
#sve = SVEnv(wavfname)

# append a spectrogram view
specview = sve.add_spectrogram()

# append a continuous annotation layer corresponding to a sinusoidal signal
# on the spectrogram view previously defined
x = np.array(range(10000, 20000, 5)) / 1000.
sve.add_continuous_annotations(x, 1 + 3 * np.sin(2 * x), view=specview)

# append a labelled interval annotation layer on a new view
intvtime = [1., 5., 21.5]
intvdur = [3., 11., 5.]
intvlabel = ['myintv1', 'mywonderfull  intv2', 'intv3']
intvval = [0, 1, 5]
sve.add_interval_annotations(intvtime,intvdur,intvlabel,intvval)

# save the environment to a sonic visualiser environment file
sve.save(outsvenvfname)