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

from exparser.EyelinkAscFolderReader import EyelinkAscFolderReader
from exparser.Cache import cachedDataMatrix
from exparser import TraceKit as tk
import numpy as np

# Display center
xc = 512
yc = 384

class MyReader(EyelinkAscFolderReader):

	"""An experiment-specific reader to parse the EyeLink data files."""

	def __init__(self):

		self.trialId = 0
		EyelinkAscFolderReader.__init__(self, blinkReconstruct=True, maxN=None,
			maxTrialId=None)

	def startTrial(self, l):

		"""
		desc:
			Detects the start of a trial.

		arguments:
			l:
				desc:	A whitespace-splitted line of data.
				type:	list

		returns:
			The trial id or None if l does not correspond to a trial start.
		"""

		if 'start_selection_loop' in l:
			return self.trialId
		return None

	def endTrial(self, l):

		"""
		desc:
			Detects the end of a trial.

		arguments:
			l:
				desc:	A whitespace-splitted line of data.
				type:	list

		returns:
			True if l corresponds to the start of a trial, False otherwise.
		"""

		return 'end_selection_loop' in l

	def initTrial(self, trialDict):

		"""
		desc:
			Performs pre-trial initialization.

		arguments:
			trialDict:
				desc:	Trial information.
				type:	dict
		"""

		self.startTime = None
		self.endTime = None

	def finishTrial(self, trialDict):

		"""
		desc:
			Performs post-trial initialization.

		arguments:
			trialDict:
				desc:	Trial information.
				type:	dict
			l:
				desc:	A whitespace-splitted line of data.
				type:	list
		"""

		trialDict['rt'] = self.endTime - self.startTime
		trialDict['correct'] = self.correct # Get the correct correct
		self.trialId += 1

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

		# MSG	7072763 start_round 0
		if 'start_round' in l and l[3] == 0:
			self.startTime = l[1]
		# MSG	7093294 var correct 1
		if 'correct' in l and l[4] in (0, 1):
			self.endTime = l[1]
			self.correct = l[4]
		# Collect pupil trace
		if 'start_round' in l:
			self.tracePhase = 'dummy'
		# Determine whether the target is bright or dark
		if self.tracePhase != None and 'item' in l:
			if 'id="%s"' % trialDict['target'] in l:
				if 'brightness=1.0' in l:
					self.phaseType = 'bright'
				elif 'brightness=-1.0' in l:
					self.phaseType = 'dark'
				else:
					raise Exception('Incorrect brightness!')
		if 'end_round' in l:
			a = np.array(self.traceDict['dummy'], dtype=float)
			a[:,2] = tk.blinkReconstruct(a[:,2])
			np.save('traces/%s-%04d.npy' % (self.phaseType, self.trialId), a)
			del self.traceDict['dummy']
			self.tracePhase = None

@cachedDataMatrix
def getDataMatrix():
	return MyReader().dataMatrix()
