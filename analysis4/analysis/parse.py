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

		self.resp = ''
		self._resp = ''

	def finishTrial(self, trialDict):

		"""
		desc:
			Performs post-trial initialization.

		arguments:
			trialDict:
				desc:	Trial information.
				type:	dict
		"""

		trialDict['full_response'] = self.resp
		print trialDict['free_writing_result'], self.resp, self._resp

	def parseLine(self, trialDict, l):

		"""
		desc:
			Parses a single line from the EyeLink .asc file.

		arguments:
			trialDict:
				desc:	Trial information.trialDict['free_writing_result']
				desc:	A white-space-splitted line.
				type:	list
		"""

		# MSG	4721971 end_get_input I
		if 'end_get_input' in l:
			ch = l[3]
			if len(ch) == 1 or ch in ('Del', 'Space'):
				if ch == 'Space':
					ch = '_'
				elif ch == 'Del':
					ch = '<'
				if ch == '<':
					self._resp = self._resp[:-1]
				else:
					self._resp += ch
				#print self._resp
				self.resp += ch

@cachedDataMatrix
def getDataMatrix():
	return MyReader(blinkReconstruct=True, requireEndTrial=False).dataMatrix()
