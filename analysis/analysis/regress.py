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
def learningRegression(dm):

	"""
	desc:
		Performs regression analyses to test the effect of learning across
		blocks.

	arguments:
		dm:
			desc:	The data.
			type:	DataMatrix
	"""

	R = RBridge.R()
	for phase in [1,2,3]:
		_dm = dm.select('phase == %d' % phase, verbose=False)
		_dm = _dm.select('block <= 6', verbose=False)
		R.load(_dm)
		glm = R.glmerBinomial('correct ~ block + (1+block|subject_nr)')
		glm._print(sign=4, title='Phase %d (correct)' % phase)
		glm.save('output/glm.correct.phase%d.csv' % phase)
		lm = R.lmer('loop_rt ~ block + (1+block|subject_nr)')
		lm._print(sign=4, title='Phase %d (loop_rt)' % phase)
		lm.save('output/lm.loop_rt.phase%d.csv' % phase)

@yamldoc.validate
def baselinePupilSizeRegression(dm):

	"""
	desc:
		Performs regression analyses to test the effect of baseline pupil size
		on performance.

	arguments:
		dm:
			desc:	The data.
			type:	DataMatrix
	"""

	dm = dm.select('block <= 6', verbose=False)
	dm = dm.addField('baselinePupilSizeZ', dtype=float)
	dm = dm.withinize('baselinePupilSize', 'baselinePupilSizeZ', 'subject_nr',
		verbose=True, whiten=True)
	R = RBridge.R()
	R.load(dm)
	glm = R.glmerBinomial(
		'correct ~ baselinePupilSizeZ + (1+baselinePupilSizeZ|subject_nr)')
	glm._print(sign=4)
	glm.save('output/glm.correct.baselinePupilSizeZ.csv')
	lm = R.lmer(
		'loop_rt ~ baselinePupilSizeZ + (1+baselinePupilSizeZ|subject_nr)')
	lm._print(sign=4)
	lm.save('output/lm.loop_rt.baselinePupilSizeZ.csv')
