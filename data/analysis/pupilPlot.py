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
import numpy as np
from scipy.stats import nanmean, nanstd
from constants import *
from yamldoc import validate
from exparser import TraceKit as tk
from exparser import Plot
from matplotlib import pyplot as plt

@validate
def getTraceAvg(dm, traceLen=1350, rnd=rndRange, phaseTypes=['bright', 'dark']):

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
	for i in dm.range():
		for rnd in rndRange:
			for phaseType in phaseTypes:
				path = 'traces/%s-%s-%04d-%04d-%s.npy' \
					% (dm['file'][i][4:-5], dm['file'][i][-5:-4],
					dm['trialId'][i], rnd, phaseType)
				if not os.path.exists(path):
					continue
				print path
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
	traceLen = int(dm['endCollectionTime'].mean())
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
	for _dm in dm.group('subject_nr'):
		plt.subplot(1, dm.count('subject_nr'), i)
		pupilPlot(_dm)
		i += 1
	Plot.save('pupilPlotSubject', show=show)

@validate
def pupilPlotEcc(dm):

	"""
	desc:
		Creates the overall pupil-size plot for switch-to-bright and
		switch-to-dark rounds, separately for each subject.

	arguments:
		dm:
			desc:	A DataMatrix.
			type:	DataMatrix
	"""

	i = 1
	for ecc in dm.unique('ecc'):
		for subject_nr in dm.unique('subject_nr'):
			_dm = dm.select('ecc == %d' % ecc) \
				.select('subject_nr == %s' % subject_nr)
			plt.subplot(dm.count('ecc'), dm.count('subject_nr'), i)
			plt.title('%d - %d' % (subject_nr, ecc))
			pupilPlot(_dm)
			i += 1
	Plot.save('pupilPlotEcc', show=show)

@validate
def pupilPlotSize(dm):

	"""
	desc:
		Creates the overall pupil-size plot for switch-to-bright and
		switch-to-dark rounds, separately for each subject.

	arguments:
		dm:
			desc:	A DataMatrix.
			type:	DataMatrix
	"""

	i = 1
	for size in dm.unique('size'):
		for subject_nr in dm.unique('subject_nr'):
			_dm = dm.select('size == %d' % size) \
				.select('subject_nr == %s' % subject_nr)
			plt.subplot(dm.count('size'), dm.count('subject_nr'), i)
			plt.title('%d - %d' % (subject_nr, size))
			pupilPlot(_dm)
			i += 1
	Plot.save('pupilPlotSize', show=show)

@validate
def pupilPlotBgLum(dm):

	"""
	desc:
		Creates the overall pupil-size plot for switch-to-bright and
		switch-to-dark rounds, separately for each subject.

	arguments:
		dm:
			desc:	A DataMatrix.
			type:	DataMatrix
	"""

	i = 1
	for bgLum in dm.unique('bgLum'):
		for subject_nr in dm.unique('subject_nr'):
			_dm = dm.select('bgLum == %f' % bgLum) \
				.select('subject_nr == %s' % subject_nr)
			plt.subplot(dm.count('bgLum'), dm.count('subject_nr'), i)
			plt.title('%d - %f' % (subject_nr, bgLum))
			pupilPlot(_dm)
			i += 1
	Plot.save('pupilPlotBgLum', show=show)
