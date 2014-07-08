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

defaultTraceParams = {
	'signal'		: 'pupil',
	'lock'			: 'start',
	'phase'			: 'retention',
	'baseline'		: 'cue',
	'baselineLock'	: 'end',
	'traceLen'		: 5000
	}

show = '--silent' not in sys.argv
brightColor = orange[1]
darkColor = blue[1]

def getTraceAvg(_filter=None):

	traceLen = 1250
	i = 0
	l = []
	for path in os.listdir('traces'):
		if _filter != None and _filter not in path:
			continue
		a = np.load('traces/%s' % path)[:,2][:traceLen]
		b = np.empty(traceLen)
		b[:] = np.nan
		b[:len(a)] = a
		l.append(b)
	c = np.array(l)
	return nanmean(c, axis=0), nanstd(c, axis=0)


def pupilPlot(dm):

	mBright, stdBright = getTraceAvg('bright')
	mDark, stdDark = getTraceAvg('dark')
	plt.plot(mBright, color=brightColor)
	plt.plot(mDark, color=darkColor)
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

	#print dm
	#pm = PivotMatrix(dm, ['mode2'], ['mode2'], dv='rt')
	#pm._print('Response time')
	print dm.collapse(['mode2'], vName='rt')
	print dm.collapse(['mode2'], vName='rounds')
