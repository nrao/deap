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

from   wx import py
import wx

class Shell(py.shell.Shell):
    def __init__(self, parent, id, introText, locals):
        py.shell.Shell.__init__(self, parent, id, 
                                introText = introText,
                                locals    = locals)

    def GetHistory(self):
        "Returns a list of command executed.  The newest command is first."
        return self.history

    def SetHistory(self, history):
        "Sets the command line history. Newest commands first."
        self.history = history[::-1]
        self.ExecuteCommands(history)

    def ExecuteCommands(self, commands):
        """
        Executes the commands in the shell.  Each command is stripped of
        any Ctrl=M's introduced by Windows*.
        """
        for command in commands:
            busy = wx.BusyCursor()
            self.waiting = True
            self.more = self.interp.push(command.replace('\x0D', ''))
            self.waiting = False
            del busy
        self.prompt()

    def setBuiltinKeywords(self):
        """
        Override pseudo keywords as part of builtins.

        This sets `close`, `exit` and `quit` to a helpful string.
        """
        import __builtin__
        __builtin__.close = __builtin__.exit = __builtin__.quit = \
            'Please use File->Exit to exit the application.'
