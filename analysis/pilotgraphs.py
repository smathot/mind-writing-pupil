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

from exparser import Plot
from exparser.TangoPalette import *
from matplotlib import pyplot as plt

r = 42.5
rt_adjust = 1.185 # Remove the winning animation from the RT

errors = 0 + 2 + 1 + 0 + 2
total = 400 + 512 + 512 + 256 + 384

exp1 = [
	('Horiz.', 21.9, 2.57),
	('Up+', 15.44, 1.63),
	('Down+', 19.98, 2.43),
	('Up-', 20.99, 2.41),
	('Down-', 21.77, 2.57)
	]

exp2 = [
	('%.2f' % (164/r), 9.95, 1.09),
	('%.2f' % (304/r), 9.12, 0.92),
	('%.2f' % (445/r), 7.99, .58),
	('%.2f' % (585/r), 7.70, .6),
	]

exp3 = [
	('%.2f' % (33/r), 9.09, 1.03),
	('%.2f' % (66/r), 7.95, .67),
	('%.2f' % (99/r), 7.70, .64),
	('%.2f' % (132/r), 6.62, .52),
	]

exp4 = [
	('%.2f' % (375/r), 6.59, .48),
	('%.2f' % (446/r), 6.33, .42),
	]

exp5 = [
	('3.6', 5.87, .37),
	('22.9', 8.10, .78),
	('61.5', 9.33, .81),
	]

def pilotgraph(data, name, xlabel):

	Plot.new(size=(3,3))
	x = -.4
	xticks = []
	for key, rt, se in data:
		xticks.append(key)
		plt.bar(x, rt-rt_adjust, color=blue[1])
		plt.errorbar(x+.4, rt-rt_adjust, se, color='black', capsize=0)
		x += 1
	plt.xlim(-.7, x+.2)
	plt.xticks(range(len(data)), xticks)
	plt.xlabel(xlabel)
	plt.ylabel('Response time (s)')
	plt.ylim(0, 25)
	Plot.save(name, folder='pilot')

pilotgraph(exp1, 'pilot-exp1', u'Configuration')
pilotgraph(exp2, 'pilot-exp2', u'Eccentricity (°)')
pilotgraph(exp3, 'pilot-exp3', u'Size (°)')
pilotgraph(exp4, 'pilot-exp4', u'Eccentricity (°)')
pilotgraph(exp5, 'pilot-exp5', u'Background luminance (cd/m²)')
