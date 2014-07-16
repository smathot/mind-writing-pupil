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
def pupilPlot(dm, filters=[]):

	"""
	desc:
		Creates the overall pupil-size plot for switch-to-bright and
		switch-to-dark rounds.

	arguments:
		dm:
			desc:	A DataMatrix.
			type:	DataMatrix

	keywords:
		filters:
			desc:	Filters
			type:	list
	"""

	assert(dm.count('subject_nr') == 1)
	traceLen = dm['endCollectionTime'].mean()
	mBright = getTraceAvg(traceLen=traceLen, filters=['bright']+filters)
	mDark = getTraceAvg(traceLen=traceLen, filters=['dark']+filters)
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
	#plt.show()

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
		f = 'P%02d'%_dm['subject_nr'][0]
		print f
		pupilPlot(_dm, filters=[f])
		i += 1
	plt.show()

@validate
def evolution(dm):

	"""
	desc:
		Determines accuracy and speed as a function of threshold.

	arguments:
		dm:
			desc:	A DataMatrix.
			type:	DataMatrix
	"""

	import pickle

	if 'likelihoodThr' in dm:
		maxLikelihood = dm['likelihoodThr'][0]
	else:
		# In Exp 1 this wasn't logged yet.
		maxLikelihood = 2
	steps = 100
	maxRnd = 100
	aThr = np.linspace(1.05, maxLikelihood, steps)
	aAcc = np.empty((len(dm), steps))
	aRnd = np.empty((len(dm), steps))
	aRat = np.empty((len(dm), maxRnd))
	aRat[:] = np.nan
	for i in dm.range():
		print 'Trial %d' % i
		d = pickle.load(open(dm['__likelihood__'][i]))
		# Create an array with the mean likelihood
		l = []
		for _id in d:
			l.append(d[_id])
		a = np.array(l, dtype=float)
		m = np.mean(a, axis=0)
		# Array with target likelihood
		t = np.array(d['target'], dtype=float)
		# Array with the mean distractor likelihood
		for _id in d:
			if _id != 'target':
				dist = np.array(d[_id], dtype=float)
			a = np.array(d[_id], dtype=float)
		ratio = t / dist
		if len(ratio) >= maxRnd:
			aRat[i] = ratio[:maxRnd]
		else:
			aRat[i,:len(ratio)] = ratio
		for j in range(steps):
			thr = aThr[j]
			iHit = np.where(ratio > thr)[0]
			rnd = iHit[0]
			iErr = np.where(ratio < 1/thr)[0]
			correct = 1
			if len(iErr) > 0:
				if iErr[0] < iHit[0]:
					correct = 0
					rnd = iErr[0]
			aAcc[i,j] = correct
			aRnd[i,j] = rnd
	Plot.new()
	plt.subplot(311)
	plt.plot(np.arange(maxRnd), np.swapaxes(aRat, 0, 1), alpha=.1,
		color=gray[1])
	plt.plot(np.arange(maxRnd), nanmean(aRat, axis=0), color=blue[1])
	plt.xlabel('Round')
	plt.ylabel('Ratio')
	plt.subplot(312)
	plt.plot(aThr, aAcc.mean(axis=0), color=blue[1])
	plt.xlabel('Ratio threshold')
	plt.ylabel('Accuracy')
	plt.subplot(313)
	plt.plot(aThr, np.swapaxes(aRnd, 0, 1), alpha=.1, color=gray[1])
	plt.plot(aThr, aRnd.mean(axis=0), color=blue[1])
	plt.xlabel('Ratio threshold')
	plt.ylabel('Rounds until decision')
	Plot.save('evolution', show=show)

@validate
def performance(dm, lDv):

	"""
	desc:
		Analyzes accuracy and response times.

	arguments:
		dm:
			desc:	A DataMatrix.
			type:	DataMatrix
		lDv:
			desc:	A list of dependent variables to split performance by.
			type:	list
	"""

	print dm.collapse(['subject_nr']+lDv, vName='rt')
	print dm.collapse(['subject_nr']+lDv, vName='rounds')

@validate
def performanceMode2(dm):

	"""
	desc:
		Analyzes accuracy and response times per mode 2. For Exp 1.

	arguments:
		dm:
			desc:	A DataMatrix.
			type:	DataMatrix
	"""

	performance(dm, ['mode2'])

@validate
def performanceEcc(dm):

	"""
	desc:
		Analyzes accuracy and response times per ecc. For Exp 2.

	arguments:
		dm:
			desc:	A DataMatrix.
			type:	DataMatrix
	"""

	performance(dm, ['ecc'])

