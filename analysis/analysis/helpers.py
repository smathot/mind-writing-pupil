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

def _filter(dm):

	#dm = dm.select('subject_nr != 8')

	"""
	PP01: Quit voluntarily
	PP05: Quit voluntarily
	PP08: Didn't make it, below 80% after restarting phase 1

	Remap PP11 to PP01
	Remap PP12 to PP05
	"""

	# Participants 1 and 5 dropped out voluntarily
	dm = dm.select('subject_nr != 5')
	dm = dm.select('subject_nr != 1')
	for i in dm.range():
		# Remove phase 2 of participant 8, because it was the redo of phase 1
		if dm['subject_nr'][i] == 8 and dm['phase'][i] == 2:
			dm['subject_nr'][i] = -1
		# Remap participants 11 and 12 to 1 and 5
		if dm['subject_nr'][i] == 11:
			dm['subject_nr'][i] = 1
		if dm['subject_nr'][i] == 12:
			dm['subject_nr'][i] = 5
	dm = dm.select('subject_nr > 0')
	dm = dm.select('correct != "NA"')
	return dm

def descriptives(dm):

	dm = dm.select('block <= 6')
	for phase in (1,2,3):
		_dm = dm.select('phase == %d' % phase)
		pm = PivotMatrix(_dm, ['subject_nr'], ['subject_nr'], dv='correct')
		pm._print(u'Accuracy phase %d' % phase, sign=4)
		pm = PivotMatrix(_dm, ['subject_nr'], ['subject_nr'], dv='loop_rt')
		pm._print(u'Response time phase %d' % phase, sign=4)
