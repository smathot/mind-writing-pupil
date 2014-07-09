#-*- coding:utf-8 -*-

"""
This file is part of P0014.1.

P0014.1 is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

P0014.1 is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with P0014.1.  If not, see <http://www.gnu.org/licenses/>.
"""

import os
import sys
from exparser import TraceKit as tk
from exparser import Plot
from exparser.TangoPalette import *
from exparser.Cache import cachedDataMatrix
from exparser.PivotMatrix import PivotMatrix
from yamldoc import validate
from matplotlib import pyplot as plt
from scipy.stats import nanmean, nanstd
import warnings
import numpy as np

show = '--silent' not in sys.argv
brightColor = orange[1]
darkColor = blue[1]

@validate
def getTraceAvg(traceLen=1350, filters=[]):

	"""
	desc:
		Gets the average pupil-size trace for a selection of trials.

	keywords:
		traceLen:
			desc:	The length of the output trace.
			typee:	int
		filters:
			desc:	A list of words that should be part of the trace filename.
			type:	list

	returns:
		desc:	A 2D array with the mean and std of the trace.
		type:	ndarray
	"""

	i = 0
	l = []
	for path in os.listdir('traces'):
		process = True
		for _filter in filters:
			if _filter not in path:
				process = False
				break
		if not process:
			continue
		a = np.load('traces/%s' % path)[:,2][:traceLen]
		b = np.empty(traceLen)
		b[:] = np.nan
		b[:len(a)] = a
		l.append(b)
	c = np.array(l)
	return np.array( [nanmean(c, axis=0), nanstd(c, axis=0)] )

@validate
def pupilPlot(dm):

	"""
	desc:
		Creates the overall pupil-size plot for switch-to-bright and
		switch-to-dark rounds.

	arguments:
		dm:
			desc:	A DataMatrix.
			type:	DataMatrix
	"""

	traceLen = dm['endCollectionTime'].mean()
	mBright = getTraceAvg(traceLen=traceLen, filters=['bright'])
	mDark = getTraceAvg(traceLen=traceLen, filters=['dark'])
	xData = np.linspace(0, mBright.shape[1]-1, mBright.shape[1])
	plt.fill_between(xData, mBright[0]-mBright[1], mBright[0]+mBright[1], alpha=.25,
		color=brightColor)
	plt.fill_between(xData, mDark[0]-mDark[1], mDark[0]+mDark[1], alpha=.25,
		color=darkColor)
	plt.plot(mBright[0], color=brightColor)
	plt.plot(mDark[0], color=darkColor)
	plt.axvline(dm['endInvertTime'].mean(), color='black', linestyle='--')
	plt.axvline(dm['endAdaptationTime'].mean(), color='black', linestyle='--')
	plt.xlabel('Time since round start (ms)')
	plt.ylabel('Mean pupil area')
	plt.xlim(0, traceLen)
	plt.show()

@validate
def behavior(dm):

	"""
	desc:
		Analyzes accuracy and response times.

	arguments:
		dm:
			desc:	A DataMatrix.
			type:	DataMatrix
	"""

	print dm.collapse(['mode2'], vName='rt')
	print dm.collapse(['mode2'], vName='rounds')
