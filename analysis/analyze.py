#!/usr/bin/env python
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

from exparser import Tools
from analysis import helpers, parse, tracePlot, barPlot, validate
Tools.analysisLoop(
	parse.getDataMatrix(cacheId='data'),
	mods=[helpers, tracePlot, barPlot, validate],
	pre=['_filter'],
	full=['fullBarPlot', 'fullTracePlot', 'fullTracePlotBySubject']
	)
