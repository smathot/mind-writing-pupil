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
from exparser.Cache import cachedDataMatrix
from exparser.PivotMatrix import PivotMatrix
from yamldoc import validate
from matplotlib import pyplot as plt
from scipy.stats import nanmean, nanstd
import warnings
import numpy as np
from constants import *

@validate
def _filter(dm):

	"""
	desc:
		Performs some preprocessing on the DataMatrix.

	arguments:
		dm:
			desc:	A DataMatrix.
			type:	DataMatrix

	returns:
		desc:	A filtered DataMatrix.
		type:	DataMatrix
	"""

	for i in dm.range():
		_file = dm['file'][i]
		subject_nr1 = dm['subject_nr'][i]
		subject_nr2 = int(_file[5:7])
		if subject_nr1 != subject_nr2:
			warnings.warn(u'Subject nr mismatch (%d - %d) in %s' \
				% (subject_nr1, subject_nr2, _file))
		dm['subject_nr'][i] = subject_nr2
	return dm

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



