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
from exparser import Math
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
rndRange = range(100)

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

	if 'likelihoodThr' in dm.columns():
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
			iHit = np.where(ratio >= thr)[0]
			iErr = np.where(ratio <= 1/thr)[0]
			if len(iHit) == 0:
				correct = 0
				rnd = iErr[0]
			elif len(iErr) > 0 and iErr[0] < iHit[0]:
				correct = 0
				rnd = iErr[0]
			else:
				correct = 1
				rnd = iHit[0]
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
		Analyzes accuracy and response times as a function of specified
		dependent variables.

	arguments:
		dm:
			desc:	A DataMatrix.
			type:	DataMatrix
		lDv:
			desc:	A list of dependent variables to split performance by.
			type:	list
	"""

	cm = dm.select('correct == 0').collapse(['subject_nr']+lDv, vName='correct')
	cm.save('output/performance.n_error.subject_nr.%s.csv' % ('.'.join(lDv)))
	print cm
	cm = dm.collapse(['subject_nr']+lDv, vName='correct')
	cm.save('output/performance.acc.subject_nr.%s.csv' % ('.'.join(lDv)))
	print cm
	cm = dm.collapse(lDv, vName='correct')
	cm.save('output/performance.acc.%s.csv' % ('.'.join(lDv)))
	print cm
	cm = dm.collapse(['subject_nr']+lDv, vName='rt')
	cm.save('output/performance.rt.subject_nr.%s.csv' % ('.'.join(lDv)))
	print cm
	cm = dm.collapse(lDv, vName='rt')
	cm.save('output/performance.rt.%s.csv' % ('.'.join(lDv)))
	print cm
	cm = dm.collapse(['subject_nr']+lDv, vName='rounds')
	cm.save('output/performance.rounds.subject_nr.%s.csv' % ('.'.join(lDv)))
	print cm
	cm = dm.collapse(lDv, vName='rounds')
	cm.save('output/performance.rounds.%s.csv' % ('.'.join(lDv)))
	print cm

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

@validate
def performanceSize(dm):

	"""
	desc:
		Analyzes accuracy and response times per ecc. For Exp 3.

	arguments:
		dm:
			desc:	A DataMatrix.
			type:	DataMatrix
	"""

	performance(dm, ['size'])

@validate
def fixation(dm):

	"""
	desc:
		Analyzes fixation stability.

	arguments:
		dm:
			desc:	A DataMatrix.
			type:	DataMatrix
	"""

	Plot.new()
	plt.subplot(211, polar=True)
	a, r = Math.angleMean(np.radians(dm['errA']), dm['errR'])
	plt.polar(np.radians(dm['errA']), dm['errR'], ',', color=blue[1])
	plt.polar([0,a], [0, r], '-', color=orange[1])

	plt.subplot(212, polar=True)
	stepSize = 15
	aData = []
	rData = []
	for a in range(0, 360, stepSize):
		_dm = dm.select('errA >= %d' % a, verbose=False)
		_dm = _dm.select('errA < %d' % (a+stepSize), verbose=False)
		rnd = _dm['rounds'].mean()
		print('a = %d, N = %d, rnd = %.2f' % (a, len(_dm), rnd))
		aData.append(np.radians(a+stepSize/2))
		rData.append(rnd)
	plt.polar(aData, rData, 'o-', color=orange[1])
	Plot.save('fixation', show=True)



