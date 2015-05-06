#-*- coding:utf-8 -*-

"""
This file is part of P0015.

P0015 is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

P0015 is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with P0015.  If not, see <http://www.gnu.org/licenses/>.
"""

from analysis.constants import *
from analysis.tracePlot import subplot

@yamldoc.validate
def barPlot(dm, dv='correct', phase=1):

	"""
	desc:
		Creates a bar plot for one phase.

	arguments:
		dm:
			desc:	The data.
			type:	DataMatrix

	keywords:
		dv:
			desc:	The dependent variable.
			valid:	[correct, loop_rt]
		phase:
			desc:	The phase to analyze.
			valid:	[1,2,3]
	"""

	dm = dm.select('phase == %d' % phase)
	for _dm in dm.group('subject_nr'):
		y = _dm[dv].mean()
		x = int(_dm['subject_nr'][0])
		se = _dm[dv].std() / np.sqrt(len(_dm))
		plt.bar(x-.4, y, color=gray[1])
		plt.errorbar(x, y, yerr=se, color='black', capsize=0)
	dm = dm.select('block <= 6')
	y = dm[dv].mean()
	print('Overall y = %f' % y)
	x = -1
	se = _dm[dv].std() / np.sqrt(len(_dm))
	plt.bar(x-.4, y, color=blue[1])
	plt.errorbar(x, y, yerr=se, color='black', capsize=0)
	maxX = int(np.max(_dm['subject_nr']))+1
	plt.xlim(-2, maxX)
	plt.xticks(range(-1, maxX), ['Overall', ''] + range(1, maxX))

@yamldoc.validate
def fullBarPlot(dm):

	"""
	desc:
		Creates a full bar plot of the results.

	arguments:
		dm:
			desc:	The data.
			type:	DataMatrix
	"""

	Plot.new(Plot.w)
	for phase in [1,2,3]:
		subplot(dv='correct', phase=phase)
		barPlot(dm, phase=phase, dv='correct')
		subplot(dv='loop_rt', phase=phase)
		barPlot(dm.select('correct == 1'), phase=phase, dv='loop_rt')
		plt.xlabel('Participant')
	Plot.save('fullBarPlot')
