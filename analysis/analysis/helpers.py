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

from matplotlib import pyplot as plt
from exparser import Plot
from exparser.TangoPalette import *
import numpy as np

def phasePlot(dm, dv='correct', phase=1, err=True, color='black'):

	xData = []
	yData = []
	yMin = []
	yMax = []
	dm = dm.select('phase == %d' % phase)
	__dm = dm.select('stabilize == "no"')
	for block in range(1, int(__dm['block'].max()+1)):
		_dm = dm.select('block == %d' % block)
		cm = _dm.collapse(['subject_nr'], dv)
		acc = cm['mean'].mean()
		xData.append(block)
		yData.append(acc)
		se = 1.96*cm['mean'].std() / np.sqrt(len(cm))
		yMin.append(acc-se)
		yMax.append(acc+se)
	plt.plot(xData, yData, 'o-', color=color)
	if err:
		plt.fill_between(xData, yMin, yMax, color=color, alpha=.1)

	_dm = dm.select('stabilize == "no"')
	cm = _dm.collapse(['subject_nr'], dv)
	acc = cm['mean'].mean()
	se = 1.96*cm['mean'].std() / np.sqrt(len(cm))
	plt.plot(-1, acc, 'o', color=color)
	if err:
		plt.errorbar(-1, acc, yerr=se, color=color)

	_dm = dm.select('stabilize != "no"')
	cm = _dm.collapse(['subject_nr'], dv)
	print(cm)
	acc = cm['mean'].mean()
	se = 1.96*cm['mean'].std() / np.sqrt(len(cm))
	plt.plot(14, acc, 'o', color=color)
	if err:
		plt.errorbar(14, acc, yerr=se, color=color)

def phasePlotSubject(dm, phase=1, dv='correct'):

	plt.axvline(6.5, color='black', linestyle=':')
	plt.xlim(-2, 16)
	plt.xticks(range(-2, 16),
		['', 'Overall', ''] + range(1, 13) + ['', 'Gaze stab.'])
	plt.xlabel('Block nr.')
	colors = brightColors*10
	for _dm in dm.group('subject_nr'):
		phasePlot(_dm, dv=dv, phase=phase, err=False, color=colors.pop())
	phasePlot(dm, phase=phase, dv=dv)

def fullPlot(dm, phase=1):

	Plot.new()
	plt.subplot(211)
	plt.axhline(1, color='black', linestyle=':')
	plt.axhline(.5, color='black', linestyle=':')
	plt.ylim(.45, 1.05)
	plt.yticks(np.linspace(.5, 1, 6), 100*np.linspace(.5, 1, 6))
	plt.ylabel('Accuracy (%)')
	phasePlotSubject(dm, phase=phase, dv='correct')
	plt.subplot(212)

	plt.ylabel('Response time (s)')
	phasePlotSubject(dm.select('correct == 1'), phase=phase, dv='loop_rt')
	plt.show()
