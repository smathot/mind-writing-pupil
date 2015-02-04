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

		pass

	def finishTrial(self, trialDict):

		"""
		desc:
			Performs post-trial initialization.

		arguments:
			trialDict:
				desc:	Trial information.
				type:	dict
		"""

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

		pass

for dirpath, dirnames, filenames in os.walk('../data'):
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
	return MyReader(blinkReconstruct=True).dataMatrix()
