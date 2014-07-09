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
		self.endInvertTime = []
		self.endAdaptationTime = []
		self.endCollectionTime = []
		self.endRoundTime = []

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
		trialDict['endInvertTime'] = np.mean(self.endInvertTime)
		trialDict['endAdaptationTime'] = np.mean(self.endAdaptationTime)
		trialDict['endCollectionTime'] = np.mean(self.endCollectionTime)
		trialDict['endRoundTime'] = np.mean(self.endRoundTime)

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
			self.startRoundTime = l[1]
		# Determine whether the target is bright or dark
		if self.tracePhase != None and 'item' in l:
			if 'id="%s"' % trialDict['target'] in l:
				if 'brightness=1.0' in l:
					self.phaseType = 'bright'
				elif 'brightness=-1.0' in l:
					self.phaseType = 'dark'
				else:
					raise Exception('Incorrect brightness!')
		if 'end_invert' in l:
			self.endInvertTime.append(l[1] - self.startRoundTime)
		if 'end_adaptation' in l:
			self.endAdaptationTime.append(l[1] - self.startRoundTime)
		if 'end_collection' in l:
			self.endCollectionTime.append(l[1] - self.startRoundTime)
		if 'end_round' in l:
			a = np.array(self.traceDict['dummy'], dtype=float)
			a[:,2] = tk.blinkReconstruct(a[:,2])
			path = 'traces/%s-%04d-%s.npy' % (trialDict['file'][4:-5],
				trialDict['trialId'], self.phaseType)
			np.save(path, a)
			del self.traceDict['dummy']
			self.tracePhase = None
			self.endRoundTime.append(l[1] - self.startRoundTime)

@cachedDataMatrix
def getDataMatrix():
	return MyReader(blinkReconstruct=True).dataMatrix()
