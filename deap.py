#!/usr/bin/env python

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

from   gui.framework      import Application
from   gui                import DEAPFrame
from   document           import Document
from   interpreter.python import Interpreter

class DEAPApp(Application):

    def __init__(self, console):
        Application.__init__(self, console, "")

    def OnInit(self):
        self.document    = Document()
        self.interpreter = Interpreter(self.document)

        # Create main GUI window
        self.main = DEAPFrame(None, self.interpreter)
        self.SetTopWindow(self.main)
        self.main.Show()

        return 1

    def Open(self, file):
        self.main.OpenFile(file)

def main(console, file):
    app = DEAPApp(console)

    if file is not None:
        app.Open(file)

    app.MainLoop()

if __name__ == '__main__':
    import sys

    file = None
    if len(sys.argv) > 1:
        file = sys.argv[1]
    main(1, file)
