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

from constants import *
from yamldoc import validate

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
