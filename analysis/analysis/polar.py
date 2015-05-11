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

@yamldoc.validate
def performanceByPos(dm, color=blue[1], style='-'):

	"""
	desc:
		Creates polar plots of the performance for each location.

	arguments:
		dm:
			desc:	The data.
			type:	DataMatrix

	keywords:
		color:
			desc:	The line color.
			type:	str
		style:
			desc:	The line style.
			type:	str
	"""

	i = 1
	for phase in [1,2,3]:
		_dm = dm.select('phase == %d' % phase)
		if len(_dm) == 0:
			continue
		cm = _dm.collapse(['targetAngle'], 'correct')
		plt.subplot(3,2,i, polar=True); i+=1
		plt.ylim(0, 1)
		plt.yticks([0, .5, 1])
		r = cm['targetAngle']
		a = cm['mean']
		plt.polar(r, a, style, color=color)
		plt.polar([r[0],r[-1]], [a[0], a[-1]], style, color=color)
		cm = _dm.collapse(['targetAngle'], 'pruneRt')
		plt.subplot(3,2,i, polar=True); i+=1
		plt.ylim(0, 30000)
		plt.yticks([0, 15000, 30000], [0, 15, 30])
		r = cm['targetAngle']
		a = cm['mean']
		plt.polar(r, a, style, color=color)
		plt.polar([r[0],r[-1]], [a[0], a[-1]], style, color=color)

@yamldoc.validate
def performanceByPosAndSubject(dm):

	"""
	desc:
		Creates polar plots of the performance for each location, for individual
		participants as well as the mean.

	arguments:
		dm:
			desc:	The data.
			type:	DataMatrix
	"""

	Plot.new()
	dm = dm.select('stabilize == 0')
	for subject_nr, _dm in dm.walk('subject_nr'):
		color = colors.pop()
		performanceByPos(_dm, color)
	_dm = dm.select('block <= 6')
	performanceByPos(_dm, 'black', style='o-')
	Plot.save('performanceByPosAndSubject')
