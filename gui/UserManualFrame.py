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

from HtmlFrame import *

class UserManualFrame(HtmlFrame):
    """
    This class is a container for the User Manual.
    """

    def __init__(self, prnt):
        "Constructor for UserManualFrame."

        HtmlFrame.__init__(self, prnt, 'User Manual', 'help/index.html')

# The piece of code below enables an UserManualFrame to be run separately from any
# other application for testing/debugging purposes.

if __name__ == '__main__':
    import wx
    class MyApp(wx.App):
        def OnInit(self):
            frame = UserManualFrame(None)
            self.SetTopWindow(frame)
            frame.Show()
            return True
    app = MyApp(0)
    app.MainLoop()
