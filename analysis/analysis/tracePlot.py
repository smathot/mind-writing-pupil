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

@yamldoc.validate
def tracePlot(dm, dv='correct', phase=1, color=blue[1], style='o-'):

	"""
	desc:
		Plots the performance for individual blocks, as well as the mean
		performance on the first six blocks, and the gaze-stabilization block.

	arguments:
		dm:
			desc:	The data.
			type:	DataMatrix

	keywords:
		dv:
			desc:	The dependent variable.
			valid:	[correct, loop_rt]
		phase:
			desc:	The phase to analyze.
			valid:	[1,2,3]
		color:
			desc:	The line color.
			type:	str
		style:
			desc:	The line style.
			type:	str
	"""

	xData = []
	yData = []
	yMin = []
	yMax = []
	dm = dm.select('phase == %d' % phase)
	if len(dm) == 0:
		return
	__dm = dm.select('stabilize == 0')
	x = []
	y = []
	s = []
	for block in range(1, int(__dm['block'].max()+1)):
		_dm = dm.select('block == %d' % block)
		cm = _dm.collapse(['subject_nr'], dv)
		m = cm['mean']
		if __dm.count('subject_nr') > 1:
			for a in stats.itemfreq(m):
				y.append(a[0])
				x.append(block)
				s.append(2*a[1]**2)
		if block > 6 and __dm.count('subject_nr') != 1:
			continue
		acc = m.mean()
		xData.append(block)
		yData.append(acc)
		ci95 = 1.96*cm['mean'].std() / np.sqrt(len(cm))
		yMin.append(acc-ci95)
		yMax.append(acc+ci95)
	plt.xlim(-2, 16)
	plt.xticks([-1] + range(1, 13) + [14],
		['Avg.'] + range(1, 13) + ['Stb.'])
	plt.xlabel('Block nr.')
	plt.scatter(x, y, s=s, color=gray[2])
	plt.plot(xData, yData, style, color=color)
	plt.fill_between(xData, yMin, yMax, color=color, alpha=.25)
	# Averages of block 1 - 6
	_dm = dm.select('stabilize == 0', verbose=False)
	cm = _dm.collapse(['subject_nr'], dv)
	acc = cm['mean'].mean()
	ci95 = 1.96*cm['mean'].std() / np.sqrt(len(cm))
	plt.plot(-1, acc, 'o', color=color)
	plt.errorbar(-1, acc, yerr=ci95, color=color, capsize=0)
	# Gaze stabilizing block
	_dm = dm.select('stabilize == 1')
	cm = _dm.collapse(['subject_nr'], dv)
	print(cm)
	acc = cm['mean'].mean()
	ci95 = 1.96*cm['mean'].std() / np.sqrt(len(cm))
	plt.plot(14, acc, 'o', color=color)
	plt.errorbar(14, acc, yerr=ci95, color=color, capsize=0)

@yamldoc.validate
def subplot(phase=1, dv='correct', shading=False):

	"""
	desc:
		Creates a generic subplot in a 2x3 plot.

	keywords:
		phase:
			desc:	A phase.
			valid:	[1,2,3]
		dv:
			desc:	The dependent variable.
			valid:	[correct, loop_rt]
		shading:
			desc:	Indicates whether the critical value should be shaded.
			type:	bool
	"""

	if dv == 'correct':
		plt.subplot(2,3,phase)
		plt.axhline(1, color='black', linestyle=':')
		if phase == 1:
			plt.title('2 options')
			plt.axhline(.5, color='black', linestyle=':')
			if shading:
				plt.axhspan(critical2/16., 1, color=green[1], alpha=.1)
		elif phase == 2:
			plt.title('4 options')
			plt.axhline(.25, color='black', linestyle=':')
			if shading:
				plt.axhspan(critical4/16., 1, color=green[1], alpha=.1)
		elif phase == 3:
			plt.title('8 options')
			plt.axhline(.125, color='black', linestyle=':')
			if shading:
				plt.axhspan(critical8/16., 1, color=green[1], alpha=.1)
		plt.ylim(.0, 1.05)
		plt.yticks(np.linspace(0, 1, 5), [0, 25, 50, 75, 100])
		plt.ylabel('Accuracy (%)')
	else:
		plt.subplot(2,3,phase+3)
		plt.yticks(np.linspace(0, 50, 6))
		plt.ylim(0,60)
		plt.ylabel('Response time (s)')

@yamldoc.validate
def fullTracePlot(dm, suffix='', folder=None):

	"""
	desc:
		Plots the performance for individual blocks, as well as the mean
		performance on the first six blocks, and the gaze-stabilization block.

	arguments:
		dm:
			desc:	The data.
			type:	DataMatrix

	keywords:
		suffix:
			desc:	A suffix for the plot name.
			type:	str
		folder:
			desc:	A subfolder for the plot.
			type:	[str, NoneType]
	"""

	Plot.new(Plot.w)
	plt.subplots_adjust(wspace=0, hspace=0)
	for phase in [1,2,3]:
		subplot(dv='correct', phase=phase, shading=False)
		tracePlot(dm, phase=phase, dv='correct')
		plt.gca().xaxis.set_ticklabels([])
		if phase != 1:
			plt.gca().yaxis.set_ticklabels([])
			plt.ylabel('')
		subplot(dv='loop_rt', phase=phase)
		tracePlot(dm, phase=phase, dv='loop_rt')
		if phase != 1:
			plt.gca().yaxis.set_ticklabels([])
			plt.ylabel('')
	Plot.save('fullTracePlot'+suffix)

@yamldoc.validate
def fullTracePlotBySubject(dm):

	"""
	desc:
		Plots the performance for individual subjects in separate figures.

	arguments:
		dm:
			desc:	The data.
			type:	DataMatrix
	"""

	for subject_nr, _dm in dm.walk('subject_nr'):
		fullTracePlot(_dm, '.subject%.2d' % subject_nr, folder='subject')
