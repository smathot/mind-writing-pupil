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

def validatePhase(dm):

	if len(dm) == 0:
		print('*** Phase missing')
		return False
	phase = dm['phase'][0]
	print('Validating phase %d' % phase)
	blocks = dm.unique('block')
	print('Blocks: %s' % blocks)
	if len(blocks) < 7:
		print('*** Too few blocks')
		return False
	elif len(blocks) > 13:
		print('*** Too many blocks')
		return False
	ok = True
	if list(blocks) != range(1, len(blocks)+1):
		print('*** Irregular blocks')
		ok = False
	# The gaze contingent block is last
	gcBlock = blocks[-1]
	_dm = dm.select('block == %d' % gcBlock, verbose=False)
	if _dm.unique('stabilize') != [1]:
		print('*** Gaze stabilization block missing')
		ok = False
	# Check whether gaze contingent mode was disabled for all other blocks
	for b in blocks:
		_dm = dm.select('block == %d' % b, verbose=False)
		if len(_dm) != 16:
			print('*** Block %d has length %d' % (b, len(_dm)))
			ok = False
	# Check whether gaze contingent mode was disabled for all other blocks
	for b in blocks[:-1]:
		_dm = dm.select('block == %d' % b, verbose=False)
		if _dm.unique('stabilize') != [0]:
			print('*** Gaze stabilization enabled in block %d' % b)
			ok = False
	# The last block is just before
	lBlock = blocks[-2]
	_dm = dm.select('block == %d' % lBlock, verbose=False)
	acc = _dm['correct'].mean()
	print('Accuracy on last block (%d): %.2f' % (lBlock, acc))
	if not (acc == 1 or acc >= .8 and lBlock == 12):
		print('*** Accuracy incorrect')
		ok = False
	return ok

def validateSubject(dm):

	subject_nr = dm['subject_nr'][0]
	print('\nValidating subject %d' % subject_nr)
	_dm = dm.select('phase == 1', verbose=False)
	ok1 = validatePhase(_dm)
	_dm = dm.select('phase == 2', verbose=False)
	ok2 = validatePhase(_dm)
	_dm = dm.select('phase == 3', verbose=False)
	ok3 = validatePhase(_dm)
	okAll = ok1 and ok2 and ok3
	return subject_nr, ok1, ok2, ok3, okAll

def validate(dm):

	if list(dm.unique('stabilize')) != [0,1]:
		print('*** Invalid stabilize values: %s' % dm.unique('stabilize'))
	print('Subjects: %s' % dm.unique('subject_nr'))
	if dm.unique('subject_nr') != range(1, 11):
		print('*** Subject numbers incorrect')
	l = [['pp', 'ok1', 'ok2', 'ok3', 'okAll']]
	for _dm in dm.group('subject_nr'):
		subject_nr, ok1, ok2, ok3, okAll = validateSubject(_dm)
		l.append([subject_nr, ok1, ok2, ok3, okAll])
	dm = DataMatrix(l)
	print(dm)
