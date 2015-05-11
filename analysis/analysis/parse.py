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


import os
import subprocess
from exparser.EyelinkAscFolderReader import EyelinkAscFolderReader
from exparser.Cache import cachedDataMatrix

class MyReader(EyelinkAscFolderReader):

	"""An experiment-specific reader to parse the EyeLink data files."""

	def initTrial(self, trialDict):

		"""
		desc:
			Performs pre-trial initialization.

		arguments:
			trialDict:
				desc:	Trial information.
				type:	dict
		"""

		self.stabilize = None
		self.baselinePupilSize = None

	def finishTrial(self, trialDict):

		"""
		desc:
			Performs post-trial initialization.

		arguments:
			trialDict:
				desc:	Trial information.
				type:	dict
		"""

		assert(self.stabilize is not None)
		assert(self.baselinePupilSize is not None)
		assert('targetAngle' in trialDict)
		assert('pruneRt' in trialDict)
		trialDict['stabilize'] = self.stabilize
		trialDict['baselinePupilSize'] = self.baselinePupilSize
		file = trialDict['file']
		subject_nr = int(file[2:4])
		phase = int(file[4:6])
		block = int(file[6:8])
		trialDict['phase'] = phase
		trialDict['block'] = block
		print(trialDict['subject_nr'])
		print(
			'%(file)s [subject %(subject_nr)s, phase %(phase)d, block %(block)d]' \
			% trialDict)
		if subject_nr != trialDict['subject_nr']:
			trialDict['subject_nr'] = subject_nr

	def parseLine(self, trialDict, l):

		"""
		desc:
			Parses a single line from the EyeLink .asc file.

		arguments:
			trialDict:
				desc:	Trial information.
				type:	dict
			l:
				desc:	A white-space-splitted line.
				type:	list
		"""

		# MSG	6720410 var stabilize False
		if 'stabilize' in l:
			if l[-1] == 'False':
				self.stabilize = 0
			elif l[-1] == 'True':
				self.stabilize = 1

		# MSG	1662043 item id="A" status=init likelihood=1 ecc=390 \
		# angle=0.785398163397 size=132 brightness=-1 color=green opacity=0.5 \
		# x=275.771644663 y=275.7716
		if 'targetAngle' not in trialDict and len(l) > 3 and l[2] == 'item':
			# id="A"
			_l = l[3].split('=')
			assert(_l[0] == 'id')
			letter = _l[1][1:-1]
			if letter == trialDict['target']:
				# angle=0.785398163397
				_l = l[7].split('=')
				assert(_l[0] == 'angle')
				angle = _l[1]
				trialDict['targetAngle'] = angle
				print('Target = %s, angle = %s' % (letter, angle))

		# Get baseline pupil size
		if self.baselinePupilSize is None:
			fix = self.toFixation(l)
			if fix is not None:
				self.baselinePupilSize = fix['pupilSize']

		# MSG	3647136 start_selection_loop
		if len(l) == 3 and l[2] == 'start_selection_loop':
			self.startTime = l[1]
		# MSG	3652559 prune yes
		if 'pruneRt' not in trialDict and len(l) == 4 and l[2] == 'prune' \
			and l[3] == 'yes':
			trialDict['pruneRt'] = l[1] - self.startTime

for dirpath, dirnames, filenames in os.walk('../data'):
	if 'Phase 4' in dirpath:
		continue
	for filename in filenames:
		if not filename.endswith('.edf'):
			continue
		src = os.path.join(dirpath, filename)
		tmp = src[:-4] + '.asc'
		target = os.path.join('data', filename[:-4] + '.asc')
		if not os.path.exists(target):
			subprocess.call(['edf2asc', '-e', src])
			os.rename(tmp, target)
			if os.path.exists('.cache/data.npy'):
				os.remove('.cache/data.npy')

@cachedDataMatrix
def getDataMatrix():
	return MyReader(blinkReconstruct=True, requireEndTrial=False).dataMatrix()
