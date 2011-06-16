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

from framework import Shell

class Wrapper:
    def __init__(self, object):
        """
        A simplistic wrapper class, which allows the user to exit the
        application by mapping keywords to callable objects.
        """
        self.object = object

    def __call__(self):
        "You can exit the application by typing: exit(), quit(), or close()."
        self.object.Close()
        self.object.GetGrandParent().Close()
        self.object.GetGrandParent().Destroy()

class DEAPPyShell(Shell):
    def __init__(self, parent, interpreter):
        self.interpreter = interpreter
        self.Hold(False)

        text = "Welcome to DEAP!\nThe pylab module is loaded and ready for use..\n"
        Shell.__init__(self, 
                       parent,
                       id = -1,
                       introText = text,
                       locals = interpreter.DefineFunctions())
        self.push("from pylab import *; import matplotlib")

    def GetInterpreter(self):
        return self.interpreter

    def Clear(self):
        self.GetInterpreter().clear()

    def Hold(self, state):
        self.GetInterpreter().hold(state)
        if state is None:
            self.hold = not self.hold
        else:
            self.hold = state

        if not self.hold:
            self.GetInterpreter().draw()

    def ExecuteCommands(self, commands):
        Shell.ExecuteCommands(self, commands)

        if not self.hold:
            self.GetInterpreter().draw()

    def setBuiltinKeywords(self):
        """
        Override pseudo keywords as part of builtins.

        This sets `close`, `exit` and `quit` to a helpful string.
        """
        import __builtin__
        __builtin__.close = __builtin__.exit = __builtin__.quit = \
            Wrapper(self)

    def push(self, command):
        try:
            Shell.push(self, command)
        except:
            if command[:command.rfind("(")] not in ("quit", "close", "exit"):
                raise
            return

        self.GetInterpreter().GetDocument().AddUndo(command)
        if not self.hold:
            self.GetInterpreter().draw()
