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

import numpy as np
from exparser import Plot
from matplotlib import pyplot as plt
from exparser.TangoPalette import *

def bps(N, P):

	if P is None:
		return np.log2(N)
	return np.log2(N) + P * np.log2(P) + (1-P)*np.log2( (1-P)/(N-1))

def itr(rt, N, P):

	return bps(N, P) * (60./rt)

print('Pilot (Exp 5: SM):', itr(8.664-1.185, 2, None))
print('Pilot (Exp 5: LL):', itr(6.578-1.185, 2, None))


print('Stoll (HC):', itr(16.5, 2, .90))
print('Stoll (LIS):', itr(22.5, 2, .70))

print('Center spell:', itr(44.44, 30, .971))

print('Phase 1:', itr(14.6845, 2., .9083))
print('Phase 2:', itr(19.7127, 4., .9016))
print('Phase 3:', itr(28.1214, 8., .8634))
print('Phase 4 (raw):', itr(51.0775291309, 30., None))
print('Phase 4 (use):', itr(75.2328265173, 30., None))

def itrPhase(phase, N):
	a = np.loadtxt('phase%d.csv' % phase, delimiter=',')
	abr = np.zeros(a.shape[0])
	for i in range(a.shape[0]):
		rt = a[i,0]
		P = a[i,1]
		abr[i] = itr(rt, N, P)
	return abr, abr.mean(), abr.std()

Plot.new(size=Plot.xs)

a, m, sd = itrPhase(1, 2)
print(m)
plt.bar(0, m, width=.5, color=blue[1])
plt.plot([.25] * 10, a, 'o', color=green[2])

a, m, sd = itrPhase(2, 4)
print(m)
plt.bar(1, m, width=.5, color=blue[1])
plt.plot([1.25] * 9, a, 'o', color=green[2])

a, m, sd = itrPhase(3, 8)
print(m)
plt.bar(2, m, width=.5, color=blue[1])
plt.plot([2.25] * 9, a, 'o', color=green[2])

plt.ylabel('information-transfer rate (bits/min)')
plt.xlim(-.25, 2.75)
plt.xticks([.25, 1.25, 2.25],
	['Phase 1',
	'Phase 2',
	'Phase 3',
	])
Plot.save('bitrate')
