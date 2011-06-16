# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
# more details. 
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the
#
# Free Software Foundation, Inc.,
# 675 Mass Ave
# Cambridge, MA 02139, USA.

from ConfigValues import ConfigValues

import time
import wx

class Application(wx.App):
    """
    Adds support for options and config files to a basic python
    application.  Use wx.GetApp() to access these methods.
    """
    
    def __init__(self, console, configPath):
        
        self.configValues =  ConfigValues(configPath)
        
        if console:
            wx.App.__init__(self, redirect = 0)
        else:
            wx.App.__init__(self)
            
    def OnInit(self):
        self.configValues.InitConfig()
        return 1

    def GetOption(self, name, key = None, default = None):        
        return self.configValues.GetOption(name, key, default)
