# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the
#
# Free Software Foundation, Inc.,
# 675 Mass Ave
# Cambridge, MA 02139, USA

"""
The gui.framework library implements a lightweight plugin
framework that can be used to construct DEAP applications.  DEAP
functionality can be introduced into end-user applications by
hosting a DEAPPanel inside a top-level window derived from Frame.
"""

from   ConfigValues import ConfigValues
from   Application import Application
from   Frame       import *
from   Notebook    import Notebook
from   Panel       import Panel
from   PlotView    import PlotView
from   Shell       import Shell
import wxUnit
