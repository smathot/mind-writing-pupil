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
from exparser.DataMatrix import DataMatrix
from exparser.PivotMatrix import PivotMatrix
import numpy as np

#colors = [butter[0], orange[0], chameleon[0], skyBlue[0], plum[0],
#	scarletRed[0], butter[2], orange[2], chameleon[2], skyBlue[2]]
colors = allColors[:]*2
# Critical values for blocks of 16 trials
critical2 = 11
critical4 = 7
critical8 = 4
