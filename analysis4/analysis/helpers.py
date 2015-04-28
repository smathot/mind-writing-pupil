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

from exparser.DataMatrix import DataMatrix

def _filter(dm):

	# Participants 1 and 5 dropped out voluntarily
	dm = dm.select('subject_nr != 5')
	dm = dm.select('subject_nr != 1')
	for i in dm.range():
		# Remap participants 11 and 12 to 1 and 5
		if dm['subject_nr'][i] == 11:
			dm['subject_nr'][i] = 1
		if dm['subject_nr'][i] == 12:
			dm['subject_nr'][i] = 5
	dm = dm.select('free_writing_result != "ECRITURE"')
	dm = dm.select('free_writing_result != "ECRIRE"')
	return dm

def descriptives(dm):

	l = [['pp', 'rt', 'rtn', 'resp', 'nchar', 'nresp']]
	for i in dm.range():
		sn, resp, rt = dm['subject_nr'][i], dm['full_response'][i], \
			dm['free_writing_time'][i]
		rt = rt / 1000.
		rtn = rt / len(resp)
		print('%2d\t%.2f\t%.2f\t%s' % (sn, rt, rtn,
			dm['free_writing_result'][i]))
		resp = dm['free_writing_result'][i].replace('Space', ' ')
		l.append([sn, rt, rtn, resp, ])
	dm = DataMatrix(l)
	dm.sort('pp')
	print(dm)
