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

from exparser.TangoPalette import *
import os
import numpy as np
from scipy.stats import nanmean, nanstd
from yamldoc import validate
from exparser import Plot
from matplotlib import pyplot as plt
import sys

show = '--silent' not in sys.argv
brightColor = orange[1]
darkColor = blue[1]
rndRange = range(10000)
traceLen = 1250

def check(dm):

	for i in dm.range():
		if dm['subject_nr'][i] == 0:
			dm['subject_nr'][i] = 4
		f = dm['file'][i]
		s = 'PP%02d' % dm['subject_nr'][i]
		assert(f.startswith(s))
	return dm

@validate
def getTraceAvg(dm, traceLen=1250, rnd=rndRange, phaseTypes=['bright', 'dark']):

	"""
	desc:
		Gets the average pupil-size trace for a selection of trials.

	arguments:
		dm:
			desc:	A DataMatrix.
			type:	DataMatrix

	keywords:
		traceLen:
			desc:	The length of the output trace.
			type:	int
		rnd:
			desc:	A list of round numbers to be included.
			type:	list
		phaseTypes:
			desc:	A list of phase types, which can be bright or dark.
			type:	list

	returns:
		desc:	A 2D array with the mean and std of the trace.
		type:	ndarray
	"""

	l = []
	for rnd in rndRange:
		for phaseType in phaseTypes:
			path = 'traces/subject%0d-%04d-%s.npy' % \
				(dm['subject_nr'][0], rnd, phaseType)
			if not os.path.exists(path):
				continue
			a = np.load(path)[:,2][:traceLen]
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

	assert(dm.count('subject_nr') == 1)
	mBright = getTraceAvg(dm, traceLen=traceLen, phaseTypes=['bright'])
	mDark = getTraceAvg(dm, traceLen=traceLen, phaseTypes=['dark'])
	xData = np.linspace(0, mBright.shape[1]-1, mBright.shape[1])
	plt.fill_between(xData, mBright[0]-mBright[1], mBright[0]+mBright[1],
		alpha=.25, color=brightColor)
	plt.fill_between(xData, mDark[0]-mDark[1], mDark[0]+mDark[1], alpha=.25,
		color=darkColor)
	plt.plot(mBright[0], color=brightColor)
	plt.plot(mDark[0], color=darkColor)
	plt.axvline(dm['endInvertTime'].mean(), color='black', linestyle='--')
	plt.axvline(dm['endAdaptationTime'].mean(), color='black', linestyle='--')
	plt.xlabel('Time since round start (ms)')
	plt.ylabel('Mean pupil area')
	plt.xlim(0, traceLen)

def pupilDiffPlot(dm, label=None):

	assert(dm.count('subject_nr') == 1)
	traceLen = int(dm['endCollectionTime'].mean())
	mBright = getTraceAvg(dm, traceLen=traceLen, phaseTypes=['bright'])
	mDark = getTraceAvg(dm, traceLen=traceLen, phaseTypes=['dark'])
	plt.plot(mBright[0] - mDark[0], label=label)

@validate
def pupilDiffPlotSubject(dm):

	"""
	desc:
		Creates the overall pupil-size plot for switch-to-bright and
		switch-to-dark rounds, separately for each subject.

	arguments:
		dm:
			desc:	A DataMatrix.
			type:	DataMatrix
	"""

	i = 0
	Plot.new(size=Plot.s)
	for subject_nr, _dm in dm.walk('subject_nr'):
		t = 'pp %s (N=%d)' % (subject_nr, len(_dm))
		print(t)
		pupilDiffPlot(_dm, label=str(subject_nr))
		i += 1
	plt.axvline(dm['endInvertTime'].mean(), color='black', linestyle='--')
	plt.axvline(dm['endAdaptationTime'].mean(), color='black', linestyle='--')
	plt.axhline(0, color='black', linestyle='-')
	plt.xlabel('Time since round start (ms)')
	plt.ylabel('Mean pupil area')
	plt.xlim(0, traceLen)
	plt.legend(frameon=False)
	Plot.save('pupilDiffPlotSubject', show=show)

@validate
def pupilPlotExample(dm):

	"""
	desc:
		Creates the overall pupil-size plot for switch-to-bright and
		switch-to-dark rounds for participant 10.

	arguments:
		dm:
			desc:	A DataMatrix.
			type:	DataMatrix
	"""

	dm = dm.select('subject_nr == 10')
	Plot.new(size=Plot.s)
	pupilPlot(dm)
	Plot.save('pupilPlotExample', show=show)

@validate
def pupilPlotSubject(dm):

	"""
	desc:
		Creates the overall pupil-size plot for switch-to-bright and
		switch-to-dark rounds, separately for each subject.

	arguments:
		dm:
			desc:	A DataMatrix.
			type:	DataMatrix
	"""

	i = 0
	Plot.new(Plot.xl)
	for subject_nr, _dm in dm.walk('subject_nr'):
		t = 'pp %s (N=%d)' % (subject_nr, len(_dm))
		print(t)
		plt.subplot(2, dm.count('subject_nr')/2, i)
		plt.title(t)
		pupilPlot(_dm)
		i += 1
	Plot.save('pupilPlotSubject', show=show)
