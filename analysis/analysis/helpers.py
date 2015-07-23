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

	"""
	desc:
		Performance various preprocessing on the data, notably remapping
		participant numbers and removing dropped-out participants.

	arguments:
		dm:
			desc:	The data.
			type:	DataMatrix

	returns:
		desc:	Filtered data.
		type:	DataMatrix
	"""

	# Participants 1 and 5 dropped out voluntarily
	dm = dm.select('subject_nr != 5')
	dm = dm.select('subject_nr != 1')
	for i in dm.range():
		# Remove phase 2 of participant 8, because it was the redo of phase 1
		if dm['subject_nr'][i] == 8 and dm['phase'][i] == 2:
			dm['subject_nr'][i] = -1
	# Remap participants
	# Tested 11 -> 1
	# Tested 12 -> 5
	# Tested 10 -> 8
	# Tested 8 -> 10
	dm.recode('subject_nr', [(11, 1), (12, 5), (10, 99)])
	dm.recode('subject_nr', [(8, 10), (99, 8)])
	dm = dm.select('subject_nr > 0')
	dm = dm.select('correct != "NA"')
	print('N(trials) = %d' % len(dm))
	# The duration of the animation was 1.185 seconds, and this should not be
	# included in the RT
	dm['loop_rt'] -= 1.185
	return dm

@yamldoc.validate
def descriptives(dm):

	"""
	desc:
		Gives descriptives results of performance.

	arguments:
		dm:
			desc:	The data.
			type:	DataMatrix
	"""

	dm = dm.select('stabilize == 0')
	for phase in (1,2,3):
		_dm = dm.select('phase == %d' % phase)
		pm = PivotMatrix(_dm, ['subject_nr'], ['subject_nr'], dv='correct')
		pm._print(u'Accuracy phase %d' % phase, sign=4)
		pm.save('output/acc.phase%d.csv' % phase)
		pm = PivotMatrix(_dm, ['subject_nr'], ['subject_nr'], dv='loop_rt')
		pm._print(u'Response time phase %d' % phase, sign=4)
		pm.save('output/rt.phase%d.csv' % phase)
