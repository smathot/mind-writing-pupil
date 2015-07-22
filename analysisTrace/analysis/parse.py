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

import sys
from matplotlib import pyplot as plt
from exparser import Plot
from exparser.EyelinkAscFolderReader import EyelinkAscFolderReader
from exparser.Cache import cachedDataMatrix
from exparser import TraceKit as tk
from exparser.TangoPalette import *
import numpy as np
import pickle

# Display center
xc = 1280/2
yc = 1024/2
rnd = 0

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
		self.roundId = 0
		self.likelihoodTraces = {}
		self.active = False
		self.fixList = []
		trialDict['maxFixErr'] = 0
		trialDict['nFixLost'] = 0

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

		print 'nFixLost: %(nFixLost)d, maxFixErr = %(maxFixErr).2f' % trialDict
		trialDict['rt'] = self.endTime - self.startTime
		trialDict['correct'] = self.correct # Get the correct correct
		trialDict['endInvertTime'] = np.mean(self.endInvertTime)
		trialDict['endAdaptationTime'] = np.mean(self.endAdaptationTime)
		trialDict['endCollectionTime'] = np.mean(self.endCollectionTime)
		trialDict['endRoundTime'] = np.mean(self.endRoundTime)
		path = 'likelihood/%s-%.4d.pickle' % (trialDict['file'],
			trialDict['trialId'])
		trialDict['__likelihood__'] = path
		pickle.dump(self.likelihoodTraces, open(path, 'w'))

		# Determine the mean vector of the fixations
		fax = np.mean([xy[0] for xy in self.fixList])
		fay = np.mean([xy[1] for xy in self.fixList])
		fdx = fax - xc
		fdy = fay - yc
		fa = np.degrees(np.arctan2(fdy, fdx))
		fr = np.sqrt(fdx**2 + fdy**2)
		# Determine the vector of the target
		tx = trialDict['targetX']
		ty = trialDict['targetY']
		tdx = tx - xc
		tdy = ty - yc
		ta = np.degrees(np.arctan2(tdy, tdx))
		tr = np.sqrt(tdx**2 + tdy**2)
		# Determine the vector error
		errA = ta-fa
		if errA < 0:
			errA += 360
		trialDict['errA'] = errA
		trialDict['errR'] = fr
		s = 'Vector: r = %.2f, d(a) = %.2f' % (fr, errA)
		print s
		if '--plot' in sys.argv:
			Plot.new()
			plt.title(s)
			plt.xlim(0, 1280)
			plt.ylim(0, 1024)
			plt.axvline(xc, linestyle='--', color='black')
			plt.axhline(yc, linestyle='--', color='black')
			for x, y in self.fixList:
				plt.plot(x, y, '.', color=blue[1])
			plt.plot(tx, ty, 'o', color=orange[1])
			plt.plot([xc, xc+fdx], [yc, yc+fdy], color=blue[1])
			plt.plot([xc, xc+tdx], [yc, yc+tdy], color=orange[1])
			plotName = '%s-%d' % (trialDict['file'], trialDict['trialId'])
			Plot.save(plotName)

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

		trialDict['subject_nr'] = int(trialDict['file'][2:4])
		# The active period is the moment from the first round until the winner
		# is announced. This way we don't count the extra time taken by the
		# preview and end animation.
		if 'start_round' in l and l[3] == 0:
			self.active = True
			self.startTime = l[1]
		if 'status=winner' in l:
			self.active = False
			self.endTime = l[1]
		# Check for check fixation during the active period.
		if self.active:
			fix = self.toFixation(l)
			if fix != None:
				fixErr = np.sqrt( (fix['x']-xc)**2 + (fix['y']-yc)**2 )
				trialDict['maxFixErr'] = max(trialDict['maxFixErr'], fixErr)
				self.fixList.append( (fix['x'], fix['y']) )
			if 'fixation_lost' in l:
				trialDict['nFixLost'] += 1
		# Get target coordinates
		# MSG	18895724 item id="B" status=init likelihood=1 ecc=375
		# angle=0.785398163397 size=99 brightness=-1 color=green opacity=0.5
		# x=265.165042945 y=265.16504
		if 'target' in trialDict and ('id="%s"' % trialDict['target']) in l:
			if 'targetX' not in trialDict:
				# The x and y coordinates are sometimes chopped off, because the
				# logging string is too long. Therefore, we recalculate them
				# from the radius and eccentricity.
				for i in l:
					if type(i) != str:
						continue
					if 'ecc' in i:
						r = float(i[4:])
					if 'angle' in i:
						a = float(i[6:])
				x = np.cos(a) * r
				y = np.sin(a) * r
				# If possible, doubcheck the coordinates for strings that have
				# not been chopped off.
				try:
					_x = float(l[-2][2:])
					_y = float(l[-1][2:])
					assert(int(_x) == int(x))
					assert(int(_y) == int(y))
				except:
					print 'Failed to verify'
				trialDict['targetX'] = x
				trialDict['targetY'] = y
		# For Exp 1:
		# MSG	7093294 var correct 1
		# For Exp 2+:
		# MSG	7093294 var correct_selection 1
		if ('correct' in l or 'correct_selection' in l) and l[4] in (0, 1):
			self.correct = l[4]
		# Collect pupil trace
		# MSG	18625682 start_round 0
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
			if 'dummy' in self.traceDict:
				a = np.array(self.traceDict['dummy'], dtype=float)
				a[:,2] = tk.blinkReconstruct(a[:,2])
				global rnd
				path = 'traces/subject%0d-%04d-%s.npy' % \
					(trialDict['subject_nr'], rnd, self.phaseType)
				rnd += 1
				print(path)
				np.save(path, a)
				del self.traceDict['dummy']
			else:
				print('Warning: No trace collected!')
			self.tracePhase = None
			self.endRoundTime.append(l[1] - self.startRoundTime)
			self.roundId += 1
		# Collect item information and likelihood ratios
		# MSG	1806804 item id="B" status=init likelihood=1 ecc=310
		# angle=-0.785398163397 size=64 brightness=1 color=green opacity=0.5
		# x=219.203102168
		if self.tracePhase != None:
			# Process item
			if len(l) > 2 and l[2] == 'item':
				_dict = {}
				for s in l[3:]:
					_l = s.split('=')
					if len(_l) != 2:
						continue
					_dict[_l[0]] = _l[1].strip('"')
				if _dict['id'] == trialDict['target']:
					_id = 'target'
				else:
					_id = _dict['id']
				if _id not in self.likelihoodTraces:
					self.likelihoodTraces[_id] = []
				self.likelihoodTraces[_id].append(_dict['likelihood'])

@cachedDataMatrix
def getDataMatrix():
	return MyReader(blinkReconstruct=True).dataMatrix()
