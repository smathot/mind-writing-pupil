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

def tracePlot(dm, dv='correct', phase=1, err=True, color='black'):

	xData = []
	yData = []
	yMin = []
	yMax = []
	dm = dm.select('phase == %d' % phase)
	if len(dm) == 0:
		return
	__dm = dm.select('stabilize == 0')
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

	_dm = dm.select('stabilize == 0')
	cm = _dm.collapse(['subject_nr'], dv)
	acc = cm['mean'].mean()
	se = 1.96*cm['mean'].std() / np.sqrt(len(cm))
	plt.plot(-1, acc, 'o', color=color)
	if err:
		plt.errorbar(-1, acc, yerr=se, color=color)

	_dm = dm.select('stabilize == 1')
	cm = _dm.collapse(['subject_nr'], dv)
	print(cm)
	acc = cm['mean'].mean()
	se = 1.96*cm['mean'].std() / np.sqrt(len(cm))
	plt.plot(14, acc, 'o', color=color)
	if err:
		plt.errorbar(14, acc, yerr=se, color=color)

def tracePlotSubject(dm, phase=1, dv='correct'):

	plt.axvline(6.5, color='black', linestyle=':')
	plt.xlim(-2, 16)
	plt.xticks(range(-2, 16),
		['', 'Overall', ''] + range(1, 13) + ['', 'Gaze stab.'])
	plt.xlabel('Block nr.')
	#colors = brightColors*10
	for _dm in dm.group('subject_nr'):
		n = int(_dm['subject_nr'][0])
		tracePlot(_dm, dv=dv, phase=phase, err=False, color=colors[n-1])
	tracePlot(dm, phase=phase, dv=dv)


def subplot(phase=1, dv='correct'):

	if dv == 'correct':
		plt.subplot(2,3,phase)
		plt.axhline(1, color='black', linestyle=':')
		if phase == 1:
			plt.title('2 options')
			plt.axhline(.5, color='black', linestyle=':')
			plt.axhspan(critical2/16., 1, color=green[1], alpha=.25)
		elif phase == 2:
			plt.title('4 options')
			plt.axhline(.25, color='black', linestyle=':')
			plt.axhspan(critical4/16., 1, color=green[1], alpha=.25)
		elif phase == 3:
			plt.title('8 options')
			plt.axhline(.125, color='black', linestyle=':')
			plt.axhspan(critical8/16., 1, color=green[1], alpha=.25)
		plt.ylim(.0, 1.05)
		plt.yticks(np.linspace(0, 1, 5), 100*np.linspace(0, 1, 5))
		plt.ylabel('Accuracy (%)')
		# if phase == 1:
		# 	plt.ylabel('Accuracy (%)')
		# else:
		# 	plt.gca().yaxis.set_ticklabels([])
		# plt.gca().xaxis.set_ticklabels([])

	else:
		plt.subplot(2,3,phase+3)
		plt.yticks(np.linspace(0, 60, 4))
		plt.ylim(0,60)
		plt.ylabel('Response time (s)')
		# if phase == 1:
		# 	plt.ylabel('Response time (s)')
		# else:
		# 	plt.gca().yaxis.set_ticklabels([])

def fullTracePlot(dm, suffix=''):

	Plot.new(Plot.w)
	# plt.subplots_adjust(wspace=0, hspace=0)
	for phase in [1,2,3]:
		subplot(dv='correct', phase=phase)
		tracePlotSubject(dm, phase=phase, dv='correct')
		subplot(dv='loop_rt', phase=phase)
		tracePlotSubject(dm.select('correct == 1'), phase=phase, dv='loop_rt')
	Plot.save('fullTracePlot'+suffix)

def fullTracePlotBySubject(dm):

	for subject_nr, _dm in dm.walk('subject_nr'):
		fullTracePlot(_dm, '.subject%.2d' % subject_nr)
